# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from zepben.protobuf.cc import cc_requests_pb2 as zepben_dot_protobuf_dot_cc_dot_cc__requests__pb2
from zepben.protobuf.cc import cc_responses_pb2 as zepben_dot_protobuf_dot_cc_dot_cc__responses__pb2


class CustomerConsumerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getIdentifiedObjects = channel.stream_stream(
                '/zepben.protobuf.cc.CustomerConsumer/getIdentifiedObjects',
                request_serializer=zepben_dot_protobuf_dot_cc_dot_cc__requests__pb2.GetIdentifiedObjectsRequest.SerializeToString,
                response_deserializer=zepben_dot_protobuf_dot_cc_dot_cc__responses__pb2.GetIdentifiedObjectsResponse.FromString,
                )


class CustomerConsumerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def getIdentifiedObjects(self, request_iterator, context):
        """Get identified objects
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CustomerConsumerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'getIdentifiedObjects': grpc.stream_stream_rpc_method_handler(
                    servicer.getIdentifiedObjects,
                    request_deserializer=zepben_dot_protobuf_dot_cc_dot_cc__requests__pb2.GetIdentifiedObjectsRequest.FromString,
                    response_serializer=zepben_dot_protobuf_dot_cc_dot_cc__responses__pb2.GetIdentifiedObjectsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'zepben.protobuf.cc.CustomerConsumer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CustomerConsumer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def getIdentifiedObjects(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/zepben.protobuf.cc.CustomerConsumer/getIdentifiedObjects',
            zepben_dot_protobuf_dot_cc_dot_cc__requests__pb2.GetIdentifiedObjectsRequest.SerializeToString,
            zepben_dot_protobuf_dot_cc_dot_cc__responses__pb2.GetIdentifiedObjectsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
