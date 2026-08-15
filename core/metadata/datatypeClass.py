from enum import Enum
from data_language import grammar
from data_language.tokens import tokenType

class jenisPrimitive(Enum):
    PRIM_INT = 1
    PRIM_FLOAT = 2
    PRIM_BOOL = 3
    PRIM_STR = 4
    PRIM_VOID = 5
    PRIM_ANY = 6


class datatypes:
    """
    induk dari seluruh representasi tipedata
    """
    def __init__(self)->None:
        self.namaPrimitive : str = "NULL"
        pass

    def _isPointer(self)->bool:
        return isinstance(self, pointerDatatype)

    def __repr__(self) -> str:
        return "NULL"



class datatypesFactory:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def konversi(p_tokenTypeInput : tokenType) ->datatypes:
        if(p_tokenTypeInput.name in PRIMITIVE_TIPEDATA_MAPPING.keys()):
            test = PRIMITIVE_TIPEDATA_MAPPING.get(p_tokenTypeInput.name)
            if(not test is None):
                return test
            
            else:return TIPEDATA_EROR
            
        else:return TIPEDATA_EROR
        
            

class compositeDatatype(datatypes):
    """
    class parent dri seluruh tipedata komposit
    """

class errorDatatype(datatypes):
    def __repr__(self) -> str:
        return "ERROR DATATYPE"

class nullDatatype(datatypes):
    def __repr__(self) -> str:
        return "NULLISH DATATYPE"

class primitiveDatatype(datatypes):
    """
    container tipedata primitive
    """
    def __init__(self, p_jenisPrimitive : jenisPrimitive, p_namaPrimitive : str)->None:
        self.jenisPrimitive : jenisPrimitive = p_jenisPrimitive
        self.namaPrimitive : str = p_namaPrimitive
    
    def __repr__(self):
        return self.namaPrimitive
    
    def __eq__(self, value: object) -> bool:
        if(isinstance(value, primitiveDatatype)):
            return self.jenisPrimitive == value.jenisPrimitive
        # return super().__eq__(value)
        return False

TIPEDATA_INTEGER : primitiveDatatype = primitiveDatatype(jenisPrimitive.PRIM_INT, "integer")
"""representasi tipedata integer dlm bentuk kelas
"""
TIPEDATA_FLOAT : primitiveDatatype = primitiveDatatype(jenisPrimitive.PRIM_FLOAT, "float")
"""representasi tipedata float dlm bentuk kelas
"""
TIPEDATA_BOOLEAN : primitiveDatatype = primitiveDatatype(jenisPrimitive.PRIM_BOOL, "boolean")
"""representasi tipedata boolean dlm bentuk kelas
"""
TIPEDATA_STRING : primitiveDatatype = primitiveDatatype(jenisPrimitive.PRIM_STR, "string")
"""representasi tipedata string dlm bentuk kelas
"""
TIPEDATA_VOID : primitiveDatatype = primitiveDatatype(jenisPrimitive.PRIM_VOID, "void")
"""representasi void dlm bentuk kelas
"""

TIPEDATA_ANY : primitiveDatatype = primitiveDatatype(jenisPrimitive.PRIM_ANY, "any")
"""representasi bentuk any dlm bentuk kelas (dipake khusus sistem)
"""

TIPEDATA_NULL : nullDatatype = nullDatatype()
"""representasi null dlm bentuk kelas
"""

TIPEDATA_EROR : errorDatatype = errorDatatype()
"""representasi error dlm bentuk kelas
"""

PRIMITIVE_TIPEDATA_MAPPING : dict[str, primitiveDatatype] = {
    tokenType.T_LITERAL_INT.name : TIPEDATA_INTEGER,
    tokenType.T_LITERAL_FLOAT.name : TIPEDATA_FLOAT,
    tokenType.T_LITERAL_BOOL.name : TIPEDATA_BOOLEAN,
    tokenType.T_LITERAL_STR.name : TIPEDATA_STRING,
    tokenType.T_VOID.name : TIPEDATA_VOID,

    tokenType.T_TIPE_INT.name : TIPEDATA_INTEGER,
    tokenType.T_TIPE_FLT.name : TIPEDATA_FLOAT,
    tokenType.T_TIPE_BOOL.name : TIPEDATA_BOOLEAN,
    tokenType.T_TIPE_STR.name : TIPEDATA_STRING,
    tokenType.T_VOID.name : TIPEDATA_VOID,
}
"""mapping {nama string tipedata} : {kelas representasi tipedata}
"""

class vektorDatatype(compositeDatatype):
    def __init__(self, p_isiTipedataList:datatypes) -> None:
        self.isiTipedataList : datatypes = p_isiTipedataList
        super().__init__()

    def __repr__(self) -> str:
        return f"vektor[{self.isiTipedataList}]"

class pointerDatatype(compositeDatatype):
    def __init__(self, p_baseTipeData : datatypes) -> None:
        self.baseTipeData : datatypes = p_baseTipeData
        super().__init__()

    def __repr__(self) -> str:
        return f"ptr {self.baseTipeData}"