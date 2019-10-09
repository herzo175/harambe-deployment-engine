import os
import yaml
import zipfile

import jinja2
import boto3
from botocore.client import Config


# TODO: move to storage class
def get_storage_client(config):
    session = boto3.session.Session()
    return session.client("s3",
        region_name=config["storage_region"],
        endpoint_url=config["storage_endpoint"],
        aws_access_key_id=config["storage_access_key_id"],
        aws_secret_access_key=config["storage_secret_access_key"]
    )


# NOTE: maybe move to deployer?
def download_project(deployment_id, deployments_bucket, storage_client):
    # NOTE: possibly create parent folder for deployment zips to go to
    deployment_folder = f"deployment-{deployment_id}"
    deployment_zip = f"{deployment_folder}.zip"
    storage_client.download_file(deployments_bucket, deployment_zip, deployment_zip)

    with zipfile.ZipFile(deployment_zip, "r") as deployment_zip_folder:
        deployment_zip_folder.extractall(deployment_folder)
        os.remove(deployment_zip)

    return deployment_folder


def get_base_image(language):
    # TODO: Java, PHP, Go support
    if language in ["python", "python3", "python:3.7"]:
        return "python:3.7-slim-buster"
    elif language in ["python:3.6"]:
        return "python:3.6-slim-buster"
    elif language in ["python2", "python:2.7"]:
        return "python:2.7-slim-buster"
    else:
        raise ValueError("Invalid language choice")


def load_config(config_string):
    # TODO: validate config
    # TODO: config substitution
    return yaml.safe_load(config_string)


def format_image(deployment_config, template_file_path):
    template_file_parts = template_file_path.split("/")
    templateLoader = jinja2.FileSystemLoader(searchpath="." + "/".join(template_file_parts[:-1]))
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(template_file_parts[-1])

    return template.render(
        base_image=get_base_image(deployment_config["language"]),
        **deployment_config
    )
