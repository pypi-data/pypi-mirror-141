# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/nm/set-switch-state-requests.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.protobuf.nm import set_switch_state_data_pb2 as zepben_dot_protobuf_dot_nm_dot_set__switch__state__data__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n2zepben/protobuf/nm/set-switch-state-requests.proto\x12\x12zepben.protobuf.nm\x1a.zepben/protobuf/nm/set-switch-state-data.proto\"s\n\x1dSetCurrentSwitchStatesRequest\x12\x11\n\tmessageId\x18\x01 \x01(\x03\x12?\n\x10switchesToUpdate\x18\x02 \x03(\x0b\x32%.zepben.protobuf.nm.SwitchStateUpdateB/\n\x16\x63om.zepben.protobuf.nmP\x01\xaa\x02\x12Zepben.Protobuf.NMb\x06proto3')



_SETCURRENTSWITCHSTATESREQUEST = DESCRIPTOR.message_types_by_name['SetCurrentSwitchStatesRequest']
SetCurrentSwitchStatesRequest = _reflection.GeneratedProtocolMessageType('SetCurrentSwitchStatesRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETCURRENTSWITCHSTATESREQUEST,
  '__module__' : 'zepben.protobuf.nm.set_switch_state_requests_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.nm.SetCurrentSwitchStatesRequest)
  })
_sym_db.RegisterMessage(SetCurrentSwitchStatesRequest)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\026com.zepben.protobuf.nmP\001\252\002\022Zepben.Protobuf.NM'
  _SETCURRENTSWITCHSTATESREQUEST._serialized_start=122
  _SETCURRENTSWITCHSTATESREQUEST._serialized_end=237
# @@protoc_insertion_point(module_scope)
