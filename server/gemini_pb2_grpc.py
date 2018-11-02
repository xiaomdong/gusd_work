# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import gemini_pb2 as gemini__pb2


class geminiStub(object):
  """The greeting service definition.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.login = channel.unary_unary(
        '/server.gemini/login',
        request_serializer=gemini__pb2.loginRequest.SerializeToString,
        response_deserializer=gemini__pb2.loginReply.FromString,
        )
    self.register = channel.unary_unary(
        '/server.gemini/register',
        request_serializer=gemini__pb2.registerRequest.SerializeToString,
        response_deserializer=gemini__pb2.registerReply.FromString,
        )
    self.balance = channel.unary_unary(
        '/server.gemini/balance',
        request_serializer=gemini__pb2.balanceRequest.SerializeToString,
        response_deserializer=gemini__pb2.balanceReply.FromString,
        )
    self.info = channel.unary_unary(
        '/server.gemini/info',
        request_serializer=gemini__pb2.infoRequest.SerializeToString,
        response_deserializer=gemini__pb2.infoReply.FromString,
        )
    self.exchangeGUSD = channel.unary_unary(
        '/server.gemini/exchangeGUSD',
        request_serializer=gemini__pb2.exchangeGUSDRequest.SerializeToString,
        response_deserializer=gemini__pb2.exchangeGUSDReply.FromString,
        )
    self.exchangeUSD = channel.unary_unary(
        '/server.gemini/exchangeUSD',
        request_serializer=gemini__pb2.exchangeUSDRequest.SerializeToString,
        response_deserializer=gemini__pb2.exchangeUSDReply.FromString,
        )
    self.withdrawalUSD = channel.unary_unary(
        '/server.gemini/withdrawalUSD',
        request_serializer=gemini__pb2.withdrawalUSDRequest.SerializeToString,
        response_deserializer=gemini__pb2.withdrawalUSDReply.FromString,
        )
    self.withdrawalGUSD = channel.unary_unary(
        '/server.gemini/withdrawalGUSD',
        request_serializer=gemini__pb2.withdrawalGUSDRequest.SerializeToString,
        response_deserializer=gemini__pb2.withdrawalGUSDReply.FromString,
        )
    self.record = channel.unary_stream(
        '/server.gemini/record',
        request_serializer=gemini__pb2.recordRequest.SerializeToString,
        response_deserializer=gemini__pb2.recordReply.FromString,
        )


class geminiServicer(object):
  """The greeting service definition.
  """

  def login(self, request, context):
    """Sends a deposit
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def register(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def balance(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def info(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def exchangeGUSD(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def exchangeUSD(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def withdrawalUSD(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def withdrawalGUSD(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def record(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_geminiServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'login': grpc.unary_unary_rpc_method_handler(
          servicer.login,
          request_deserializer=gemini__pb2.loginRequest.FromString,
          response_serializer=gemini__pb2.loginReply.SerializeToString,
      ),
      'register': grpc.unary_unary_rpc_method_handler(
          servicer.register,
          request_deserializer=gemini__pb2.registerRequest.FromString,
          response_serializer=gemini__pb2.registerReply.SerializeToString,
      ),
      'balance': grpc.unary_unary_rpc_method_handler(
          servicer.balance,
          request_deserializer=gemini__pb2.balanceRequest.FromString,
          response_serializer=gemini__pb2.balanceReply.SerializeToString,
      ),
      'info': grpc.unary_unary_rpc_method_handler(
          servicer.info,
          request_deserializer=gemini__pb2.infoRequest.FromString,
          response_serializer=gemini__pb2.infoReply.SerializeToString,
      ),
      'exchangeGUSD': grpc.unary_unary_rpc_method_handler(
          servicer.exchangeGUSD,
          request_deserializer=gemini__pb2.exchangeGUSDRequest.FromString,
          response_serializer=gemini__pb2.exchangeGUSDReply.SerializeToString,
      ),
      'exchangeUSD': grpc.unary_unary_rpc_method_handler(
          servicer.exchangeUSD,
          request_deserializer=gemini__pb2.exchangeUSDRequest.FromString,
          response_serializer=gemini__pb2.exchangeUSDReply.SerializeToString,
      ),
      'withdrawalUSD': grpc.unary_unary_rpc_method_handler(
          servicer.withdrawalUSD,
          request_deserializer=gemini__pb2.withdrawalUSDRequest.FromString,
          response_serializer=gemini__pb2.withdrawalUSDReply.SerializeToString,
      ),
      'withdrawalGUSD': grpc.unary_unary_rpc_method_handler(
          servicer.withdrawalGUSD,
          request_deserializer=gemini__pb2.withdrawalGUSDRequest.FromString,
          response_serializer=gemini__pb2.withdrawalGUSDReply.SerializeToString,
      ),
      'record': grpc.unary_stream_rpc_method_handler(
          servicer.record,
          request_deserializer=gemini__pb2.recordRequest.FromString,
          response_serializer=gemini__pb2.recordReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'server.gemini', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
