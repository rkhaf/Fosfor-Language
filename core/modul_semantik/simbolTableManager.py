from data_language.tokens import tokenClass
# from data_language.tokens import tokenType
from metadata.datatypeClass import datatypes
from metadata.datatypeClass import TIPEDATA_NULL
from pohon.node import nodeBikinFungsi
from pohon.node import nodeClass
from typing import Any

class scopeContainer:
    def __init__(self)->None:
        self.scopeParent : scopeContainer | None = None
        self.mappingVariabel : dict[str, varibelObjek] = {}
        self.mappingFungsi : dict[str, fungsiObjek] = {}
    
    def cekVariabel(self, p_nama : str)->bool:
        if(self.scopeParent is None):
            return p_nama in self.mappingVariabel.keys()
        else:
            percobaanCari : bool = p_nama in self.mappingVariabel.keys()
            if(percobaanCari):
                return True
            else:
                return self.scopeParent.cekVariabel(p_nama)
            
    
    def printDatas(self) -> dict[str, Any]:
        temp : list[dict[str, Any]] = []
        tempMappFungsi : list[dict[str, Any]] = []
        
        if(len(self.mappingVariabel)>0):
            for nama, vrblObj in self.mappingVariabel.items():
                temp.append(vrblObj.printDatas())
                
        if(len(self.mappingFungsi)>0):
            for nama, fngsObj in self.mappingFungsi.items():
                tempMappFungsi.append(fngsObj.printDatas())
                
        return {"tipe" : "scope", "alamat" : hex(id(self)), "parent" : hex(id(self.scopeParent)) if not self.scopeParent is None else "NONE", "variables" : temp, "fungsi" : tempMappFungsi}

class varibelObjek:
    def __init__(self, p_nama : str, p_type : datatypes) -> None:
        self.nama : str = p_nama
        self.type : datatypes = p_type
    
    def printDatas(self)->dict[str, Any]:
        # print(F"nama: {self.nama}, tipe: {self.type}")
        return {"nama":self.nama, "tipe":self.type.__repr__()}
        # print("   NAMA :",self.nama)
        # print("   TIPE :",self.type)

class fungsiObjek:
    def __init__(self, p_namaFungsi : str, p_type : datatypes, p_parameters : list[varibelObjek], p_nodeRef : nodeClass) -> None:
        self.nama : str = p_namaFungsi
        self.type : datatypes = p_type
        self.parameters : list[varibelObjek] = p_parameters
        self.nodeRef : nodeClass = p_nodeRef
        
    def printDatas(self)->dict[str, Any]:
        # print(f"nama: {self.nama}, tipe: {self.type}, nodeRef: {self.nodeRef}, parameter: ")
        temp : list[Any] = []
        
        if(len(self.parameters)>0):
            for vrblObj in self.parameters:
                temp.append(vrblObj.printDatas())
        
        # if(len(self.parameters)>0):
        #     for varObj in self.parameters:
        #         print(varObj.printDatas())
        # else:
        #     print("      kosong") 
        
        return {"tipe":"fungsi", "nama":self.nama, "tipedata":str(self.type), "parameter":temp}