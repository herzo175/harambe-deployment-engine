import * as grpc from "grpc";

import { deploymentsProto, s3Client, upload } from "./routes/deployments";
import { ConfigManager } from "./config/appConfig";

function main() {
    const server = new grpc.Server();
    const config = new ConfigManager();

    const storageClient = s3Client(config);

    server.addService(
        deploymentsProto().Deployments.service,
        {
            upload: upload(storageClient, config)
        }
    );

    server.bind("0.0.0.0:8080", grpc.ServerCredentials.createInsecure()); // TODO: connection pool
    server.start();
}

main();
