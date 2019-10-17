# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: projects.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='projects.proto',
  package='projects',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0eprojects.proto\x12\x08projects\"$\n\x14\x43reateProjectRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"*\n\x15\x43reateProjectResponse\x12\x11\n\tprojectID\x18\x01 \x01(\t\"*\n\x15GetProjectByIDRequest\x12\x11\n\tprojectID\x18\x01 \x01(\t\"2\n\x0fProjectResponse\x12\x11\n\tprojectID\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"\"\n\x12GetProjectsRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"?\n\x10ProjectsResponse\x12+\n\x08projects\x18\x01 \x03(\x0b\x32\x19.projects.ProjectResponse2\xf9\x01\n\x08Projects\x12R\n\rCreateProject\x12\x1e.projects.CreateProjectRequest\x1a\x1f.projects.CreateProjectResponse\"\x00\x12N\n\x0eGetProjectByID\x12\x1f.projects.GetProjectByIDRequest\x1a\x19.projects.ProjectResponse\"\x00\x12I\n\x0bGetProjects\x12\x1c.projects.GetProjectsRequest\x1a\x1a.projects.ProjectsResponse\"\x00\x62\x06proto3')
)




_CREATEPROJECTREQUEST = _descriptor.Descriptor(
  name='CreateProjectRequest',
  full_name='projects.CreateProjectRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='projects.CreateProjectRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=64,
)


_CREATEPROJECTRESPONSE = _descriptor.Descriptor(
  name='CreateProjectResponse',
  full_name='projects.CreateProjectResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='projectID', full_name='projects.CreateProjectResponse.projectID', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=66,
  serialized_end=108,
)


_GETPROJECTBYIDREQUEST = _descriptor.Descriptor(
  name='GetProjectByIDRequest',
  full_name='projects.GetProjectByIDRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='projectID', full_name='projects.GetProjectByIDRequest.projectID', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=110,
  serialized_end=152,
)


_PROJECTRESPONSE = _descriptor.Descriptor(
  name='ProjectResponse',
  full_name='projects.ProjectResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='projectID', full_name='projects.ProjectResponse.projectID', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='projects.ProjectResponse.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=154,
  serialized_end=204,
)


_GETPROJECTSREQUEST = _descriptor.Descriptor(
  name='GetProjectsRequest',
  full_name='projects.GetProjectsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='projects.GetProjectsRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=206,
  serialized_end=240,
)


_PROJECTSRESPONSE = _descriptor.Descriptor(
  name='ProjectsResponse',
  full_name='projects.ProjectsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='projects', full_name='projects.ProjectsResponse.projects', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=242,
  serialized_end=305,
)

_PROJECTSRESPONSE.fields_by_name['projects'].message_type = _PROJECTRESPONSE
DESCRIPTOR.message_types_by_name['CreateProjectRequest'] = _CREATEPROJECTREQUEST
DESCRIPTOR.message_types_by_name['CreateProjectResponse'] = _CREATEPROJECTRESPONSE
DESCRIPTOR.message_types_by_name['GetProjectByIDRequest'] = _GETPROJECTBYIDREQUEST
DESCRIPTOR.message_types_by_name['ProjectResponse'] = _PROJECTRESPONSE
DESCRIPTOR.message_types_by_name['GetProjectsRequest'] = _GETPROJECTSREQUEST
DESCRIPTOR.message_types_by_name['ProjectsResponse'] = _PROJECTSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CreateProjectRequest = _reflection.GeneratedProtocolMessageType('CreateProjectRequest', (_message.Message,), dict(
  DESCRIPTOR = _CREATEPROJECTREQUEST,
  __module__ = 'projects_pb2'
  # @@protoc_insertion_point(class_scope:projects.CreateProjectRequest)
  ))
_sym_db.RegisterMessage(CreateProjectRequest)

CreateProjectResponse = _reflection.GeneratedProtocolMessageType('CreateProjectResponse', (_message.Message,), dict(
  DESCRIPTOR = _CREATEPROJECTRESPONSE,
  __module__ = 'projects_pb2'
  # @@protoc_insertion_point(class_scope:projects.CreateProjectResponse)
  ))
_sym_db.RegisterMessage(CreateProjectResponse)

GetProjectByIDRequest = _reflection.GeneratedProtocolMessageType('GetProjectByIDRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETPROJECTBYIDREQUEST,
  __module__ = 'projects_pb2'
  # @@protoc_insertion_point(class_scope:projects.GetProjectByIDRequest)
  ))
_sym_db.RegisterMessage(GetProjectByIDRequest)

ProjectResponse = _reflection.GeneratedProtocolMessageType('ProjectResponse', (_message.Message,), dict(
  DESCRIPTOR = _PROJECTRESPONSE,
  __module__ = 'projects_pb2'
  # @@protoc_insertion_point(class_scope:projects.ProjectResponse)
  ))
_sym_db.RegisterMessage(ProjectResponse)

GetProjectsRequest = _reflection.GeneratedProtocolMessageType('GetProjectsRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETPROJECTSREQUEST,
  __module__ = 'projects_pb2'
  # @@protoc_insertion_point(class_scope:projects.GetProjectsRequest)
  ))
_sym_db.RegisterMessage(GetProjectsRequest)

ProjectsResponse = _reflection.GeneratedProtocolMessageType('ProjectsResponse', (_message.Message,), dict(
  DESCRIPTOR = _PROJECTSRESPONSE,
  __module__ = 'projects_pb2'
  # @@protoc_insertion_point(class_scope:projects.ProjectsResponse)
  ))
_sym_db.RegisterMessage(ProjectsResponse)



_PROJECTS = _descriptor.ServiceDescriptor(
  name='Projects',
  full_name='projects.Projects',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=308,
  serialized_end=557,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateProject',
    full_name='projects.Projects.CreateProject',
    index=0,
    containing_service=None,
    input_type=_CREATEPROJECTREQUEST,
    output_type=_CREATEPROJECTRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetProjectByID',
    full_name='projects.Projects.GetProjectByID',
    index=1,
    containing_service=None,
    input_type=_GETPROJECTBYIDREQUEST,
    output_type=_PROJECTRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetProjects',
    full_name='projects.Projects.GetProjects',
    index=2,
    containing_service=None,
    input_type=_GETPROJECTSREQUEST,
    output_type=_PROJECTSRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_PROJECTS)

DESCRIPTOR.services_by_name['Projects'] = _PROJECTS

# @@protoc_insertion_point(module_scope)
