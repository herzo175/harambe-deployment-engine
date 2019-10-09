import argparse
import os

import upload


def init(directory):
    parser = argparse.ArgumentParser()

    parser.add_argument("--name", default=None, dest="name", help="project name")
    parser.add_argument("--language", default="Dockerfile", dest="language", help="project language")

    args = parser.parse_args()


def deploy(project_id, directory):
    # zip project deployment.yml is in
    # NOTE: obscure zip file?
    deployment_file_path = upload.find_file(directory, "deployment.yml")
    assert deployment_file_path is not None, "missing deployment.yml"

    upload.create_deployments(project_id, deployment_file_path, directory)

    # os.remove(output_zip)
    # NOTE: facade will invoke deployment runner


def main():
    parser = argparse.ArgumentParser()
    # TODO: sub cli for command
    parser.add_argument("command", choices=["init", "deploy"])

    parser.add_argument("--dir", default=".", dest="dir", help="project directory")

    args = parser.parse_args()

    if args.command == "init":
        init(args.dir)
    elif args.command == "deploy":
        deploy(args.dir)
    else:
        print(f"invalid command {args.command}")


if __name__ == "__main__":
    main()
