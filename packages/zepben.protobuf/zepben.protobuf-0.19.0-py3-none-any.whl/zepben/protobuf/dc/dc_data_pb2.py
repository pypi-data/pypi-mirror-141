# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/dc/dc-data.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from zepben.protobuf.cim.iec61970.base.diagramlayout import Diagram_pb2 as zepben_dot_protobuf_dot_cim_dot_iec61970_dot_base_dot_diagramlayout_dot_Diagram__pb2
from zepben.protobuf.cim.iec61970.base.diagramlayout import DiagramObject_pb2 as zepben_dot_protobuf_dot_cim_dot_iec61970_dot_base_dot_diagramlayout_dot_DiagramObject__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n zepben/protobuf/dc/dc-data.proto\x12\x12zepben.protobuf.dc\x1a\x19google/protobuf/any.proto\x1a=zepben/protobuf/cim/iec61970/base/diagramlayout/Diagram.proto\x1a\x43zepben/protobuf/cim/iec61970/base/diagramlayout/DiagramObject.proto\"\xfb\x01\n\x17\x44iagramIdentifiedObject\x12K\n\x07\x64iagram\x18\x01 \x01(\x0b\x32\x38.zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramH\x00\x12W\n\rdiagramObject\x18\x02 \x01(\x0b\x32>.zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObjectH\x00\x12&\n\x05other\x18\xe7\x07 \x01(\x0b\x32\x14.google.protobuf.AnyH\x00\x42\x12\n\x10identifiedObjectB/\n\x16\x63om.zepben.protobuf.dcP\x01\xaa\x02\x12Zepben.Protobuf.DCb\x06proto3')



_DIAGRAMIDENTIFIEDOBJECT = DESCRIPTOR.message_types_by_name['DiagramIdentifiedObject']
DiagramIdentifiedObject = _reflection.GeneratedProtocolMessageType('DiagramIdentifiedObject', (_message.Message,), {
  'DESCRIPTOR' : _DIAGRAMIDENTIFIEDOBJECT,
  '__module__' : 'zepben.protobuf.dc.dc_data_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.dc.DiagramIdentifiedObject)
  })
_sym_db.RegisterMessage(DiagramIdentifiedObject)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\026com.zepben.protobuf.dcP\001\252\002\022Zepben.Protobuf.DC'
  _DIAGRAMIDENTIFIEDOBJECT._serialized_start=216
  _DIAGRAMIDENTIFIEDOBJECT._serialized_end=467
# @@protoc_insertion_point(module_scope)
