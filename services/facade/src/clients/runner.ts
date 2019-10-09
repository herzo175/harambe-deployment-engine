import * as grpc from "grpc";
import * as protoLoader from "@grpc/proto-loader";

import { JobRevision } from "../models/jobRevision";

const runnerProto: () => any = () => {
    const packageDefinition = protoLoader.loadSync(
        __dirname + '/../protos/runner.proto',
        {
            keepCase: true,
            longs: String,
            enums: String,
            defaults: true,
            oneofs: true
        }
    );

    return grpc.loadPackageDefinition(packageDefinition).runner;
}

class DeploymentRunner {
    private proto = null;
    private endpoint: string = null;

    constructor(endpoint: string, proto: any) {
        this.endpoint = endpoint;
        this.proto = proto;
    }

    public pushImage(
        projectID: string,
        imageID: string,
        jobName: string,
        dockerfile: string,
        callback: (err: any, response: any) => void
    ) {
        this.getClient().PushImage({projectID, imageID, jobName, dockerfile}, callback);
    }

    public runDeployment(job: any, callback: (err: any, response: any) => void) {
        this.getClient().RunDeployment(job, callback);
    }

    private getClient() {
        return new this.proto.Runner(this.endpoint, grpc.credentials.createInsecure());
    }
}

export {
    runnerProto,
    DeploymentRunner
}
