from enum import Enum

class jenisPrimitive(Enum):
    PRIM_INT = 1
    PRIM_FLOAT = 2
    PRIM_BOOL = 3
    PRIM_STR = 4
    PRIM_VOID = 5

class datatypes:
    """
    induk dari seluruh representasi tipedata
    """
    def __init__(self)->None:
        pass

class compositeDatatype(datatypes):
    """
    class parent dri seluruh tipedata komposit
    """
    pass

class primitiveDatatype(datatypes):
    """
    container tipedata primitive
    """
    def __init__(self, p_jenisPrimitive : jenisPrimitive, p_namaPrimitive : str)->None:
        self.jenisPrimitive : jenisPrimitive = p_jenisPrimitive
        self.namaPrimitive : str = p_namaPrimitive
    
    def __repr__(self) -> str:
        return self.namaPrimitive

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

PRIMITIVE_TIPEDATA_MAPPING : dict[str, primitiveDatatype] = {
    "integer" : TIPEDATA_INTEGER,
    "float" : TIPEDATA_FLOAT,
    "boolean" : TIPEDATA_BOOLEAN,
    "string" : TIPEDATA_STRING,
    "void" : TIPEDATA_VOID,
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