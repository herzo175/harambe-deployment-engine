import * as grpc from "grpc";
import * as protoLoader from "@grpc/proto-loader";
import * as fs from "fs";
import * as s3 from "s3-client";
import { ulid } from "ulid";
import * as del from "del";
import { ConfigManager } from "../config/appConfig";
import { Datastore } from "../clients/datastore";
import { Image } from "../models/image";
import { DeploymentRunner } from "../clients/runner";
import { Document } from "mongoose";
import { ObjectID } from "bson";

const deploymentsProto: () => any = () => {
    const packageDefinition = protoLoader.loadSync(
        __dirname + '/../protos/deployments.proto',
        {
            keepCase: true,
            longs: String,
            enums: String,
            defaults: true,
            oneofs: true
        }
    );

    return grpc.loadPackageDefinition(packageDefinition).deployments;
}

const s3Client = (config : ConfigManager) => { // NOTE: move to clients?
    return s3.createClient({
        maxAsyncS3: 20,     // this is the default
        s3RetryCount: 3,    // this is the default
        s3RetryDelay: 1000, // this is the default
        multipartUploadThreshold: 20971520, // this is the default (20 MB)
        multipartUploadSize: 15728640, // this is the default (15 MB)
        s3Options: {
            accessKeyId: config.getString("storage_access_key_id"),
            secretAccessKey: config.getString("storage_secret_access_key"),
            region: config.getString("storage_region"),
            endpoint: config.getString("storage_endpoint")
        },
    });
}

const upload = (
    s3Client: any,
    datastore: Datastore,
    runner: DeploymentRunner,
    config: ConfigManager
) => { // TODO: interface for storage client
    return (call: any, callback: any) => {
        // TODO: streaming zip file parts
        // NOTE: use+create deployments folder if not exists?
        const imageID = ulid();
        const imageFile = `image-${imageID}.tar.gz`;

        fs.writeFile(imageFile, call.request.imageZip, (err) => {
            if (err) {
                callback({code: grpc.status.INVALID_ARGUMENT, message: err});
            } else {
                const params = {
                    localFile: imageFile,

                    s3Params: {
                        Bucket: config.getString("deployments_storage_bucket"),
                        Key: imageFile
                    }
                };

                const uploader = s3Client.uploadFile(params);

                uploader.on("error", function(err) {
                    callback({code: grpc.status.INTERNAL, message: err});
                });
                // uploader.on('progress', function() {
                //     console.log("progress", uploader.progressMd5Amount,
                //             uploader.progressAmount, uploader.progressTotal);
                // });
                uploader.on("end", function() {
                    console.log("done uploading " + imageFile);
                    del(imageFile);

                    runner.pushImage(
                        call.request.projectID,
                        imageID,
                        call.request.jobName,
                        call.request.dockerfile,
                        (err, resp) => {
                        if (err) {
                            console.error("error pushing image " + imageID, err);
                            callback({code: grpc.status.INTERNAL, message: "error while pushing image"});
                        } else {
                            datastore.getModel(Image).create({
                                _id: imageID,
                                project: new ObjectID(call.request.projectID), // TODO: imply project id from project name and user
                                jobName: call.request.jobName,
                                dockerfile: call.request.dockerfile,
                                imageTag: resp.imageTag,
                                directory: call.request.directory,
                                language: call.request.language,
                                buildSteps: call.request.buildSteps,
                                run: call.request.run
                            })
                            .then(image => {
                                callback(null, {imageID: image._id});
                            })
                            .catch(err => {
                                console.error("error saving image:", err);
                                callback({code: grpc.status.INTERNAL, message: "error saving image tag"});
                            });
                        }
                    })
                });
            }
        });
    }
}

function getImage(datastore: Datastore) : (call: any, callback: any) => any {
    return (call, callback) => {
        datastore
            .getModel(Image)
            .findOne({
                imageTag: call.request.imageTag,
                project: new ObjectID(call.request.projectID)
            })
            .exec()
            .then(image => {
                if (!image) {
                    callback({
                        code: grpc.status.NOT_FOUND,
                        // TODO: log request ID
                        message: `image ${call.request.imageID} not found`
                    });
                } else {
                    callback(null, serializeImage(image));
                }
            })
            .catch(err => {
                console.error(`error getting project with ID ${call.request.id}: ${err}`);
                callback({code: grpc.status.INTERNAL, message: err});
            });
    }
}

function serializeImage(image: Document) : any {
    return {
        imageID: image._id,
        projectID: image["project"],
        jobName: image["jobName"],
        dockerfile: image["dockerfile"],
        imageTag: image["imageTag"]
    }
}

export {
    deploymentsProto,
    s3Client,
    upload,
    getImage
}
