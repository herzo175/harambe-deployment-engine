import click

import upload

cli = click.Group()

@cli.command()
@click.argument("name")
def init(name):
    upload.create_project(name)


@cli.command()
@click.argument("project_id") # TODO: get project id from state file if not specified
@click.option("--directory", default=".")
@click.option("--deployment-file", default="deployment.yml")
def deploy(project_id, directory, deployment_file):
    # zip project deployment.yml is in
    # NOTE: obscure zip file?
    deployment_file_path = upload.find_file(directory, deployment_file)
    assert deployment_file_path is not None, f"missing {deployment_file}"

    upload.create_deployments(project_id, deployment_file_path, directory)


if __name__ == "__main__":
    cli()