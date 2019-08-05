import yaml

import jinja2


def get_base_image(language):
    # TODO: Java, PHP, Go support
    if language in ["python", "python3", "python:3.7"]:
        return "python:3.7"
    elif language in ["python:3.6"]:
        return "python:3.6"
    elif language in ["python2", "python:2.7"]:
        return "python:2.7"
    else:
        raise ValueError("Invalid language choice")


def load_config(config_string):
    # TODO: validate config
    # TODO: config substitution
    return yaml.safe_load(config_string)


def format_image(deployment_config, template_file):
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(template_file)
    outputText = template.render(
        base_image=get_base_image(deployment_config["language"]),
        deployment_config
    )
    print(outputText)


def push_image(filename):
    pass
