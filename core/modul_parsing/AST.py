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
        self.nodeRoot : node.nodeRoot = node.nodeRoot()
        self.nodeRootDivisiImpor : node.nodeRoot = node.nodeRoot()
        self.context : list[node.nodeClass] = [self.nodeRoot]
    
    def printTree(self)->None:
        print("[IMPORTING]")
        for node in self.nodeRootDivisiImpor.nodeContainer:
            pass
            print(json.dumps(node.getDatas(), indent=2))
            
        print("[GLOBAL]")
        for node in self.nodeRoot.nodeContainer:
            pass
            print(json.dumps(node.getDatas(), indent=2))
    
    def addNode(self, p_node : node.nodeClass)->None:
        pass
    
    def addContext(self, p_node : node.nodeClass)->None:
        self.context.append(p_node)
    
    def popContext(self)->None:
        self.context.pop()
    
    def getTree(self)->list[node.nodeClass]:
        return self.nodeRoot.nodeContainer
    
    def getTreeImporting(self)->list[node.nodeClass]:
        return self.nodeRootDivisiImpor.nodeContainer
