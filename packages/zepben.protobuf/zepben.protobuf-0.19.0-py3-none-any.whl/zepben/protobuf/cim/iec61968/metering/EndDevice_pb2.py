# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/cim/iec61968/metering/EndDevice.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.protobuf.cim.iec61968.assets import AssetContainer_pb2 as zepben_dot_protobuf_dot_cim_dot_iec61968_dot_assets_dot_AssetContainer__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n5zepben/protobuf/cim/iec61968/metering/EndDevice.proto\x12%zepben.protobuf.cim.iec61968.metering\x1a\x38zepben/protobuf/cim/iec61968/assets/AssetContainer.proto\"\x98\x01\n\tEndDevice\x12?\n\x02\x61\x63\x18\x01 \x01(\x0b\x32\x33.zepben.protobuf.cim.iec61968.assets.AssetContainer\x12\x17\n\x0fusagePointMRIDs\x18\x02 \x03(\t\x12\x14\n\x0c\x63ustomerMRID\x18\x03 \x01(\t\x12\x1b\n\x13serviceLocationMRID\x18\x04 \x01(\tBU\n)com.zepben.protobuf.cim.iec61968.meteringP\x01\xaa\x02%Zepben.Protobuf.CIM.IEC61968.Meteringb\x06proto3')



_ENDDEVICE = DESCRIPTOR.message_types_by_name['EndDevice']
EndDevice = _reflection.GeneratedProtocolMessageType('EndDevice', (_message.Message,), {
  'DESCRIPTOR' : _ENDDEVICE,
  '__module__' : 'zepben.protobuf.cim.iec61968.metering.EndDevice_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.cim.iec61968.metering.EndDevice)
  })
_sym_db.RegisterMessage(EndDevice)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n)com.zepben.protobuf.cim.iec61968.meteringP\001\252\002%Zepben.Protobuf.CIM.IEC61968.Metering'
  _ENDDEVICE._serialized_start=155
  _ENDDEVICE._serialized_end=307
# @@protoc_insertion_point(module_scope)
