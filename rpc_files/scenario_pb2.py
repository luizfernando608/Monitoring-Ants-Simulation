# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scenario.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0escenario.proto\"\x19\n\x02ID\x12\x13\n\x0bscenario_id\x18\x01 \x01(\x05\"b\n\x06Report\x12\x0f\n\x07\x65lapsed\x18\x01 \x01(\x01\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x12\n\ntotal_food\x18\x03 \x01(\x05\x12\x10\n\x08map_food\x18\x04 \x01(\x05\x12\x11\n\tants_info\x18\x05 \x01(\t2/\n\nSimulation\x12!\n\rRunSimulation\x12\x03.ID\x1a\x07.Report\"\x00\x30\x01\x62\x06proto3')



_ID = DESCRIPTOR.message_types_by_name['ID']
_REPORT = DESCRIPTOR.message_types_by_name['Report']
ID = _reflection.GeneratedProtocolMessageType('ID', (_message.Message,), {
  'DESCRIPTOR' : _ID,
  '__module__' : 'scenario_pb2'
  # @@protoc_insertion_point(class_scope:ID)
  })
_sym_db.RegisterMessage(ID)

Report = _reflection.GeneratedProtocolMessageType('Report', (_message.Message,), {
  'DESCRIPTOR' : _REPORT,
  '__module__' : 'scenario_pb2'
  # @@protoc_insertion_point(class_scope:Report)
  })
_sym_db.RegisterMessage(Report)

_SIMULATION = DESCRIPTOR.services_by_name['Simulation']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ID._serialized_start=18
  _ID._serialized_end=43
  _REPORT._serialized_start=45
  _REPORT._serialized_end=143
  _SIMULATION._serialized_start=145
  _SIMULATION._serialized_end=192
# @@protoc_insertion_point(module_scope)