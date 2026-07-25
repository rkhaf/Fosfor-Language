# from enum import Enum
from pohon import node
import json

# class states(Enum):
#     default = 0,
#     variabel = 1

# class scopes(Enum):
#     globalScope = 0

class ASTClass:
    def __init__(self)->None:
        # self.scope : scopes = scopes.globalScope
        # self.state : states = states.default
        self.nodeRoot : node.nodeRoot = node.nodeRoot()
        # self.nodeContext : node.nodeClass
        self.context : list[node.nodeClass] = [self.nodeRoot]
        # self.nodes : list[node.nodeClass] = [self.nodeRoot]
        # self.nodeRoot : 
    
    def printTree(self)->None:
        print("[GLOBAL]")
        # print("HANS :",json.dumps(self.nodeRoot.getDatas(), indent=2))
        for node in self.nodeRoot.nodeContainer:
            # print("  ",node.getDatas())
            print(json.dumps(node.getDatas(), indent=2))
        # if(len(self.nodes)!=0):
        #     for node in self.nodes:
        #         # print("  ",node.getDatas())
        #         print(json.dumps(node.getDatas(), indent=2))
    
    def addNode(self, p_node : node.nodeClass)->None:
        pass
    
    def addContext(self, p_node : node.nodeClass)->None:
        self.context.append(p_node)
    
    def popContext(self)->None:
        self.context.pop()
