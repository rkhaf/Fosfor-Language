from llvmlite import ir

from typing import TypedDict

from llvmFolder.konverter import TIPEDATA_LLVM_BOOLEAN
from llvmFolder.konverter import TIPEDATA_LLVM_STRING
from llvmFolder.konverter import TIPEDATA_LLVM_INTEGER
from llvmFolder.konverter import TIPEDATA_LLVM_FLOAT
from llvmFolder.konverter import TIPEDATA_LLVM_VOID

class detailFungsi(TypedDict):
    namaDiCPP : str
    parameter : list[ir.Type]
    tipeReturn : ir.Type

fungsiBuiltin : dict[str, list[detailFungsi]] = {
    "tampilin":[
        {"namaDiCPP":"fosfor_tampilin_int", "tipeReturn":ir.VoidType(), "parameter":[TIPEDATA_LLVM_INTEGER]},
        {"namaDiCPP":"fosfor_tampilin_str", "tipeReturn":ir.VoidType(), "parameter":[TIPEDATA_LLVM_STRING]},
        {"namaDiCPP":"fosfor_tampilin_bool", "tipeReturn":ir.VoidType(), "parameter":[TIPEDATA_LLVM_BOOLEAN]},
        {"namaDiCPP":"fosfor_tampilin_flt", "tipeReturn":ir.VoidType(), "parameter":[TIPEDATA_LLVM_FLOAT]},
    ],
    "mulaiTimer":[
        {"namaDiCPP":"fosfor_mulai_timer","tipeReturn":ir.VoidType(), "parameter":[]}
    ],
    "stopTimer":[
        {"namaDiCPP":"fosfor_stop_timer","tipeReturn":ir.VoidType(), "parameter":[]}
    ]
}

class builtinClass:
    def __init__(self) -> None:
        self.fungsiBuiltin : dict[str, list[detailFungsi]] = {
            "tampilin":[
                {"namaDiCPP":"fosfor_trampilin_int", "tipeReturn":ir.VoidType(), "parameter":[TIPEDATA_LLVM_INTEGER]},
                {"namaDiCPP":"fosfor_trampilin_str", "tipeReturn":ir.VoidType(), "parameter":[TIPEDATA_LLVM_STRING]},
                {"namaDiCPP":"fosfor_trampilin_bool", "tipeReturn":ir.VoidType(), "parameter":[TIPEDATA_LLVM_BOOLEAN]},
                {"namaDiCPP":"fosfor_trampilin_flt", "tipeReturn":ir.VoidType(), "parameter":[TIPEDATA_LLVM_FLOAT]},
            ],
            "mulaiTimer":[
                {"namaDiCPP":"fosfor_mulai_timer","tipeReturn":ir.VoidType(), "parameter":[]}
            ],
            "stopTimer":[
                {"namaDiCPP":"fosfor_stop_timer","tipeReturn":ir.VoidType(), "parameter":[]}
            ]
        }
    
    @staticmethod
    def cekFungsi(p_namaFungsi:str)->bool:
        if(p_namaFungsi in fungsiBuiltin.keys()):
            return True
        else:
            return False
    
    @staticmethod
    def getFungsiAllVariant(p_namaFungsi:str)->list[detailFungsi] | None:
        if(p_namaFungsi in fungsiBuiltin.keys()):
            return fungsiBuiltin.get(p_namaFungsi, None)
        else:
            return None
    
    @staticmethod
    def getDetailByParams(p_datatypeParams : list[ir.Type], p_fungsiVariantList:list[detailFungsi])->detailFungsi | None:
        for fungsiVariant in p_fungsiVariantList:
            if(p_datatypeParams==fungsiVariant["parameter"]):
                return fungsiVariant
        return None