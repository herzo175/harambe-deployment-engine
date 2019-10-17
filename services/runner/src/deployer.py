import time

import kubernetes

# TODO: move kube methods?
def get_kubernetes_api(in_cluster=False):
    if in_cluster:
        kubernetes.config.load_incluster_config()
    else:
        kubernetes.config.load_kube_config(config_file=".kubeconfig")

    return kubernetes.client


def build_image(project_id, image_id, job_name, dockerfile, kube_api):
    # TODO: get master repository name (harambe-6) from config
    # NOTE: use job instead of pod?
    docker_tag = f"gcr.io/harambe-6/{project_id}-{job_name}:{image_id}"
    pod_name = f"kaniko-{image_id}".lower()
    image_context = f"s3://deployments-to-registry/image-{image_id}.tar.gz"

    pod_manifest = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": pod_name
        },
        "spec": {
            "restartPolicy": "Never",
            "volumes": [{
                "name": "kaniko-secrets",
                "secret": {
                    "secretName": "kaniko-secrets"
                }
            }],
            "containers": [{
                "image": "gcr.io/kaniko-project/executor:latest",
                "name": "kaniko",
                "args": [
                    f"--dockerfile={dockerfile}",
                    f"--context={image_context}",
                    f"--destination={docker_tag}"
                ],
                "volumeMounts": [{
                    "name": "kaniko-secrets",
                    "mountPath": "/secret"
                }],
                "env": [
                    {
                        "name": "GOOGLE_APPLICATION_CREDENTIALS",
                        "value": "/secret/harambe-6-account.json"
                    },
                    {
                        "name": "AWS_ACCESS_KEY_ID",
                        "valueFrom": {
                            "secretKeyRef": {
                                "name": "kaniko-secrets",
                                "key": "account-id"
                            }
                        }
                    },
                    {
                        "name": "AWS_SECRET_ACCESS_KEY",
                        "valueFrom": {
                            "secretKeyRef": {
                                "name": "kaniko-secrets",
                                "key": "secret-access-key"
                            }
                        }
                    },
                    {
                        "name": "AWS_REGION",
                        "valueFrom": {
                            "secretKeyRef": {
                                "name": "kaniko-secrets",
                                "key": "region"
                            }
                        }
                    },
                    {
                        "name": "S3_ENDPOINT",
                        "valueFrom": {
                            "secretKeyRef": {
                                "name": "kaniko-secrets",
                                "key": "endpoint"
                            }
                        }
                    },
                    {
                        "name": "S3_FORCE_PATH_STYLE",
                        "value": "true"
                    },
                ]
            }]
        }
    }

    # TODO: run in project namespace
    resp = kube_api.create_namespaced_pod(
        body=pod_manifest, namespace="default"
    )

    while True:
        resp = kube_api.read_namespaced_pod(name=pod_name, namespace="default")

        if resp.status.phase in ["Failed", "Succeeded", "Unknown"]:
            break

        time.sleep(1)

    kube_api.delete_namespaced_pod(name=pod_name, namespace="default")

    return docker_tag


def run_deployment(job, kube_api):
    # TODO: rolling deploy
    # TODO: get namespace
    # NOTE: include project id in job name?
    namespace = "default"
    manifest = generate_job_manifest(job)

    # Get service by service name
    resp = None

    try:
        resp = kube_api.get_namespaced_custom_object(
            group="serving.knative.dev",
            version="v1alpha1",
            name=job.name,
            namespace=namespace,
            plural="services"
        )
    except kubernetes.client.rest.ApiException as e:
        if e.status != 404:
            return e

    if resp is None:
        resp = kube_api.create_namespaced_custom_object(
            group="serving.knative.dev",
            version="v1alpha1",
            namespace=namespace,
            plural="services",
            body=manifest
        )
    else:
        resp = kube_api.patch_namespaced_custom_object(
            group="serving.knative.dev",
            version="v1alpha1",
            name=job.name,
            namespace=namespace,
            plural="services",
            body=manifest
        )

    # check if deployment succeeded
    # TODO: healthcheck
    while True:
        try:
            kube_api.get_namespaced_custom_object(
                group="serving.knative.dev",
                version="v1alpha1",
                namespace=namespace,
                plural="routes",
                name=job.name
            )
            # TODO: check traffic cutover
            break
        except kubernetes.client.rest.ApiException as e:
            if e.status != 404:
                return e
            else:
                time.sleep(1)

    return None


def delete_deployment(job, kube_api):
    namespace = "default"
    manifest = generate_job_manifest(job)

    kube_api.patch_namespaced_custom_object(
        group="serving.knative.dev",
        version="v1alpha1",
        name=job.name,
        namespace=namespace,
        plural="services",
        body=manifest
    )

    # Keep checking if object still exists until it 404's
    while True:
        try:
            kube_api.get_namespaced_custom_object(
                group="serving.knative.dev",
                version="v1alpha1",
                namespace=namespace,
                plural="routes",
                name=job.name
            )
            time.sleep(1)
        except kubernetes.client.rest.ApiException as e:
            if e.status != 404:
                return e
            else:
                break

    return None


def generate_job_manifest(job):
    # TODO: concurrent requests, memory cap
    # TODO: do not allow implicit use of gcp service account
    # TODO: ^ create gcloud iam service-account+k8 service account+iam -> k8 binding per namespace
    # TODO: resolve secrets for env
    # TODO: DNS records for service
    # TODO: http1.1 configurable
    return {
        "apiVersion": "serving.knative.dev/v1alpha1",
        "kind": "Service",
        "metadata": {
            "name": job.name
        },
        "spec": {
            "template": {
                "metadata": {
                    "annotations": {
                        "autoscaling.knative.dev/class": "kpa.autoscaling.knative.dev",
                        "autoscaling.knative.dev/metric": "concurrency",
                        "autoscaling.knative.dev/target": "100",
                        "autoscaling.knative.dev/minScale": str(job.minInstances),
                        "autoscaling.knative.dev/maxScale": str(job.maxInstances)
                    }
                },
                "spec": {
                    "containers": [{
                        "name": job.name,
                        "image": job.imageTag,
                        "env": [{
                            "name": name,
                            "value": job.envVars[name]
                        } for name in job.envVars],
                        "ports": {
                            "name": "h2c",
                            "containerPort": 8080
                        }
                    }]
                }
            }
        }
    }
