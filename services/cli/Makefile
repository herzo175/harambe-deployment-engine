.PHONY: grpc-stubs

PY_GENERATE_STUB=python3 -m grpc_tools.protoc -I src/protos --python_out=./src --grpc_python_out=./src

grpc-stubs:
	$(PY_GENERATE_STUB) src/protos/deployments.proto
	$(PY_GENERATE_STUB) src/protos/projects.proto
