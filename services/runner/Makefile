.PHONY: grpc-stubs

PY_GENERATE_STUB=python3 -m grpc_tools.protoc -I ../../protos --python_out=./src --grpc_python_out=./src

grpc-stubs:
	$(PY_GENERATE_STUB) ../../protos/jobs.proto
	$(PY_GENERATE_STUB) ../../protos/runner.proto
	$(PY_GENERATE_STUB) ../../protos/deployments.proto