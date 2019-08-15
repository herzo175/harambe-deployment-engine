import subprocess


# TODO: get instance info
# TODO: push image to registry
# TODO: delete resource (rio rm)


def push_image():
    pass


def deploy(config):
    # NOTE: possibly configure script from options+template
    # TODO: namespaces
    # TODO: load env at runtime
    # TODO: save/return deployment ID
    out = subprocess.Popen(
        [
            "rio", "run", "-p", "8080/http",
            "--name", config["name"],
            f"--scale={config['min_instances']}-{config['max_instances']}",
            f"{config['image']}:{config['version']}"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    stdout, stderr = out.communicate()
    return {"message": stdout, "error": stderr}
