# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import deployments_pb2 as deployments__pb2


class DeploymentsStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Upload = channel.unary_unary(
        '/deployments.Deployments/Upload',
        request_serializer=deployments__pb2.UploadRequest.SerializeToString,
        response_deserializer=deployments__pb2.Image.FromString,
        )
    self.GetImage = channel.unary_unary(
        '/deployments.Deployments/GetImage',
        request_serializer=deployments__pb2.GetImageRequest.SerializeToString,
        response_deserializer=deployments__pb2.Image.FromString,
        )


class DeploymentsServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Upload(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetImage(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_DeploymentsServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Upload': grpc.unary_unary_rpc_method_handler(
          servicer.Upload,
          request_deserializer=deployments__pb2.UploadRequest.FromString,
          response_serializer=deployments__pb2.Image.SerializeToString,
      ),
      'GetImage': grpc.unary_unary_rpc_method_handler(
          servicer.GetImage,
          request_deserializer=deployments__pb2.GetImageRequest.FromString,
          response_serializer=deployments__pb2.Image.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'deployments.Deployments', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
