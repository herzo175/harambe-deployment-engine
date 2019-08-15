.PHONY: grpc-stubs

PY_GENERATE_STUB=python3 -m grpc_tools.protoc -I ../facade/src/protos --python_out=./src --grpc_python_out=./src

grpc-stubs:
	$(PY_GENERATE_STUB) ../facade/src/protos/deployments.proto
