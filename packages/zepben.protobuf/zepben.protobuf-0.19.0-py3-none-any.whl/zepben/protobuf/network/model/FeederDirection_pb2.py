# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/network/model/FeederDirection.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3zepben/protobuf/network/model/FeederDirection.proto\x12\x1dzepben.protobuf.network.model*C\n\x0f\x46\x65\x65\x64\x65rDirection\x12\x08\n\x04NONE\x10\x00\x12\x0c\n\x08UPSTREAM\x10\x01\x12\x0e\n\nDOWNSTREAM\x10\x02\x12\x08\n\x04\x42OTH\x10\x03\x42\x45\n!com.zepben.protobuf.network.modelP\x01\xaa\x02\x1dZepben.Protobuf.Network.Modelb\x06proto3')

_FEEDERDIRECTION = DESCRIPTOR.enum_types_by_name['FeederDirection']
FeederDirection = enum_type_wrapper.EnumTypeWrapper(_FEEDERDIRECTION)
NONE = 0
UPSTREAM = 1
DOWNSTREAM = 2
BOTH = 3


if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n!com.zepben.protobuf.network.modelP\001\252\002\035Zepben.Protobuf.Network.Model'
  _FEEDERDIRECTION._serialized_start=86
  _FEEDERDIRECTION._serialized_end=153
# @@protoc_insertion_point(module_scope)
