# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/cim/iec61970/base/wires/ShuntCompensator.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.protobuf.cim.iec61970.base.wires import PhaseShuntConnectionKind_pb2 as zepben_dot_protobuf_dot_cim_dot_iec61970_dot_base_dot_wires_dot_PhaseShuntConnectionKind__pb2
from zepben.protobuf.cim.iec61970.base.wires import RegulatingCondEq_pb2 as zepben_dot_protobuf_dot_cim_dot_iec61970_dot_base_dot_wires_dot_RegulatingCondEq__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n>zepben/protobuf/cim/iec61970/base/wires/ShuntCompensator.proto\x12\'zepben.protobuf.cim.iec61970.base.wires\x1a\x46zepben/protobuf/cim/iec61970/base/wires/PhaseShuntConnectionKind.proto\x1a>zepben/protobuf/cim/iec61970/base/wires/RegulatingCondEq.proto\"\xed\x01\n\x10ShuntCompensator\x12\x46\n\x03rce\x18\x01 \x01(\x0b\x32\x39.zepben.protobuf.cim.iec61970.base.wires.RegulatingCondEq\x12\x10\n\x08sections\x18\x02 \x01(\x01\x12\x10\n\x08grounded\x18\x03 \x01(\x08\x12\x0c\n\x04nomU\x18\x04 \x01(\x05\x12_\n\x0fphaseConnection\x18\x05 \x01(\x0e\x32\x46.zepben.protobuf.cim.iec61970.base.wires.PhaseShuntConnectionKind.EnumBY\n+com.zepben.protobuf.cim.iec61970.base.wiresP\x01\xaa\x02\'Zepben.Protobuf.CIM.IEC61970.Base.Wiresb\x06proto3')



_SHUNTCOMPENSATOR = DESCRIPTOR.message_types_by_name['ShuntCompensator']
ShuntCompensator = _reflection.GeneratedProtocolMessageType('ShuntCompensator', (_message.Message,), {
  'DESCRIPTOR' : _SHUNTCOMPENSATOR,
  '__module__' : 'zepben.protobuf.cim.iec61970.base.wires.ShuntCompensator_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.cim.iec61970.base.wires.ShuntCompensator)
  })
_sym_db.RegisterMessage(ShuntCompensator)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n+com.zepben.protobuf.cim.iec61970.base.wiresP\001\252\002\'Zepben.Protobuf.CIM.IEC61970.Base.Wires'
  _SHUNTCOMPENSATOR._serialized_start=244
  _SHUNTCOMPENSATOR._serialized_end=481
# @@protoc_insertion_point(module_scope)
