from llvmlite import ir

LLVM_PRIMITIVE_TYPES : dict[str, ir.Type] = {
    """
    berisi sekumpulan datatype primitiv utk llvm
    """
    
    "i32" : ir.IntType(32),
    "f64" : ir.DoubleType(),
    "bool" : ir.IntType(1),
    "char" : ir.IntType(8),
    "string" : ir.PointerType(ir.IntType(8)),
}

class llvm_dataTypeClass:
    def getTypeStr(self)->str:
        raise NotImplementedError
    def getLLVMType(self)->ir.Type | None:
        raise NotImplementedError