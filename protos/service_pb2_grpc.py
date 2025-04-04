# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from protos import recognize_ingredients_pb2 as protos_dot_recognize__ingredients__pb2
from protos import select_ingredient_pb2 as protos_dot_select__ingredient__pb2

GRPC_GENERATED_VERSION = '1.68.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in protos/service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class IngredientRecognitionServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RecognizeIngredientsStream = channel.stream_unary(
                '/IngredientRecognitionService/RecognizeIngredientsStream',
                request_serializer=protos_dot_recognize__ingredients__pb2.RecognizeIngredientsStreamRequest.SerializeToString,
                response_deserializer=protos_dot_recognize__ingredients__pb2.RecognizeIngredientsResponse.FromString,
                _registered_method=True)
        self.SelectIngredientStream = channel.stream_stream(
                '/IngredientRecognitionService/SelectIngredientStream',
                request_serializer=protos_dot_select__ingredient__pb2.SelectIngredientStreamRequest.SerializeToString,
                response_deserializer=protos_dot_select__ingredient__pb2.SelectIngredientStreamResponse.FromString,
                _registered_method=True)


class IngredientRecognitionServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RecognizeIngredientsStream(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SelectIngredientStream(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_IngredientRecognitionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RecognizeIngredientsStream': grpc.stream_unary_rpc_method_handler(
                    servicer.RecognizeIngredientsStream,
                    request_deserializer=protos_dot_recognize__ingredients__pb2.RecognizeIngredientsStreamRequest.FromString,
                    response_serializer=protos_dot_recognize__ingredients__pb2.RecognizeIngredientsResponse.SerializeToString,
            ),
            'SelectIngredientStream': grpc.stream_stream_rpc_method_handler(
                    servicer.SelectIngredientStream,
                    request_deserializer=protos_dot_select__ingredient__pb2.SelectIngredientStreamRequest.FromString,
                    response_serializer=protos_dot_select__ingredient__pb2.SelectIngredientStreamResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'IngredientRecognitionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('IngredientRecognitionService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class IngredientRecognitionService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RecognizeIngredientsStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(
            request_iterator,
            target,
            '/IngredientRecognitionService/RecognizeIngredientsStream',
            protos_dot_recognize__ingredients__pb2.RecognizeIngredientsStreamRequest.SerializeToString,
            protos_dot_recognize__ingredients__pb2.RecognizeIngredientsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SelectIngredientStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            '/IngredientRecognitionService/SelectIngredientStream',
            protos_dot_select__ingredient__pb2.SelectIngredientStreamRequest.SerializeToString,
            protos_dot_select__ingredient__pb2.SelectIngredientStreamResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
