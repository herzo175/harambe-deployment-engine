import * as grpc from "grpc";
import * as protoLoader from "@grpc/proto-loader";
import * as fs from "fs";
import * as uuid from "uuid/v4";
import * as s3 from "s3-client";
import * as del from "del";
import { ConfigManager } from "../config/appConfig";

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

const upload = (s3Client : any, config: ConfigManager) => { // TODO: interface for storage client
    return (call: any, callback: any) => {
        // NOTE: use+create deployments folder if not exists?
        const deploymentFile = `deployment-${uuid()}.zip`;

        fs.writeFile(deploymentFile, call.request.deploymentZip, (err) => {
            if (err) {
                callback({code: grpc.status.INVALID_ARGUMENT, message: err});
            } else {
                const params = {
                    localFile: deploymentFile,

                    s3Params: {
                        Bucket: config.getString("deployments_storage_bucket"),
                        Key: deploymentFile
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
                    console.log("done uploading " + deploymentFile);
                    del(deploymentFile);
                    callback(null, {uploadedKey: deploymentFile});
                });
            }
        });
    }
}

export {
    deploymentsProto,
    s3Client,
    upload
}
