from llvmFolder.library import LLVM_PRIMITIVE_TYPES

class nodeClass:
    def __init__(self)->None:
        pass

class nodeBikinVariabel(nodeClass):
    def __init__(self)->None:
        self.namaVariabel : str = ""
        self.tipedataVariabel : str = ""
        self.nilaiVariabel : nodeClass = nodeClass()
        
class nomorNode(nodeClass):
    def __init__(self, )