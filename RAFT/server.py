import raft_pb2_grpc
import raft_pb2
import grpc
import random
import json
import time
import math
from client import Client

class Server():

    def __init__(self,id):
        print("[SERVER] INFO : Server() init")
        self.id = id
        self.status = "F"
        self.leader = -1
        self.timeout = random.randint(1000,5000)/1000
        self.votes = 0
        self.clients = {}
        self.clientMap = {}
        self.voted = False
        self.data = None
        self.connect_neighbours()
                
        with open('config.json') as f:
            self.data = json.load(f)
        # self.connect_neighbours()
        # print(self.get_client_map())
        #print(self.get_client_map().items())


    def setLeader(self,leaderId):
        print("[SERVER] INFO : Setting leader for server: ",self.id," leaderId: ", leaderId)
        try:
            if leaderId:
                leaderId = int(leaderId)
                self.leader = leaderId
        except Exception as e:
            print("[SERVER] ERROR : Setting leader failed. Exception: ",e)
    
    def getLeader(self):
        print("[SERVER] INFO : Fetch current leader: ", self.leader)
        if self.leader:
            return int(self.leader)
        else:
            return -1
            
    
    def is_leader(self):
        print("[SERVER] INFO : Is Current node: ",self.id," leader? ", (int(self.leader) == int(self.id)))
        return int(self.leader) == int(self.id)
        
    def requestVote(self):
        print("[SERVER] INFO : Request vote to connected clients")
        try:
            self.status = "C"
            self.votes = 1
            for k in self.get_client_map().items():
                c = self.get_client(k[0])
                if not c:
                    continue
                id = k[0]
                if id == self.id:
                    continue
                print("[SERVER] INFO : Requesting vote to client id: ", id)
                if (c.requestVote()).result:
                    print("[SERVER] INFO : Secured vote from client id: ", id)
                    self.votes+=1
            active_nodes = int(self.getActiveNodes())
            print("[SERVER] INFO : Active nodes: ", active_nodes, " active nodes: ", self.active_nodes)
            if self.votes >= math.ceil((active_nodes+1)/2):
                print("[SERVER] INFO : Won majority votes: ", self.votes, " active nodes: ", self.active_nodes)
                return True
            else:
                return False
        except Exception as e:
            print("[SERVER] ERROR : Request vote failed. Exception: ",e)
            return False
    
    def get_client_map(self):
        print("[SERVER] INFO : Fetch client map")
        try:
            if self.clientMap:
                return self.clientMap
            if self.data:
                for d in self.data["client_map"]:
                    self.clientMap[str(d)] = self.data["client_map"][str(d)]  #HERE IS WHERE CODE IS SHITTING!
            return self.clientMap
        except Exception as e:
            print("[SERVER] ERROR : Fetch client map failed. Exception: ",e)
            return self.clientMap

    def get_client(self, clientID):
        print("[SERVER] INFO : Fetch client: ", clientID)
        try:
            clientID = int(clientID)
            client_obj = self.clients[str(clientID)]['client_obj']
            print("[SERVER] INFO : Fetched client object: ", client_obj)
            if client_obj is None or self.clients[str(clientID)]['active'] ==False:
                print("[SERVER] INFO : Fetched client, Connection does not exisit. Trying to connect.")
                try:
                    client_obj = Client(self.clients[str(clientID)]['host'])
                    if client_obj.ping().result:
                        print("[SERVER] INFO : Fetched client, Connection successful.")
                        self.clients[str(clientID)]['client_obj'] = client_obj
                        self.clients[str(clientID)]['active'] = True
                    else:
                        raise
                except Exception as e:
                    print("[SERVER] INFO : Fetched client, connection Failed. Exception: ",e)
                    return None
            else:
                try:
                    print("[SERVER] INFO : Fetched client, Connection exisit. Trying to connect.")
                    self.clients[str(clientID)]['client_obj'] = None
                    self.clients[str(clientID)]['active'] = False
                    if client_obj.ping().result:
                        print("[SERVER] INFO : Fetched client, Connection verified.")
                        self.clients[str(clientID)]['client_obj'] = client_obj
                        self.clients[str(clientID)]['active'] = True
                    else:
                        print("[SERVER] INFO : Fetched client, Connection failed. Creating new connection")
                        client_obj = Client(self.clients[str(clientID)]['host'])
                        if client_obj.ping().result:
                            print("[SERVER] INFO : Fetched client, Connection created.")
                            self.clients[str(clientID)]['client_obj'] = client_obj
                            self.clients[str(clientID)]['active'] = True
                except Exception as e:
                    print("[SERVER] ERROR : Fetched client, Connection exisit still failed. Exception: ",e)
                    return None
            return client_obj
        except Exception as e:
            print("[SERVER] ERROR : Get client failed. Exception: ",e)
            return None

    def getActiveNodes(self):
        print("[SERVER] INFO : Fetch active nodes count")
        try:
            count = 0
            for k in self.get_client_map().items():
                if self.get_client(k[0]):
                    count+=1
            print("[SERVER] INFO : Active node count: ", count)
            return count
        except Exception as e:
            print("[SERVER] ERROR : Fetch active nodes count failed. Exception: ",e)
            return 0
        
    def giveVote(self):
        print("[SERVER] INFO : Give vote ", self.id)
        try:
            if self.leader:
                print("[SERVER] INFO : Leader already defined ", self.leader," . Trying to connect.")
                leader_client = self.get_client(self.leader)
                if leader_client and leader_client.ping().result:
                    print("[SERVER] INFO : Leader already defined ", self.leader," . Connection successful. No vote")
                    return False
            if self.status in ("L","C") or self.voted:
                print("[SERVER] INFO : Current node already Leader or Candidate. ", self.status, ". No vote")
                return False
            self.voted = True
            print("[SERVER] INFO : Current node gave successfull vote")
            return True
        except Exception as e:
            print("[SERVER] ERROR : Give vote failed. Exception: ",e)
            return False

    def connect_neighbours(self):  
        print("[SERVER] INFO : Connecting neighbours")
        try:
            for v in self.get_client_map().items():
                node_details = v[1]
                try:
                    print("[SERVER] INFO : Connection attempt to: ", node_details)
                    c = Client(node_details)
                    if c.ping().result:
                        print("[SERVER] INFO : Connection successfull to: ", node_details)
                        self.clients[str(v[0])] = {'client_obj':c,'active':True,'host':node_details}
                    else:
                        raise
                except:
                    print("[SERVER] INFO : Connection attempt to: ", node_details, ". Failed")
                    self.clients[str(v[0])] = {'client_obj':None,'active':False,'host':node_details}
        except Exception as e:
            print("[SERVER] ERROR : Connecting neighbours failed. Exception: ",e)

    def broadCastLeader(self):
        print("[SERVER] INFO : Broadcast leader: ", self.leader," to nighbours")
        try:
            for k in self.get_client_map().values():
                if k["client_obj"] is None:
                    continue
                try:
                    print("[SERVER] INFO : Broadcast leader to: ", k["host"])
                    k["client_obj"].setLeader(self.leader)
                except Exception as e:
                    print("[SERVER] ERROR : Broadcast leader to: ", k["host"]," falied")
        except Exception as e:
            print("[SERVER] ERROR : Broadcast leader to nighbours failed. Exception: ",e)
        

    def getLeaderNode(self):
        print("[SERVER] INFO : Get leader node")
        try:
            if int(self.leader) and int(self.leader) != -1:
                print("[SERVER] INFO : Get leader node: Leader already defined")
                if int(self.leader) == int(self.id):
                    print("[SERVER] INFO : Get leader node: I am the leader")
                    return int(self.leader)
                print("[SERVER] INFO : Get leader node: Trying to connect with leader")
                leader_client = self.get_client(self.leader)
                try:
                    if leader_client is None or not leader_client.ping().result:
                        raise
                    print("[SERVER] INFO : Get leader node: Connection to leader successful")
                except:
                    print("[SERVER] INFO : Leader not reachable. START ELECTION")
                    try:
                        leader_id = self.start_election()
                        print("[SERVER] INFO : New leader elected: ", leader_id)
                        self.setLeader(int(leader_id))
                    except Exception as e:
                        print("[SERVER] ERROR : New leader elected failed. Exception: ",e)
                return self.leader
            else:
                print("[SERVER] INFO : Get leader node: Leader not defined, Checking with cluster for leader")
                leader_id = self.checkClusterForLeader()
                print("[SERVER] INFO : Get leader node: Other leader in cluster: ", leader_id)
                if leader_id == -1:
                    try:
                        print("[SERVER] INFO : Invalid leader. START ELECTION")
                        leader_id = self.start_election()
                        print("[SERVER] INFO : New leader elected: ", leader_id)
                    except Exception as e:
                        print("[SERVER] ERROR : New leader elected failed. Exception: ",e)
            self.setLeader(int(leader_id))
            return self.leader
        except Exception as e:
            print("[SERVER] ERROR : Get leader node failed. Exception: ",e)
            return self.leader
        
        # try:
        #     if self.leader and int(self.leader) != -1:
        #         # print("Server - Leader Already Defined")
        #         if int(self.leader)==int(self.id):
        #             # print("Server - I am already leader")
        #             return int(self.leader)
        #         leader_client = self.get_client(int(self.leader))
        #         print("qqqqqqq",leader_client)
        #         try:
        #             if leader_client is None or not leader_client.ping().result:
        #                 raise
        #         except:
        #             print("Server - Leader not reachable")
        #             leader_id = int(self.start_election())
        #             self.setLeader(leader_id)
        #         return int(self.leader)
        #     else:
        #         print("Server - No Leader Defined")
        #         leader_id = int(self.checkClusterForLeader())
        #         print("Server - Leaders in cluserter", leader_id)
        #         if leader_id == -1:
        #             print("Server - Election")
        #             leader_id = int(self.start_election())
        #     print("Server - Setting Leader", leader_id)
        #     self.setLeader(int(leader_id))
        #     return int(self.leader)
        # except Exception as e:
        #     print("SERVER - getLeaderNode ",e)
        #     return -1
        
                    


    def checkClusterForLeader(self):
        print("[SERVER] INFO : Checking cluster for leader")
        try:
            for k in self.get_client_map().items():
                c = self.get_client(k[0])
                if not c:
                    continue
                print("[SERVER] INFO : Checking node: ", c)
                status = c.getClientStatus()
                if(status.is_leader):
                    print("[SERVER] INFO : Leader found: ", c," Trying to connect")
                    leader_node = status.leader_id
                    leader_client = self.get_client(leader_node)
                    if leader_client.ping().result:
                        print("[SERVER] INFO : Leader connection successfull")
                        return int(leader_node)
                    else:
                        print("[SERVER] INFO : Leader connection failed")
        except Exception as e:
            print("[SERVER] ERROR : Checking cluster for leader failed. Exception: ",e)
        return -1

    def start_election(self):
        print("[SERVER] INFO : Starting election")
        try:
            while(True):
                time.sleep(self.timeout)
                print("[SERVER] INFO : Requesting vote")
                try:
                    if self.requestVote():
                        print("[SERVER] INFO : Won election")
                        self.setLeader(self.id)
                        self.votes = 0
                        self.status = "L"
                        print("[SERVER] INFO : Broadcasting leader to other nodes")
                        try:
                            self.broadCastLeader()
                        except Exception as e:
                            print("[SERVER] ERROR : Broadcast leader failed. Exception: ",e)
                            raise
                        return int(self.leader)
                    else:
                        print("[SERVER] INFO : Did not win the election. Checking who won.")
                        try:
                            leader_node = self.checkClusterForLeader()
                        except Exception as e:
                            print("[SERVER] ERROR : Checking cluster for leader failed. Exception: ",e)
                            raise
                        print("[SERVER] INFO : Election winner: ", leader_node)
                        if self.leader>0:
                            print("[SERVER] INFO : Setting new leader: ", leader_node)
                            self.status = "F"
                            self.setLeader(leader_node)
                            return int(self.leader)
                        else:
                            print("[SERVER] INFO : New leader invalid: ", self.leader)
                        self.timeout = random.randint(1000,5000)/1000
                except Exception as e:
                    print("[SERVER] ERROR : Request vote failed. Exception: ",e)
                    return int(self.leader)
        except Exception as e:
            print("[SERVER] ERROR : Checking cluster for leader failed. Exception: ",e)
            return int(self.leader)
        

# if __name__ == "__main__":
#     s = Server(3)
#     s.broadCastLeader()