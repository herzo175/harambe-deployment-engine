import * as grpc from "grpc";

import { deploymentsProto, s3Client, upload, getImage } from "./routes/deployments";
import { projectsProto, createProject, getProjectByID, getProjects } from "./routes/projects";
import { ConfigManager } from "./config/appConfig";
import { Datastore } from "./clients/datastore";
import { Project } from "./models/project";
import { Image } from "./models/image";
import { DeploymentRunner, runnerProto } from "./clients/runner";
import { jobsProto, addJobRevision, runJobRevision, getJobRevisions, getJobRevisionByID, getCurrentJobRevision } from "./routes/jobs";
import { JobRevision } from "./models/jobRevision";

function main() {
    const server = new grpc.Server();
    const config = new ConfigManager();

    const datastore = new Datastore(config.getString("db_url"));
    datastore.addModel("Project", Project);
    datastore.addModel("Image", Image);
    datastore.addModel("JobRevision", JobRevision);

    console.log(config.getString("NODE_ENV"));
    console.log(config.getString("runner_endpoint"));

    const storageClient = s3Client(config);
    const deploymentRunner = new DeploymentRunner(
        config.getString("runner_endpoint"),
        config.getString("runner_host"),
        runnerProto()
    );

    server.addService(
        deploymentsProto().Deployments.service,
        {
            Upload: upload(storageClient, datastore, deploymentRunner, config),
            GetImage: getImage(datastore)
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

    server.addService(
        jobsProto().Jobs.service,
        {
            AddJobRevision: addJobRevision(datastore),
            RunJobRevision: runJobRevision(datastore, deploymentRunner),
            GetJobRevisions: getJobRevisions(datastore),
            GetJobRevisionByID: getJobRevisionByID(datastore),
            GetCurrentJobRevision: getCurrentJobRevision(datastore)
        }
    )

    server.bind("0.0.0.0:8080", grpc.ServerCredentials.createInsecure()); // TODO: connection pool
    server.start();
}

main();
