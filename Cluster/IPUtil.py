import json
class IPUtil():

    def __init__(self):
        self.jsonData = {}
        self.readJSON()

    def getServerPort(self):
        return str(3000)
    
    def getElectionPort(self):
        return str(2000)

    def readJSON(self):
        with open("valid_ip.json", "r") as f:
            self.jsonData = json.load(f)
        #print(self.jsonData)
    
    def getSelf(self):
        if self.jsonData and self.jsonData["node_id"]:
            for i in self.jsonData["client_map"]:
                if int(i)==int(self.jsonData["node_id"]):
                    return self.jsonData["client_map"][i]["ip"]
        return -1
    
    def getSelfForServer(self):
        if self.jsonData and self.jsonData["node_id"]:
            for i in self.jsonData["client_map"]:
                if int(i)==int(self.jsonData["node_id"]):
                    return self.jsonData["client_map"][i]["ip"]+":"+self.getServerPort()
        return -1
    
    
    def getSelfForElection(self):
        if self.jsonData and self.jsonData["node_id"]:
            for i in self.jsonData["client_map"]:
                if int(i)==int(self.jsonData["node_id"]):
                    return self.jsonData["client_map"][i]["ip"]+":"+self.getElectionPort()
        return -1
    
    def getPartners(self):
        partners = []
        if self.jsonData and self.jsonData["node_id"]:
            for i in self.jsonData["client_map"]:
                if int(i)!=int(self.jsonData["node_id"]):
                    partners.append((self.jsonData["client_map"][i]["ip"]+":"+self.getServerPort()))
        return partners

    def getAllForServer(self):
        partners = []
        if self.jsonData and self.jsonData["node_id"]:
            for i in self.jsonData["client_map"]:
                partners.append((self.jsonData["client_map"][i]["ip"]+":"+self.getServerPort()))
        return partners
    
    def getPartnersForElection(self):
        partnersForElection = []
        if self.jsonData and self.jsonData["node_id"]:
            for i in self.jsonData["client_map"]:
                if int(i)!=int(self.jsonData["node_id"]):
                    temp = self.jsonData["client_map"][i]["ip"]
                    temp = temp + ":"+ self.getElectionPort()
                    partnersForElection.append(temp)
        return partnersForElection


    def getSuperNode(self):
        if self.jsonData:
            return self.jsonData["superNodeIp"]
        return -1
    
    def getSuperNodePort(self):
        if self.jsonData:
            return self.jsonData["superNodePort"]
        return -1

    def getSuperNodeIp(self):
        return self.getSuperNode()+":"+self.getSuperNodePort()

    def getLeader(self):
        if self.jsonData:
            return self.jsonData["currentLeader"]
        return -1

    def setLeader(self,leader):
        if self.jsonData and leader:
            self.jsonData["currentLeader"] = leader.split(":")[0]+":3000"
            with open("valid_ip.json","w") as jsonfile:
                json.dump(self.jsonData,jsonfile)
            self.readJSON()
        else:
            return
        
    
    def setInActive(self,ipAddress):
        if self.jsonData:
            for j in self.jsonData["client_map"]:
                print(j)
                if self.jsonData["client_map"][j]["ip"]==ipAddress:
                    self.jsonData["client_map"][j]["status"] = "False"
            with open("valid_ip.json","w") as jsonfile:
                json.dump(self.jsonData,jsonfile)
            self.readJSON()
        else:
            return
    
    def setActive(self,ipAddress):
        if self.jsonData:
            for j in self.jsonData["client_map"]:
                print(j)
                if self.jsonData["client_map"][j]["ip"]==ipAddress:
                    self.jsonData["client_map"][j]["status"] = "True"
            with open("valid_ip.json","w") as jsonfile:
                json.dump(self.jsonData,jsonfile)
            self.readJSON()
        else:
            return

    

    

if __name__ == "__main__":
    t = IPUtil()
    # print(t.getSelf())
    print(t.getSuperNodeIp())
    # print(t.getPartnersForElection())
    # print(t.getPartners())
    # print(t.getSelfForElection())
    #print(t.setInActive("192.168.43.170"))
    # print([t.getSelf()] + t.getPartners())