from concurrent import futures
import time

import grpc

import api
import runner_pb2_grpc

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    runner_pb2_grpc.add_RunnerServicer_to_server(
        api.Runner(),
        server
    )

    server.add_insecure_port("[::]:5151")
    server.start()
    # server.wait_for_termination() # NOTE: upgrade grpc version (need python 3.8)
    try:
        while True:
            # Keep server on until keyboard interrupt
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()