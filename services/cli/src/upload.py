import os
import zipfile

import grpc

import deployments_pb2
import deployments_pb2_grpc


def get_source_paths(source_dir):
    filepaths = []

    for root, _, files in os.walk(source_dir):
        for filename in files:
            filepath = os.path.join(root, filename)
            filepaths += [filepath]

    return filepaths


def zip_source(source_dir, output_file):
    file_paths = get_source_paths(source_dir)

    with zipfile.ZipFile(output_file, "w") as output_zip:
        # writing each file one by one 
        for file in file_paths: 
            output_zip.write(file)


def upload_deployment(deployment_zip):
    with open(deployment_zip, "rb") as deployment_zip_file:
        with grpc.insecure_channel('localhost:5050') as channel: # TODO: get endpoint from config
            stub = deployments_pb2_grpc.DeploymentsStub(channel)
            response = stub.Upload(
                deployments_pb2.UploadRequest(
                    deploymentZip=deployment_zip_file.read()
                )
            )
            print("Greeter client received: " + response.uploadedKey)
