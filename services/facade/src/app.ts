import * as grpc from "grpc";

import { deploymentsProto, s3Client, upload } from "./routes/deployments";
import { projectsProto, createProject, getProjectByID, getProjects } from "./routes/projects";
import { ConfigManager } from "./config/appConfig";
import { Datastore } from "./clients/datastore";
import { Project } from "./models/project";

function main() {
    const server = new grpc.Server();
    const config = new ConfigManager();

    const datastore = new Datastore(config.getString("db_url"));
    datastore.addModel("Project", Project);

    const storageClient = s3Client(config);

    server.addService(
        deploymentsProto().Deployments.service,
        {
            Upload: upload(storageClient, config)
        }
    );

    server.addService(
        projectsProto().Projects.service,
        {
            CreateProject: createProject(datastore),
            GetProjectByID: getProjectByID(datastore),
            GetProjects: getProjects(datastore)
        }
    );

    server.bind("0.0.0.0:8080", grpc.ServerCredentials.createInsecure()); // TODO: connection pool
    server.start();
}

main();
