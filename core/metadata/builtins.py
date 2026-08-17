from llvmlite import ir

from typing import TypedDict

from collections import defaultdict

from pohon import node

from llvmFolder.konverter import TIPEDATA_LLVM_BOOLEAN
from llvmFolder.konverter import TIPEDATA_LLVM_STRING
from llvmFolder.konverter import TIPEDATA_LLVM_INTEGER
from llvmFolder.konverter import TIPEDATA_LLVM_FLOAT
from llvmFolder.konverter import TIPEDATA_LLVM_VOID

from metadata.datatypeClass import TIPEDATA_VOID
from metadata.datatypeClass import TIPEDATA_NULL
from metadata.datatypeClass import TIPEDATA_ANY
from metadata.datatypeClass import TIPEDATA_EROR
from metadata.datatypeClass import TIPEDATA_BOOLEAN

from modul_semantik.simbolTableManager import varibelObjek
from modul_semantik.simbolTableManager import fungsiObjek

# class detailFungsi(TypedDict):
#     namaDiCPP : str
#     parameter : list[ir.Type]
#     tipeReturn : ir.Type
    
    

class detailFungsiLLVM:
    __slots__ = ('kumpulanFungsi')
    
    def __init__(self) -> None:
        self.kumpulanFungsi : dict[str, list[tuple[str, list[ir.Type], ir.Type]]] = defaultdict(list)
        
    def addFungsi(self,p_namaFungsi : str, p_namaDiCPP : str, p_parameter : list[ir.Type], p_tipeReturn : ir.Type)->None:
        self.kumpulanFungsi[p_namaFungsi].append((p_namaDiCPP, p_parameter, p_tipeReturn))
        pass
# dict[str, dict[str, list[detailFungsi]]]
# dict[namaModul, dict[namaFungsi, (detailFungsi)]]
# fungsiBuiltinLLVM : dict[str, list[detailFungsi]] = {
#     "tampilin":[
#         {"namaDiCPP":"fosfor_tampilin_int", "tipeReturn":TIPEDATA_LLVM_VOID, "parameter":[TIPEDATA_LLVM_INTEGER]},
#         {"namaDiCPP":"fosfor_tampilin_str", "tipeReturn":TIPEDATA_LLVM_VOID, "parameter":[TIPEDATA_LLVM_STRING]},
#         {"namaDiCPP":"fosfor_tampilin_bool", "tipeReturn":TIPEDATA_LLVM_VOID, "parameter":[TIPEDATA_LLVM_BOOLEAN]},
#         {"namaDiCPP":"fosfor_tampilin_flt", "tipeReturn":TIPEDATA_LLVM_VOID, "parameter":[TIPEDATA_LLVM_FLOAT]},
#     ],
#     "mulaiTimer":[
#         {"namaDiCPP":"fosfor_mulai_timer","tipeReturn":TIPEDATA_LLVM_VOID, "parameter":[]}
#     ],
#     "stopTimer":[
#         {"namaDiCPP":"fosfor_stop_timer","tipeReturn":TIPEDATA_LLVM_VOID, "parameter":[]}
#     ]
# }

# fungsiBuiltinFOS : list[fungsiObjek] = [
#     fungsiObjek("tampilin", TIPEDATA_VOID, [varibelObjek(False,"p_inputCout", TIPEDATA_ANY)], node.nodeClass(-1, -1)),
#     fungsiObjek("mulaiTimer", TIPEDATA_VOID, [], node.nodeClass(-1, -1)),
#     fungsiObjek("stopTimer", TIPEDATA_VOID, [], node.nodeClass(-1, -1)),
# ]

class builtinClass:
    def __init__(self) -> None:
        self.fungsiBuiltinLLVM : dict[str, detailFungsiLLVM] = {}
        self.fungsiBuiltinFOS : dict[str, dict[str, fungsiObjek]] = {}
        # self.fungsiBuiltinLLVM : dict[str, list[detailFungsi]] = {
        #     "tampilin":[
        #         {"namaDiCPP":"fosfor_trampilin_int", "tipeReturn":ir.VoidType(), "parameter":[TIPEDATA_LLVM_INTEGER]},
        #         {"namaDiCPP":"fosfor_trampilin_str", "tipeReturn":ir.VoidType(), "parameter":[TIPEDATA_LLVM_STRING]},
        #         {"namaDiCPP":"fosfor_trampilin_bool", "tipeReturn":ir.VoidType(), "parameter":[TIPEDATA_LLVM_BOOLEAN]},
        #         {"namaDiCPP":"fosfor_trampilin_flt", "tipeReturn":ir.VoidType(), "parameter":[TIPEDATA_LLVM_FLOAT]},
        #     ],
        #     "mulaiTimer":[
        #         {"namaDiCPP":"fosfor_mulai_timer","tipeReturn":ir.VoidType(), "parameter":[]}
        #     ],
        #     "stopTimer":[
        #         {"namaDiCPP":"fosfor_stop_timer","tipeReturn":ir.VoidType(), "parameter":[]}
        #     ]
        # }
    
    def proses(self, p_dictFungsiBuiltinLLVM : dict[str, detailFungsiLLVM], p_fungsiBuiltinFos : dict[str, dict[str, fungsiObjek]])->None:
        self.fungsiBuiltinLLVM = p_dictFungsiBuiltinLLVM
        self.fungsiBuiltinFOS = p_fungsiBuiltinFos
    
    # @staticmethod
    def cekFungsi(self, p_namaModul : str, p_namaFungsi:str)->bool:
        if(p_namaModul in self.fungsiBuiltinLLVM.keys()):
            getAsModul : detailFungsiLLVM | None = self.fungsiBuiltinLLVM.get(p_namaModul, None)
            if(not getAsModul is None and p_namaFungsi in getAsModul.kumpulanFungsi.keys()):
                return True
            else:
                return False
        else:return False
    
    # @staticmethod
    def getFungsiAllVariant(self, p_namaModul : str, p_namaFungsi:str)->list[tuple[str, list[ir.Type], ir.Type]] | None:
        if(p_namaModul in self.fungsiBuiltinLLVM.keys()):
            getAsModul : detailFungsiLLVM | None = self.fungsiBuiltinLLVM.get(p_namaModul, None)
            if(not getAsModul is None and p_namaFungsi in getAsModul.kumpulanFungsi.keys()):
                return getAsModul.kumpulanFungsi.get(p_namaFungsi, None)
            else:
                return None
        else:return None
    
    # @staticmethod
    # def getDetailByParams(self, p_datatypeParams : list[ir.Type], p_fungsiVariantList:list[tuple[str, list[ir.Type], ir.Type]])->tuple[str, list[ir.Type], ir.Type] | None:
    #     for fungsiVariant in p_fungsiVariantList:
    #         if(p_datatypeParams==fungsiVariant["parameter"]):
    #             return fungsiVariant
    #     return None