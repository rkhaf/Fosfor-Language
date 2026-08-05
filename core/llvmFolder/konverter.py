from llvmlite import ir
from metadata.datatypeClass import datatypes
from metadata.datatypeClass import primitiveDatatype
from metadata.datatypeClass import TIPEDATA_BOOLEAN
from metadata.datatypeClass import TIPEDATA_INTEGER
from metadata.datatypeClass import TIPEDATA_FLOAT
from metadata.datatypeClass import TIPEDATA_STRING
from metadata.datatypeClass import TIPEDATA_VOID

LLVM_PRIMITIVE_TYPES : dict[str, ir.Type] = {
    # """
    # berisi sekumpulan datatype primitiv utk llvm
    # """
    
    TIPEDATA_INTEGER.namaPrimitive : ir.IntType(32),
    TIPEDATA_FLOAT.namaPrimitive : ir.DoubleType(),
    TIPEDATA_BOOLEAN.namaPrimitive : ir.IntType(1),
    # "char" : ir.IntType(8),
    TIPEDATA_STRING.namaPrimitive : ir.PointerType(ir.IntType(8)),
    TIPEDATA_VOID.namaPrimitive : ir.VoidType(),
}

class LLVMLITEConverterClass:
    @staticmethod
    def konversiTipedata(p_tipedata : datatypes)->ir.Type:
        if(isinstance(p_tipedata, primitiveDatatype)):
            if(p_tipedata.namaPrimitive in LLVM_PRIMITIVE_TYPES.keys()):
                getter : ir.Type | None = LLVM_PRIMITIVE_TYPES.get(p_tipedata.namaPrimitive)
                if(not getter is None):
                    return getter
                else:
                    raise Exception("RETURNING NONE")
            else:
                raise Exception("[LLVMLITEConverterClass] tipedata blm kedaftar dimapping LLVM_PRIMITIVES")
        else:
            raise Exception("[LLVMLITEConverterClass] tipedata komposit blm kedaftar")