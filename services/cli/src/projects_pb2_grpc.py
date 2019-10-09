# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import projects_pb2 as projects__pb2


class ProjectsStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.CreateProject = channel.unary_unary(
        '/projects.Projects/CreateProject',
        request_serializer=projects__pb2.CreateProjectRequest.SerializeToString,
        response_deserializer=projects__pb2.CreateProjectResponse.FromString,
        )
    self.GetProjectByID = channel.unary_unary(
        '/projects.Projects/GetProjectByID',
        request_serializer=projects__pb2.GetProjectByIDRequest.SerializeToString,
        response_deserializer=projects__pb2.ProjectResponse.FromString,
        )
    self.GetProjects = channel.unary_unary(
        '/projects.Projects/GetProjects',
        request_serializer=projects__pb2.GetProjectsRequest.SerializeToString,
        response_deserializer=projects__pb2.ProjectsResponse.FromString,
        )


class ProjectsServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def CreateProject(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetProjectByID(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetProjects(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ProjectsServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'CreateProject': grpc.unary_unary_rpc_method_handler(
          servicer.CreateProject,
          request_deserializer=projects__pb2.CreateProjectRequest.FromString,
          response_serializer=projects__pb2.CreateProjectResponse.SerializeToString,
      ),
      'GetProjectByID': grpc.unary_unary_rpc_method_handler(
          servicer.GetProjectByID,
          request_deserializer=projects__pb2.GetProjectByIDRequest.FromString,
          response_serializer=projects__pb2.ProjectResponse.SerializeToString,
      ),
      'GetProjects': grpc.unary_unary_rpc_method_handler(
          servicer.GetProjects,
          request_deserializer=projects__pb2.GetProjectsRequest.FromString,
          response_serializer=projects__pb2.ProjectsResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'projects.Projects', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))