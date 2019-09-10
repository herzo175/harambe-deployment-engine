import subprocess

import templates

# TODO: delete resource (rio rm)

def deploy(app_name, deployment_id, storage_client, config):
    deployment_path = templates.download_project(
        deployment_id,
        config["deployments_bucket"],
        storage_client
    )

    with open(f"{deployment_path}/{config['deployment_file_name']}") as deployment_file:
        config_string = deployment_file.read()
        deployment_config = templates.load_config(config_string)

        for deployment in deployment_config["deployment"]: # TODO: rename
            tag = build_image(deployment_path, deployment_id, app_name, deployment, config)
            push_images(tag)
            run_deployment(deployment, tag)


def build_image(deployment_path, deployment_id, app_name, app_config, config):
    dockerfile_name = f"{deployment_path}/{app_config['name']}.Dockerfile"

    with open(dockerfile_name, "w") as dockerfile:
        dockerfile.write(
            templates.format_image(
                app_config,
                config["deployment_dockerfile_template"]
            )
        )

    # TODO: store deployment metadata
    docker_tag = f"registry.vask.io/{app_name}.{app_config['name']}:{deployment_id}"
    # NOTE: use docker-slim?
    out = subprocess.Popen([
        "docker", "build",
        "-t", docker_tag,
        "-f", dockerfile_name,
        deployment_path
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    _, stderr = out.communicate()

    if stderr is not None:
        print(stderr)
    else:
        return docker_tag


def push_images(docker_tag):
    # TODO: docker login
    out = subprocess.Popen([
        "docker", "push", docker_tag
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    _, stderr = out.communicate()

    if stderr is not None:
        print(stderr)


def run_deployment(app_config, docker_tag):
    # NOTE: possibly configure script from options+template
    # TODO: rio promote
    # TODO: namespaces
    # TODO: load env at runtime
    # TODO: save/return deployment ID
    out = subprocess.Popen(
        [
            "rio", "run", "-p", "8080/http", # TODO: configurable port
            "--name", app_config["name"],
            f"--scale={app_config['min_instances']}-{app_config['max_instances']}",
            docker_tag
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    stdout, stderr = out.communicate()
    return {"message": stdout, "error": stderr}
