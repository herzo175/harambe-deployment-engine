.PHONY: grpc-stubs

PY_GENERATE_STUB=python3 -m grpc_tools.protoc -I ../../protos --python_out=./src --grpc_python_out=./src
NAME=hde-runner
TAG?=$(shell git rev-parse head)
IMAGE=gcr.io/harambe-6/${NAME}:${TAG}

build:
	docker build -t ${IMAGE} .

run:
	docker run \
		--rm \
		-e GOOGLE_APPLICATION_CREDENTIALS=gcp.json \
		-v ~/.kube/config:/app/.kubeconfig \
		-v $(shell pwd)/harambe-6-account.json:/app/gcp.json \
		-p 5151:8080 \
		${IMAGE}

push:
	gcloud auth configure-docker
	docker push ${IMAGE}

deploy:
	cat deployment.mustache | IMAGE=${IMAGE} mo > deployment.yaml
	kubectl apply -f deployment.yaml
	rm deployment.yaml

grpc-stubs:
	$(PY_GENERATE_STUB) ../../protos/jobs.proto
	$(PY_GENERATE_STUB) ../../protos/runner.proto
	$(PY_GENERATE_STUB) ../../protos/deployments.proto