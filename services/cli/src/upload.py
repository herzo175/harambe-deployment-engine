import os
import zipfile

import grpc

import projects_pb2
import projects_pb2_grpc
import deployments_pb2
import deployments_pb2_grpc


def create_project(options):
    # TODO: auth
    with grpc.insecure_channel("localhost:5050") as channel: # TODO: get endpoint from config
        stub = projects_pb2_grpc.ProjectsStub(channel)
        response = stub.CreateProject(
            projects_pb2.CreateProjectRequest(
                name=options["name"],
                language=options["language"]
            )
        )

        return response.projectID


def get_project_by_id(project_id):
    with grpc.insecure_channel("localhost:5050") as channel:
        stub = projects_pb2_grpc.ProjectsStub(channel)
        response = stub.GetProjectByID(
            projects_pb2.GetProjectByIDRequest(
                projectID=project_id # NOTE: default to None to exclude filter
            )
        )

        return response


def find_file(source_dir, filename):
    # from os import listdir
    # from os.path import isfile, join
    for file in [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]:
        if file == filename:
            return os.path.join(source_dir, filename)


def zip_source(source_dir, output_file):
    with zipfile.ZipFile(output_file, "w") as output_zip:
        source_dir_len = len(source_dir)

        for root, _ , files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                output_zip.write(file_path, file_path[source_dir_len:])


def upload_deployment(deployment_zip):
    # TODO: auth
    with open(deployment_zip, "rb") as deployment_zip_file:
        with grpc.insecure_channel("localhost:5050") as channel: # TODO: get endpoint from config
            stub = deployments_pb2_grpc.DeploymentsStub(channel)
            response = stub.Upload(
                deployments_pb2.UploadRequest(
                    deploymentZip=deployment_zip_file.read()
                )
            )
            # TODO: return deployment ID
            print("Deployment zip: " + response.uploadedKey)
