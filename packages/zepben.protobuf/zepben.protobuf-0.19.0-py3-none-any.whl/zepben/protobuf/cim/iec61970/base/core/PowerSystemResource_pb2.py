# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/cim/iec61970/base/core/PowerSystemResource.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.protobuf.cim.iec61970.base.core import IdentifiedObject_pb2 as zepben_dot_protobuf_dot_cim_dot_iec61970_dot_base_dot_core_dot_IdentifiedObject__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n@zepben/protobuf/cim/iec61970/base/core/PowerSystemResource.proto\x12&zepben.protobuf.cim.iec61970.base.core\x1a=zepben/protobuf/cim/iec61970/base/core/IdentifiedObject.proto\"\x9d\x01\n\x13PowerSystemResource\x12\x44\n\x02io\x18\x01 \x01(\x0b\x32\x38.zepben.protobuf.cim.iec61970.base.core.IdentifiedObject\x12\x15\n\rassetInfoMRID\x18\x02 \x01(\t\x12\x14\n\x0clocationMRID\x18\x03 \x01(\t\x12\x13\n\x0bnumControls\x18\x04 \x01(\x05\x42W\n*com.zepben.protobuf.cim.iec61970.base.coreP\x01\xaa\x02&Zepben.Protobuf.CIM.IEC61970.Base.Coreb\x06proto3')



_POWERSYSTEMRESOURCE = DESCRIPTOR.message_types_by_name['PowerSystemResource']
PowerSystemResource = _reflection.GeneratedProtocolMessageType('PowerSystemResource', (_message.Message,), {
  'DESCRIPTOR' : _POWERSYSTEMRESOURCE,
  '__module__' : 'zepben.protobuf.cim.iec61970.base.core.PowerSystemResource_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.cim.iec61970.base.core.PowerSystemResource)
  })
_sym_db.RegisterMessage(PowerSystemResource)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n*com.zepben.protobuf.cim.iec61970.base.coreP\001\252\002&Zepben.Protobuf.CIM.IEC61970.Base.Core'
  _POWERSYSTEMRESOURCE._serialized_start=172
  _POWERSYSTEMRESOURCE._serialized_end=329
# @@protoc_insertion_point(module_scope)
