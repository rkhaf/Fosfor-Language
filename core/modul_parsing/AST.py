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
        self.nodeContext : node.nodeClass
        self.context : list[ASTClass | node.nodeClass] = [self]
        self.nodes : list[node.nodeClass] = []
    
    def printTree(self)->None:
        print("[GLOBAL]")
        if(len(self.nodes)!=0):
            for node in self.nodes:
                # print("  ",node.getDatas())
                print(json.dumps(node.getDatas(), indent=2))
    
    def addNode(self, p_node : node.nodeClass)->None:
        if(self.context[-1] is self):
            self.nodes.append(p_node)
    
    def addContext(self, p_node : node.nodeClass)->None:
        self.context.append(p_node)
    
    def popContext(self)->None:
        self.context.pop()
