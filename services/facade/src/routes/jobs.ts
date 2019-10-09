import * as grpc from "grpc";
import * as protoLoader from "@grpc/proto-loader";
import { Datastore } from "../clients/datastore";
import { JobRevision } from "../models/jobRevision";
import { ObjectID } from "bson";
import { ulid } from "ulid";
import { DeploymentRunner } from "../clients/runner";
import { Document } from "mongoose";

const jobsProto: () => any = () => {
    const packageDefinition = protoLoader.loadSync(
        __dirname + '/../protos/jobs.proto',
        {
            keepCase: true,
            longs: String,
            enums: String,
            defaults: true,
            oneofs: true
        }
    );

    return grpc.loadPackageDefinition(packageDefinition).jobs;
}

function addJobRevision(datastore: Datastore) : (call: any, callback: any) => any {
    return (call, callback) => {
        datastore
            .getModel(JobRevision)
            .create({
                _id: ulid(),
                minInstances: call.request.job.minInstances,
                maxInstances: call.request.job.maxInstances,
                ports: call.request.job.ports,
                envVars: call.request.job.envVars,
                name: call.request.job.name,
                imageTag: call.request.job.imageTag,
                project: new ObjectID(call.request.projectID)
            })
            .then(job => {
                callback(null, {jobRevisionID: job._id});
            })
            .catch(err => {
                console.error(err);
                callback({code: grpc.status.INTERNAL, message: "error adding job revision"});
            })
    }
}

function runJobRevision(datastore: Datastore, runner: DeploymentRunner) : (call: any, callback: any) => any {
    return (call, callback) => {
        datastore
            .getModel(JobRevision)
            .findOne({project: new ObjectID(call.request.projectID), _id: call.request.jobID})
            .exec()
            .then(job => {
                runner.runDeployment(serializeJob(job), (err) => {
                    if (err) {
                        console.error(err);
                        callback({code: grpc.status.INTERNAL, message: "error running deployment"});
                    } else {
                        callback(null, serializeJob(job));
                    }
                });
            })
            .catch(err => {
                console.error(err);
                callback({code: grpc.status.NOT_FOUND, message: "job not found"});
            })
    }
}


function getJobRevisions(datastore: Datastore) : (call: any, callback: any) => any {
    return (call, callback) => {
        datastore
            .getModel(JobRevision)
            .find({project: new ObjectID(call.request.projectID)})
            .exec()
            .then(jobs => {
                callback(null, {jobs: jobs.map(j => serializeJob(j))});
            })
            .catch(err => {
                console.error(err);
                callback({code: grpc.status.NOT_FOUND, message: "project not found"});
            })
    }
}

function getJobRevisionByID(datastore: Datastore) : (call: any, callback: any) => any {
    return (call, callback) => {
        datastore
            .getModel(JobRevision)
            .findOne({project: new ObjectID(call.request.projectID), _id: call.request.jobID})
            .exec()
            .then(job => {
                callback(null, serializeJob(job));
            })
            .catch(err => {
                console.error(err);
                callback({code: grpc.status.NOT_FOUND, message: "project not found"});
            })
    }
}

function getCurrentJobRevision(datastore: Datastore) : (call: any, callback: any) => any {
    return (call, callback) => {
        datastore
            .getModel(JobRevision)
            .findOne({project: new ObjectID(call.request.projectID)}, {}, { sort: { _id : -1 } })
            .exec()
            .then(job => {
                callback(null, serializeJob(job));
            })
            .catch(err => {
                console.error(err);
                callback({code: grpc.status.NOT_FOUND, message: "project not found"});
            })
    }
}

function serializeJob(job: Document) : any {
    return {
        jobRevisionID: job._id,
        minInstances: job["minInstances"],
        maxInstances: job["maxInstances"],
        ports: job["ports"],
        envVars: job["envVars"].toJSON(),
        name: job["name"],
        imageTag: job["imageTag"],
    }
}

export {
    jobsProto,
    addJobRevision,
    runJobRevision,
    getJobRevisions,
    getJobRevisionByID,
    getCurrentJobRevision
}
