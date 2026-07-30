from data_language.tokens import tokenClass
# from data_language.tokens import tokenType
from metadata.datatypeClass import datatypes
from metadata.datatypeClass import TIPEDATA_NULL

class scopeContainer:
    def __init__(self)->None:
        self.scopeParent : scopeContainer
        self.mappingVariabel : list[varibelObjek]
    

class varibelObjek:
    def __init__(self, p_token : tokenClass) -> None:
        self.nama : str = p_token.nilai
        self.datatype : datatypes = TIPEDATA_NULL