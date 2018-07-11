# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: payload.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='payload.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\rpayload.proto\"\xa6\x03\n\x07Payload\x12\x1f\n\x06\x61\x63tion\x18\x01 \x01(\x0e\x32\x0f.Payload.Action\x12\x11\n\ttimestamp\x18\x02 \x01(\x04\x12,\n\x0e\x63reate_project\x18\x03 \x01(\x0b\x32\x14.CreateProjectAction\x12&\n\x0b\x63reate_item\x18\x04 \x01(\x0b\x32\x11.CreateItemAction\x12\"\n\tedit_item\x18\x05 \x01(\x0b\x32\x0f.EditItemAction\x12\x30\n\x10increment_sprint\x18\x06 \x01(\x0b\x32\x16.IncrementSprintAction\x12 \n\x08\x61\x64\x64_user\x18\x07 \x01(\x0b\x32\x0e.AddUserAction\x12&\n\x0bremove_user\x18\x08 \x01(\x0b\x32\x11.RemoveUserAction\"q\n\x06\x41\x63tion\x12\x12\n\x0e\x43REATE_PROJECT\x10\x00\x12\x0f\n\x0b\x43REATE_ITEM\x10\x01\x12\r\n\tEDIT_ITEM\x10\x02\x12\x14\n\x10INCREMENT_SPRINT\x10\x03\x12\x0c\n\x08\x41\x44\x44_USER\x10\x04\x12\x0f\n\x0bREMOVE_USER\x10\x05\"+\n\x13\x43reateProjectAction\x12\x14\n\x0cproject_name\x18\x01 \x01(\t\"\x12\n\x10\x43reateItemAction\"\x10\n\x0e\x45\x64itItemAction\"\x17\n\x15IncrementSprintAction\"\x0f\n\rAddUserAction\"\x12\n\x10RemoveUserActionb\x06proto3')
)



_PAYLOAD_ACTION = _descriptor.EnumDescriptor(
  name='Action',
  full_name='Payload.Action',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CREATE_PROJECT', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CREATE_ITEM', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EDIT_ITEM', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INCREMENT_SPRINT', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ADD_USER', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REMOVE_USER', index=5, number=5,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=327,
  serialized_end=440,
)
_sym_db.RegisterEnumDescriptor(_PAYLOAD_ACTION)


_PAYLOAD = _descriptor.Descriptor(
  name='Payload',
  full_name='Payload',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='action', full_name='Payload.action', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='Payload.timestamp', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create_project', full_name='Payload.create_project', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create_item', full_name='Payload.create_item', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='edit_item', full_name='Payload.edit_item', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='increment_sprint', full_name='Payload.increment_sprint', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='add_user', full_name='Payload.add_user', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='remove_user', full_name='Payload.remove_user', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PAYLOAD_ACTION,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=440,
)


_CREATEPROJECTACTION = _descriptor.Descriptor(
  name='CreateProjectAction',
  full_name='CreateProjectAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='project_name', full_name='CreateProjectAction.project_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=442,
  serialized_end=485,
)


_CREATEITEMACTION = _descriptor.Descriptor(
  name='CreateItemAction',
  full_name='CreateItemAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=487,
  serialized_end=505,
)


_EDITITEMACTION = _descriptor.Descriptor(
  name='EditItemAction',
  full_name='EditItemAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=507,
  serialized_end=523,
)


_INCREMENTSPRINTACTION = _descriptor.Descriptor(
  name='IncrementSprintAction',
  full_name='IncrementSprintAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=525,
  serialized_end=548,
)


_ADDUSERACTION = _descriptor.Descriptor(
  name='AddUserAction',
  full_name='AddUserAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=550,
  serialized_end=565,
)


_REMOVEUSERACTION = _descriptor.Descriptor(
  name='RemoveUserAction',
  full_name='RemoveUserAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=567,
  serialized_end=585,
)

_PAYLOAD.fields_by_name['action'].enum_type = _PAYLOAD_ACTION
_PAYLOAD.fields_by_name['create_project'].message_type = _CREATEPROJECTACTION
_PAYLOAD.fields_by_name['create_item'].message_type = _CREATEITEMACTION
_PAYLOAD.fields_by_name['edit_item'].message_type = _EDITITEMACTION
_PAYLOAD.fields_by_name['increment_sprint'].message_type = _INCREMENTSPRINTACTION
_PAYLOAD.fields_by_name['add_user'].message_type = _ADDUSERACTION
_PAYLOAD.fields_by_name['remove_user'].message_type = _REMOVEUSERACTION
_PAYLOAD_ACTION.containing_type = _PAYLOAD
DESCRIPTOR.message_types_by_name['Payload'] = _PAYLOAD
DESCRIPTOR.message_types_by_name['CreateProjectAction'] = _CREATEPROJECTACTION
DESCRIPTOR.message_types_by_name['CreateItemAction'] = _CREATEITEMACTION
DESCRIPTOR.message_types_by_name['EditItemAction'] = _EDITITEMACTION
DESCRIPTOR.message_types_by_name['IncrementSprintAction'] = _INCREMENTSPRINTACTION
DESCRIPTOR.message_types_by_name['AddUserAction'] = _ADDUSERACTION
DESCRIPTOR.message_types_by_name['RemoveUserAction'] = _REMOVEUSERACTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Payload = _reflection.GeneratedProtocolMessageType('Payload', (_message.Message,), dict(
  DESCRIPTOR = _PAYLOAD,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:Payload)
  ))
_sym_db.RegisterMessage(Payload)

CreateProjectAction = _reflection.GeneratedProtocolMessageType('CreateProjectAction', (_message.Message,), dict(
  DESCRIPTOR = _CREATEPROJECTACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:CreateProjectAction)
  ))
_sym_db.RegisterMessage(CreateProjectAction)

CreateItemAction = _reflection.GeneratedProtocolMessageType('CreateItemAction', (_message.Message,), dict(
  DESCRIPTOR = _CREATEITEMACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:CreateItemAction)
  ))
_sym_db.RegisterMessage(CreateItemAction)

EditItemAction = _reflection.GeneratedProtocolMessageType('EditItemAction', (_message.Message,), dict(
  DESCRIPTOR = _EDITITEMACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:EditItemAction)
  ))
_sym_db.RegisterMessage(EditItemAction)

IncrementSprintAction = _reflection.GeneratedProtocolMessageType('IncrementSprintAction', (_message.Message,), dict(
  DESCRIPTOR = _INCREMENTSPRINTACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:IncrementSprintAction)
  ))
_sym_db.RegisterMessage(IncrementSprintAction)

AddUserAction = _reflection.GeneratedProtocolMessageType('AddUserAction', (_message.Message,), dict(
  DESCRIPTOR = _ADDUSERACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:AddUserAction)
  ))
_sym_db.RegisterMessage(AddUserAction)

RemoveUserAction = _reflection.GeneratedProtocolMessageType('RemoveUserAction', (_message.Message,), dict(
  DESCRIPTOR = _REMOVEUSERACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:RemoveUserAction)
  ))
_sym_db.RegisterMessage(RemoveUserAction)


# @@protoc_insertion_point(module_scope)