import * as grpc from "grpc";
import * as protoLoader from "@grpc/proto-loader";
import { Datastore } from "../clients/datastore";
import { Project } from "../models/project";
import { Document } from "mongoose";
import { ObjectID } from "bson";

const projectsProto: () => any = () => {
    const packageDefinition = protoLoader.loadSync(
        __dirname + `/../protos/projects.proto`,
        {
            keepCase: true,
            longs: String,
            enums: String,
            defaults: true,
            oneofs: true
        }
    );

    return grpc.loadPackageDefinition(packageDefinition).projects;
}

function createProject(datastore: Datastore) : (call: any, callback: any) => any {
    return (call, callback) => {
        // TODO: validator
        datastore.getModel(Project).create({
            "name": call.request.name,
            "language": call.request.language
        })
        .then(project => {
            callback(null, {projectID: project._id});
        })
        .catch(err => {
            console.error(`error creating project ${call.request.name}:`, err)
            callback({code: grpc.status.INTERNAL, message: err});
        });
    }
}

function serializeProject(project : Document) : any {
    return {
        projectID: project._id,
        name: project["name"]
    }
}

function getProjectByID(datastore: Datastore) : (call: any, callback: any) => any {
    return (call, callback) => {
        datastore
            .getModel(Project)
            .findById(new ObjectID(call.request.projectID))
            .exec()
            .then(project => {
                if (!project) {
                    callback({
                        code: grpc.status.NOT_FOUND,
                        // TODO: log request ID
                        message: `project ${call.request.projectID} not found`
                    });
                } else {
                    callback(null, serializeProject(project));
                }
            })
            .catch(err => {
                console.error(`error getting project with ID ${call.request.id}: ${err}`);
                callback({code: grpc.status.INTERNAL, message: err});
            });
    }
}

function getProjects(datastore: Datastore) : (call: any, callback: any) => any {
    // TODO: filter by user ID
    return (call, callback) => {
        const populatedFields = Object
            .keys({
                name: call.request.name
            })
            .reduce((newFields, field) => {
                if (!!call.request[field]) {
                    newFields[field] = call.request[field];
                }
                return newFields;
            }, {});

        datastore
            .getModel(Project)
            .find(populatedFields)
            .exec()
            .then(projects => {
                callback(null, {projects: projects.map(serializeProject)});
            })
            .catch(err => {
                console.error("error getting projects:", err);
                callback({code: grpc.status.INTERNAL, message: err});
            });
    }
}

export {
    projectsProto,
    createProject,
    getProjectByID,
    getProjects
}