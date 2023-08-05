# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from biostarPython.service import status_pb2 as status__pb2


class StatusStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetConfig = channel.unary_unary(
        '/status.Status/GetConfig',
        request_serializer=status__pb2.GetConfigRequest.SerializeToString,
        response_deserializer=status__pb2.GetConfigResponse.FromString,
        )
    self.SetConfig = channel.unary_unary(
        '/status.Status/SetConfig',
        request_serializer=status__pb2.SetConfigRequest.SerializeToString,
        response_deserializer=status__pb2.SetConfigResponse.FromString,
        )
    self.SetConfigMulti = channel.unary_unary(
        '/status.Status/SetConfigMulti',
        request_serializer=status__pb2.SetConfigMultiRequest.SerializeToString,
        response_deserializer=status__pb2.SetConfigMultiResponse.FromString,
        )


class StatusServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetConfig(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetConfig(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetConfigMulti(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_StatusServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetConfig': grpc.unary_unary_rpc_method_handler(
          servicer.GetConfig,
          request_deserializer=status__pb2.GetConfigRequest.FromString,
          response_serializer=status__pb2.GetConfigResponse.SerializeToString,
      ),
      'SetConfig': grpc.unary_unary_rpc_method_handler(
          servicer.SetConfig,
          request_deserializer=status__pb2.SetConfigRequest.FromString,
          response_serializer=status__pb2.SetConfigResponse.SerializeToString,
      ),
      'SetConfigMulti': grpc.unary_unary_rpc_method_handler(
          servicer.SetConfigMulti,
          request_deserializer=status__pb2.SetConfigMultiRequest.FromString,
          response_serializer=status__pb2.SetConfigMultiResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'status.Status', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
