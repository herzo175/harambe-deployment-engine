import argparse

import upload


def upload_project(source_dir):
    # zip project deployment.yml is in
    output_zip = "./deployment.zip"

    # TODO: check that deployment.yml is in this source directory
    upload.zip_source(source_dir, output_zip)
    # multipart upload to API


def deploy():
    # upload project
    upload_project("./")
    # invoke deployment runner


def main():
    deploy()


if __name__ == "__main__":
    main()
