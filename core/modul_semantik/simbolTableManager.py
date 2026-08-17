from __future__ import annotations
# from data_language.tokens import tokenClass
# from data_language.tokens import tokenType
from metadata.datatypeClass import datatypes
from metadata.datatypeClass import TIPEDATA_NULL
from metadata.datatypeClass import TIPEDATA_VOID
# from pohon.node import nodeBikinFungsi
from pohon.node import nodeClass
from typing import Any

class varibelObjek:
    def __init__(self, p_bernilai : bool, p_nama : str, p_type : datatypes, p_baris : int =-1) -> None:
        self.nama : str = p_nama
        self.type : datatypes = p_type
        self.invalid : bool = False
        self.bernilai : bool = p_bernilai
        self.baris : int = p_baris
    
    def printDatas(self)->dict[str, Any]:
        return {"nama":self.nama, "tipe":self.type.__repr__(), "bernilai":self.bernilai}

class fungsiObjek:
    def __init__(self, p_namaFungsi : str, p_type : datatypes, p_parameters : list[varibelObjek], p_nodeRef : nodeClass) -> None:
        self.nama : str = p_namaFungsi
        self.type : datatypes = p_type
        self.parameters : list[varibelObjek] = p_parameters
        self.nodeRef : nodeClass = p_nodeRef
        self.invalid : bool = False
        
    def printDatas(self)->dict[str, Any]:
        temp : list[Any] = []
        
        if(len(self.parameters)>0):
            for vrblObj in self.parameters:
                temp.append(vrblObj.printDatas())
        
        
        return {"tipe":"fungsi", "nama":self.nama, "tipedata":str(self.type), "parameter":temp}

class scopeContainer:
    def __init__(self)->None:
        self.scopeParent : scopeContainer | None = None
        self.mappingVariabel : dict[str, varibelObjek] = {}
        self.mappingFungsi : dict[str, fungsiObjek] = {}
        self.mappingBuiltin : dict[str, dict[str, fungsiObjek]] = {}
        self._dummyVariabel : varibelObjek = varibelObjek(True, "ERROR", TIPEDATA_NULL)
        self._dummyFungsi : fungsiObjek = fungsiObjek("ERROR", TIPEDATA_NULL, [], nodeClass(-1, -1))
    
    def cekVariabel(self, p_nama : str)->bool:
        if(self.scopeParent is None):
            return p_nama in self.mappingVariabel.keys()
        else:
            percobaanCari : bool = p_nama in self.mappingVariabel.keys()
            if(percobaanCari):
                return True
            else:
                return self.scopeParent.cekVariabel(p_nama)

    def getVariabel(self, p_nama : str)->varibelObjek:
        if(self.cekVariabel(p_nama)):
            if(self.scopeParent is None):
                return self.mappingVariabel.get(p_nama, self._dummyVariabel)
            
            else:
                percobaanCari : bool = p_nama in self.mappingVariabel.keys()
                if(percobaanCari):
                    return self.mappingVariabel.get(p_nama, self._dummyVariabel)
                else:
                    return self.scopeParent.getVariabel(p_nama)
        else:
            raise Exception("ERROR")
    
    def cekFungsi(self, p_namaFungsi : str)->bool:
        if(self.scopeParent is None):
            return p_namaFungsi in self.mappingFungsi.keys()
        else:
            percobaanCari : bool = p_namaFungsi in self.mappingFungsi.keys()
            if(percobaanCari):
                return True
            else:
                return self.scopeParent.cekFungsi(p_namaFungsi)
            
    def cekModul(self, p_namaModul : str)->bool:
        if(self.scopeParent is None):
            return p_namaModul in self.mappingBuiltin.keys()
        else:
            percobaanCari : bool = p_namaModul in self.mappingBuiltin.keys()
            if(percobaanCari):
                return True
            else:
                return self.scopeParent.cekModul(p_namaModul)
            
    def cekFungsiBuiltin(self, p_namaModul : str , p_namaFungsi : str)->bool:
        if(self.scopeParent is None):
            if(p_namaModul in self.mappingBuiltin.keys()):
                return p_namaFungsi in self.mappingBuiltin[p_namaModul].keys()
            else:
                return False
        else:
            if(p_namaModul in self.mappingBuiltin.keys()):
                percobaanCari : bool = p_namaFungsi in self.mappingBuiltin[p_namaModul].keys()
                if(percobaanCari):
                    return True
                else:
                    return self.scopeParent.cekFungsiBuiltin(p_namaModul, p_namaFungsi)
            else:
                return self.scopeParent.cekFungsiBuiltin(p_namaModul, p_namaFungsi)
                # return False
    
    def getFungsi(self, p_namaFungsi : str)->fungsiObjek:
        if(self.cekFungsi(p_namaFungsi)):
            if(self.scopeParent is None):
                return self.mappingFungsi.get(p_namaFungsi, self._dummyFungsi)
            
            else:
                percobaanCari : bool = p_namaFungsi in self.mappingFungsi.keys()
                if(percobaanCari):
                    return self.mappingFungsi.get(p_namaFungsi, self._dummyFungsi)
                else:
                    return self.scopeParent.getFungsi(p_namaFungsi)
        else:
            raise Exception("ERROR")
        
    def getFungsiBuiltin(self, p_namaModul : str, p_namaFungsi : str)->fungsiObjek:
        if(self.cekFungsiBuiltin(p_namaModul, p_namaFungsi)):
            if(self.scopeParent is None):
                # return self.mappingFungsi.get(p_namaFungsi, self._dummyFungsi)
                return self.mappingBuiltin[p_namaModul].get(p_namaFungsi, self._dummyFungsi)
            
            else:
                percobaanCari : bool = p_namaFungsi in self.mappingFungsi.keys()
                if(percobaanCari):
                    return self.mappingBuiltin[p_namaModul].get(p_namaFungsi, self._dummyFungsi)
                else:
                    return self.scopeParent.getFungsiBuiltin(p_namaModul, p_namaFungsi)
        else:
            raise Exception("ERROR")
    
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