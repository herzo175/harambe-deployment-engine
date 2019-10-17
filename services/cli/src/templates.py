import os
import yaml
import zipfile

import jinja2
import boto3
from botocore.client import Config


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


def format_image(deployment_config, template_filename):
    templateLoader = jinja2.FileSystemLoader(searchpath=os.path.dirname(__file__))
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(template_filename)

    return template.render(
        base_image=get_base_image(deployment_config["language"]),
        **deployment_config
    )
