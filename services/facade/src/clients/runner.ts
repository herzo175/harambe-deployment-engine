import * as grpc from "grpc";
import * as protoLoader from "@grpc/proto-loader";

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
    private host: string = null;

    constructor(endpoint: string, host: string, proto: any) {
        this.endpoint = endpoint;
        this.host = host;
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
        console.log(this.endpoint, this.host);
        return new this.proto.Runner(
            this.endpoint,
            grpc.credentials.createInsecure(),
            {
                "grpc.default_authority": this.host
            }
        );
    }
}

export {
    runnerProto,
    DeploymentRunner
}
