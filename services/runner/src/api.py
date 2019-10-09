import runner_pb2
import runner_pb2_grpc
import deployer
import facade


class Runner(runner_pb2_grpc.RunnerServicer):

    def __init__(self):
        # TODO: get from outside class
        self.kube_api = deployer.get_kubernetes_api()

    def PushImage(self, request, context):
        image_tag = deployer.build_image(
            request.projectID,
            request.imageID,
            request.jobName,
            request.dockerfile,
            self.kube_api.CoreV1Api()
        )
        return runner_pb2.PushImageResponse(imageTag=image_tag)

    def RunDeployment(self, request, context):
        # NOTE: request job to dict?
        deployer.run_deployment(request, self.kube_api.CustomObjectsApi())
        return runner_pb2.DeployJobResponse()

    def DeleteDeployment(self, request, context):
        # NOTE: request job to dict?
        deployer.delete_deployment(request, self.kube_api.CustomObjectsApi())
        return runner_pb2.DeployJobResponse()
