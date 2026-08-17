from modul_parsing.AST import ASTClass
from pathlib import Path
from config import path_builtins
from pohon.node import nodeImpor
from collections import namedtuple, defaultdict
from llvmlite.ir import Type

from metadata.datatypeClass import datatypes
from metadata.datatypeClass import TIPEDATA_ANY
from metadata.datatypeClass import TIPEDATA_BOOLEAN
from metadata.datatypeClass import TIPEDATA_INTEGER
from metadata.datatypeClass import TIPEDATA_FLOAT
from metadata.datatypeClass import TIPEDATA_STRING
from metadata.datatypeClass import TIPEDATA_VOID
from metadata import builtins

from typing import Any

from modul_semantik.simbolTableManager import varibelObjek
from modul_semantik.simbolTableManager import fungsiObjek

from pohon import node

import json

from llvmFolder.konverter import LLVM_PRIMITIVE_TYPES

mappingStrKeDatatype : dict[str, datatypes] = {
    TIPEDATA_ANY.namaPrimitive : TIPEDATA_ANY,
    TIPEDATA_BOOLEAN.namaPrimitive : TIPEDATA_BOOLEAN,
    TIPEDATA_FLOAT.namaPrimitive : TIPEDATA_FLOAT,
    TIPEDATA_INTEGER.namaPrimitive : TIPEDATA_INTEGER,
    TIPEDATA_STRING.namaPrimitive : TIPEDATA_STRING,
    TIPEDATA_VOID.namaPrimitive : TIPEDATA_VOID,
}

class importHandler:
    def __init__(self) -> None:
        self.runtimePathList : list[str] = []
        self.mappingFungsiBuiltinFOS : dict[str, dict[str, fungsiObjek]] = defaultdict(dict)
        self.mappingFungsiBuiltinLLVM : dict[str, builtins.detailFungsiLLVM] = defaultdict()
        pass
    
    def getLoadedJsonModul(self, p_namaModul : str)->tuple[Path, dict[str, str]]:
        pathModul : Path = path_builtins / p_namaModul
        fileManifest : Path = pathModul / "manifest.json"
        fileObject : Path = pathModul / f"{p_namaModul}.o"
        
        loadedJson : dict[str, str] = {}
        
        if(not pathModul.is_dir()):
            raise Exception("modul gk ketemu")
        
        if(not fileManifest.is_file()):
            raise Exception("file gaada")
            
        if(not fileObject.is_file()):
            raise Exception("file gaada")

        with open(fileManifest, "r") as isiJson:
            loadedJson = json.load(isiJson)
            pass
        
        return (fileObject, loadedJson)
    
    def bacaDataJson(self, p_jsonDict : dict[Any, Any])->None:
        for fungsi in p_jsonDict['daftarFungsi']:
            namaFungsi : str = fungsi
            namaModul : str = p_jsonDict['namaModul']

            getter_tipedataFungsi : datatypes | None = mappingStrKeDatatype.get(p_jsonDict['daftarFungsi'][namaFungsi]['tipeReturn'])
            getter_tipedataFungsiLLVM : Type | None = LLVM_PRIMITIVE_TYPES.get(p_jsonDict['daftarFungsi'][namaFungsi]['tipeReturn'])

            assert isinstance(getter_tipedataFungsi, datatypes), "[importHandler] getter_tipedatafungsi eror"
            assert isinstance(getter_tipedataFungsiLLVM, Type), "[importHandler] getter_tipedatafungsi eror"
            tipedataFungsi : datatypes = getter_tipedataFungsi
            tipedataFungsiLLVM : Type = getter_tipedataFungsiLLVM

            parameters : list[varibelObjek] = []
            # parameterLLVM : list[Type] = []

            for paramFungsi in p_jsonDict['daftarFungsi'][namaFungsi]['parameter']:
                getter_namaParam : str = paramFungsi['nama']

                getter_tipeParam : datatypes | None = mappingStrKeDatatype.get(paramFungsi['tipe']) 
                # getter_tipeParamLLVM : datatypes | None = LLVM_PRIMITIVE_TYPES.get(paramFungsi['tipe']) 
                assert isinstance(getter_tipeParam, datatypes), "[importHandler] getter_tipeparam eror"
                # assert isinstance(getter_tipeParamLLVM, Type), "[importHandler] getter_tipeparamLLVM eror"
                tipeParam : datatypes = getter_tipeParam
                # tipeParamLLVM : Type = getter_tipeParamLLVM

                nilaiParam : bool = False
                if('nilai' in paramFungsi):
                    getter_nilaiParam : str | None = paramFungsi['nilai']
                    nilaiParam  = False if getter_nilaiParam is None else True
                
                tempVarObj : varibelObjek = varibelObjek(nilaiParam, getter_namaParam, tipeParam)
                # parameterLLVM.append(tipeParamLLVM)
                parameters.append(tempVarObj)
            
            # tempDetailFungsi : builtins.detailFungsi = 
            if(isinstance(p_jsonDict['daftarFungsi'][namaFungsi]['overloadCPP'], dict)):
                detailFungsiLLVM : builtins.detailFungsiLLVM = builtins.detailFungsiLLVM()
                for overloadFungsi in p_jsonDict['daftarFungsi'][namaFungsi]['overloadCPP']:
                    getter_tipeParam : Type | None =LLVM_PRIMITIVE_TYPES.get(overloadFungsi)
                    assert isinstance(getter_tipeParam, Type), "[importHandler] getter_tipeparam error"
                    
                    
                    detailFungsiLLVM.addFungsi(
                        namaFungsi,
                        p_jsonDict['daftarFungsi'][namaFungsi]['overloadCPP'][overloadFungsi],
                        [getter_tipeParam],
                        tipedataFungsiLLVM
                    )
                    self.mappingFungsiBuiltinLLVM[namaModul] = detailFungsiLLVM
                pass
            else:
                getter_tipeReturn : Type | None = LLVM_PRIMITIVE_TYPES.get(TIPEDATA_VOID.namaPrimitive)
                assert isinstance(getter_tipeReturn, Type), "[importHandler] getter_tipeReturn eror"
                detailFungsiLLVM : builtins.detailFungsiLLVM = builtins.detailFungsiLLVM()
                detailFungsiLLVM.addFungsi(
                    namaFungsi,
                    p_jsonDict['daftarFungsi'][namaFungsi]['overloadCPP'],
                    [],
                    tipedataFungsiLLVM
                )
                # tempDetailFungsi : builtins.detailFungsi = {
                #     "namaDiCPP":p_jsonDict['daftarFungsi'][namaFungsi]['overloadCPP'],
                #     "parameter":[],
                #     "tipeReturn":getter_tipeReturn
                # }
                # self.mappingFungsiBuiltinLLVM[namaFungsi].append(tempDetailFungsi)
                # self.mappingFungsiBuiltinLLVM[namaModul].setdefault(namaFungsi, []).append(tempDetailFungsi)
                self.mappingFungsiBuiltinLLVM[namaModul] = detailFungsiLLVM
                pass
            # tempFungsiObj : fungsiObjek = fungsiObjek(namaFungsi, tipedataFungsi, parameters, node.nodeClass(-1, -1))
            # self.mappingFungsiBuiltinFOS.append(fungsiObjek(namaFungsi, tipedataFungsi, parameters, node.nodeClass(-1, -1)))
            # self.mappingFungsiBuiltinFOS.setdefault(p_jsonDict['namaModul'], fungsiObjek(namaFungsi, tipedataFungsi, parameters, node.nodeClass(-1, -1)))
            self.mappingFungsiBuiltinFOS.setdefault(p_jsonDict['namaModul'], {}).setdefault(namaFungsi, fungsiObjek(namaFungsi, tipedataFungsi, parameters, node.nodeClass(-1, -1)))
        pass
    
    def handleModul(self, p_nodeImpor : nodeImpor)->None:
        jsonDict = self.getLoadedJsonModul(p_nodeImpor.nama.nilai)
        self.runtimePathList.append(str(jsonDict[0]))
        self.bacaDataJson(jsonDict[1])
        pass
    
    def proses(self, p_AST : ASTClass)->None:
        # p_AST.printTree()
        for node in p_AST.nodeRootDivisiImpor.nodeContainer:
            assert isinstance(node, nodeImpor), f"[importHandler] hrusnya nodenya nodeImpor, bukan {type(node)}"
            if(node.apakahBuiltin):
                self.handleModul(node)

    def getFosBuiltinMapping(self)->dict[str, dict[str, fungsiObjek]]:
        return self.mappingFungsiBuiltinFOS
    
    def getLLVMBuiltinMapping(self)->dict[str, builtins.detailFungsiLLVM]:
        return self.mappingFungsiBuiltinLLVM