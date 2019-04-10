from concurrent import futures
import raft_pb2_grpc
import raft_pb2
import grpc
from server import Server
import time
import json

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
id = -1

class Handler(raft_pb2_grpc.RAFTStub):

    def __init__(self):
        self.node = Server(id)
        # print("[HANDLER] INFO : Connect Neighbours")
        # self.node.connect_neighbours()

    def ping(self,request,context):
        print("[HANDLER] INFO : Ping received")
        return raft_pb2.BoolResponse(result=True)
    
    def setLeader(self,request,context):
        print("[HANDLER] INFO : Set leader: ", request.id)
        self.node.leader = request.id
        self.node.voted = False
        return raft_pb2.BoolResponse(result=True)
    
    def getLeader(self,request, context):
        leader_node = self.node.getLeader()
        leader_node = int(leader_node)
        print("[HANDLER] INFO : get leader: ", leader_node)
        return raft_pb2.Node(id=leader_node)

    def requestVote(self,request,context):
        res = self.node.giveVote()
        print("[HANDLER] INFO : Give vote?: ", res)
        return raft_pb2.BoolResponse(result=True)

    def getClientStatus(self,request,context):
        nodeId = int(self.node.id)
        nodeLeaderId = int(self.node.getLeaderNode())
        print("[HANDLER] INFO : Get client status: id:", nodeId," leaderId:", nodeLeaderId)
        return raft_pb2.ClientStatus(id= nodeId, is_leader = self.node.is_leader(),leader_id = nodeLeaderId)

    def getLeaderNode(self,request, context):
        leader_node = self.node.getLeaderNode()
        print("[HANDLER] INFO : Get leader node", leader_node)
        if leader_node is not None:
            leader_node = int(leader_node)
        else:
            leader_node=-1
        print("[SERVER] INFO : CURRENT LEADER NODE", leader_node)
        return raft_pb2.Node(id=leader_node)


if __name__ == "__main__":
    
    data = None
    with open('config.json') as f:
        data = json.load(f)

    id = str(data["node_id"])
    ip_address = data["client_map"][id]
    if data is not None:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        raft_pb2_grpc.add_RAFTServicer_to_server(Handler(), server)
        server.add_insecure_port(ip_address)
        server.start()
        print("[HANDLER] INFO : SERVER STARTED")
        # server.node.connect_neighbours()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            print("[HANDLER] INFO : SERVER STOPPED")
            server.stop(0)