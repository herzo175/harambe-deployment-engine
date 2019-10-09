import grpc

import deployments_pb2
import deployments_pb2_grpc

def get_image(project_id, image_id): # NOTE: take deployments config file if needed
    with grpc.insecure_channel("localhost:5050") as channel: # TODO: get endpoint from config
        stub = deployments_pb2_grpc.DeploymentsStub(channel)
        return stub.GetImage(
            deployments_pb2.GetImageRequest(
                projectID=project_id,
                imageID=image_id
            )
        )
