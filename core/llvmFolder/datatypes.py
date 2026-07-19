from library import LLVM_PRIMITIVE_TYPES
from library import llvm_dataTypeClass


class llvm_primitiveDatatype(llvm_dataTypeClass):
    def __init__(self, p_datatype_llvm : str)->None:
        self.typeStr = p_datatype_llvm
    
    def getTypeStr(self) -> str:
        return self.typeStr

    def getLLVMType(self):
        return LLVM_PRIMITIVE_TYPES.get(self.typeStr, None)