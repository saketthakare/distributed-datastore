# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import sample_pb2 as sample__pb2


class RAFTStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.ping = channel.unary_unary(
        '/leaderProto.RAFT/ping',
        request_serializer=sample__pb2.Node.SerializeToString,
        response_deserializer=sample__pb2.BoolResponse.FromString,
        )
    self.setLeader = channel.unary_unary(
        '/leaderProto.RAFT/setLeader',
        request_serializer=sample__pb2.Node.SerializeToString,
        response_deserializer=sample__pb2.BoolResponse.FromString,
        )
    self.requestVote = channel.unary_unary(
        '/leaderProto.RAFT/requestVote',
        request_serializer=sample__pb2.Node.SerializeToString,
        response_deserializer=sample__pb2.BoolResponse.FromString,
        )
    self.getLeader = channel.unary_unary(
        '/leaderProto.RAFT/getLeader',
        request_serializer=sample__pb2.Node.SerializeToString,
        response_deserializer=sample__pb2.Node.FromString,
        )


class RAFTServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def ping(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def setLeader(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def requestVote(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getLeader(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_RAFTServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ping': grpc.unary_unary_rpc_method_handler(
          servicer.ping,
          request_deserializer=sample__pb2.Node.FromString,
          response_serializer=sample__pb2.BoolResponse.SerializeToString,
      ),
      'setLeader': grpc.unary_unary_rpc_method_handler(
          servicer.setLeader,
          request_deserializer=sample__pb2.Node.FromString,
          response_serializer=sample__pb2.BoolResponse.SerializeToString,
      ),
      'requestVote': grpc.unary_unary_rpc_method_handler(
          servicer.requestVote,
          request_deserializer=sample__pb2.Node.FromString,
          response_serializer=sample__pb2.BoolResponse.SerializeToString,
      ),
      'getLeader': grpc.unary_unary_rpc_method_handler(
          servicer.getLeader,
          request_deserializer=sample__pb2.Node.FromString,
          response_serializer=sample__pb2.Node.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'leaderProto.RAFT', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
