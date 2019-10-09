import os
import tarfile

import grpc

import projects_pb2
import projects_pb2_grpc
import deployments_pb2
import deployments_pb2_grpc
import jobs_pb2
import jobs_pb2_grpc
import templates


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


def create_deployments(project_id, deployment_filename, deployment_root_dir):
    with open(deployment_filename) as deployment_file:
        config_string = deployment_file.read()
        deployment_config = templates.load_config(config_string)

        for job in deployment_config["jobs"]:
            job_path = os.path.join(deployment_root_dir, job['directory'])
            output_zip = os.path.join(job_path, "deployment.tar.gz")

            # determine image from job, upload and set image if not specified
            # NOTE: image must belong to project
            image = job.get("image")

            if image is None:
                # TODO: determine dockerfile template from job
                dockerfile_name = create_dockerfile(job_path, job, "Dockerfile.template.j2")
                zip_source(job_path, output_zip)
                image = upload_deployment(project_id, dockerfile_name, output_zip, job)

            assert image is not None, "Unable to resolve image"

            job_id = add_job_revision(project_id, job, image)
            # TODO: invoke deploy of job revision


def create_dockerfile(deployment_path, job_config, template_path):
    dockerfile_name = f"{job_config['name']}.Dockerfile"

    with open(os.path.join(deployment_path, dockerfile_name), "w") as dockerfile:
        dockerfile.write(
            templates.format_image(
                job_config,
                template_path
            )
        )

    return dockerfile_name


def zip_source(source_dir, output_file):
    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def upload_deployment(project_id, dockerfile, image_zip, job): # NOTE: take deployments config file if needed
    # TODO: auth
    with open(image_zip, "rb") as image_zip_file:
        with grpc.insecure_channel("localhost:5050") as channel: # TODO: get endpoint from config
            stub = deployments_pb2_grpc.DeploymentsStub(channel)
            response = stub.Upload(
                deployments_pb2.UploadRequest(
                    projectID=project_id,
                    jobName=job["name"],
                    dockerfile=dockerfile,
                    imageZip=image_zip_file.read(),
                    directory=job["directory"],
                    language=job["language"],
                    buildSteps=job["buildSteps"],
                    run=job["name"]
                )
            )

            return response.imageID


def get_image(project_id, image_tag):
    # TODO: auth
    with grpc.insecure_channel("localhost:5050") as channel: # TODO: get endpoint from config
        stub = deployments_pb2_grpc.DeploymentsStub(channel)
        response = stub.GetImage(
            deployments_pb2.GetImageRequest(
                projectID=project_id,
                imageTag=image_tag,
            )
        )

        return response.imageID


def add_job_revision(project_id, job, image_tag):
    # TODO: auth
    with grpc.insecure_channel("localhost:5050") as channel: # TODO: get endpoint from config
        stub = jobs_pb2_grpc.JobsStub(channel)
        response = stub.AddJobRevision(
            jobs_pb2.AddJobRevisionRequest(
                projectID=project_id,
                job=jobs_pb2.JobRevision(
                    imageTag=image_tag,
                    minInstances=job.get("minInstances", 0), # TODO: defaults
                    maxInstances=job.get("maxInstances", 1),
                    ports=job.get("ports"),
                    envVars=job.get("env", {}),
                    name=job["name"]
                )
            )
        )

        return response.jobRevisionID


def run_job_revision(project_id, job_id):
    with grpc.insecure_channel("localhost:5050") as channel: # TODO: get endpoint from config
        stub = jobs_pb2_grpc.JobsStub(channel)
        response = stub.RunJobRevision(
            jobs_pb2.RunJobRevisionRequest(
                projectID=project_id,
                jobID=job_id
            )
        )

        return response
