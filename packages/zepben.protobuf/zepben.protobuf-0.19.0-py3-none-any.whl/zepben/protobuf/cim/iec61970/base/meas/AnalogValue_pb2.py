# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/cim/iec61970/base/meas/AnalogValue.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.protobuf.cim.iec61970.base.meas import MeasurementValue_pb2 as zepben_dot_protobuf_dot_cim_dot_iec61970_dot_base_dot_meas_dot_MeasurementValue__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n8zepben/protobuf/cim/iec61970/base/meas/AnalogValue.proto\x12&zepben.protobuf.cim.iec61970.base.meas\x1a=zepben/protobuf/cim/iec61970/base/meas/MeasurementValue.proto\"v\n\x0b\x41nalogValue\x12\x44\n\x02mv\x18\x01 \x01(\x0b\x32\x38.zepben.protobuf.cim.iec61970.base.meas.MeasurementValue\x12\x12\n\nanalogMRID\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\x01\x42W\n*com.zepben.protobuf.cim.iec61970.base.measP\x01\xaa\x02&Zepben.Protobuf.CIM.IEC61970.Base.Measb\x06proto3')



_ANALOGVALUE = DESCRIPTOR.message_types_by_name['AnalogValue']
AnalogValue = _reflection.GeneratedProtocolMessageType('AnalogValue', (_message.Message,), {
  'DESCRIPTOR' : _ANALOGVALUE,
  '__module__' : 'zepben.protobuf.cim.iec61970.base.meas.AnalogValue_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.cim.iec61970.base.meas.AnalogValue)
  })
_sym_db.RegisterMessage(AnalogValue)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n*com.zepben.protobuf.cim.iec61970.base.measP\001\252\002&Zepben.Protobuf.CIM.IEC61970.Base.Meas'
  _ANALOGVALUE._serialized_start=163
  _ANALOGVALUE._serialized_end=281
# @@protoc_insertion_point(module_scope)
