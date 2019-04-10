import raft_pb2_grpc
import raft_pb2
import grpc
import json
import time

class Client():

    def __init__(self,host):
        # print("Client - Constructor called", host)
        self.host = host
        self.channel = grpc.insecure_channel(host) #'%s:%d' % (host, port)
        self.stub = raft_pb2_grpc.RAFTStub(self.channel)

    def setLeader(self,leaderId):
        req = (raft_pb2.RAFTStub(id=leaderId))
        print("[CLIENT] INFO : Set leader: ", req)
        return self.stub.setLeader(req)
    
    def getLeader(self):
        print("[CLIENT] INFO : Get leader invoked")
        return self.stub.getLeader(raft_pb2.Node(id=-1))
    
    def ping(self):
        print("[CLIENT] INFO : Ping invoked")
        return self.stub.ping(raft_pb2.Node(id=-1))
    
    def requestVote(self):
        print("[CLIENT] INFO : Request vote invoked")
        return self.stub.requestVote(raft_pb2.Node(id=-1))
    
    def getClientStatus(self):
        print("[CLIENT] INFO : Get client status invoked")
        return self.stub.getClientStatus(raft_pb2.Node(id=-1))
    
    def getLeaderNode(self):
        print("[CLIENT] INFO : Get leader node invoked")
        return self.stub.getLeaderNode(raft_pb2.Node(id=-1))
        
    

if __name__ == "__main__":
    data = ""
    with open('config.json') as f:
        data = json.load(f)

    if data["node_id"]:
        c = Client(data["client_map"][str(data["node_id"])])
    while(True):
        time.sleep(data["heart_beat_interval"])
        print("[CLIENT] INFO : Checking leader connection")
        try:
            c.getLeaderNode()
        except Exception as e:
            print("[CLIENT] INFO : Checking leader connection failed. Exception: ",e)
