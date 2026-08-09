# from typing import NamedTuple
from enum import Enum, auto
# from data_language.keywords import primitiveList


class tokenType(Enum):
    T_NULL = auto()
    T_EROR = auto()
    T_UDTF = auto()
    T_LTRL = auto()
    T_KYWR = auto()
    T_OPRT = auto()
    T_IDTF = auto()
    T_IVTF = auto()
    T_ALMT = auto()
    T_PTER = auto()
    T_AKHR = auto()
    T_ISNY = auto()
    T_STRK = auto()
    T_FGSI = auto()
    T_VOID = auto()
    T_RFSI = auto()
    T_KLAU = auto()
    T_PRSM = auto()
    T_SAAT = auto()
    T_STOP = auto()
    T_LNJT = auto()
    T_LAIN = auto()
    T_PMNY = auto()
    T_BLKN = auto()
    T_NGGK = auto()
    T_NGLG = auto()
    T_SLMA = auto()
    T_MSAL = auto()

    T_LGKA_BKAN = auto()
    T_LGKA_ATAU = auto()
    T_LGKA_DAN = auto()

    T_TIPE_INT = auto()
    T_TIPE_FLT = auto()
    T_TIPE_BOOL = auto()
    T_TIPE_STR = auto()

    T_LITERAL_INT = auto()
    T_LITERAL_FLOAT = auto()
    T_LITERAL_BOOL = auto()
    T_LITERAL_STR = auto()

    T_PRTS_KIRI = auto()
    T_PRTS_KNAN = auto()

    T_DIVE = auto()
    T_MDLO = auto()
    T_MINS = auto()
    T_MULT = auto()
    T_PLUS = auto()
    T_ICRT = auto()
    T_DCRT = auto()
    T_SMDG = auto()

    T_BKIN = auto()
    T_VRBL = auto()
    T_NMNY = auto()
    T_TPNY = auto()
    T_NLNY = auto()
    T_DLMR = auto()

    T_CMPR_KCIL = auto()
    T_CMPR_BSAR = auto()
    T_CMPR_SBSR = auto()
    T_CMPR_SKCL = auto()
    T_CMPR_SAMA = auto()
    T_CMPR_GSMA = auto()

    T_SYMBOL_KRWL_KIRI = auto()
    T_SYMBOL_KRWL_KNAN = auto()

    T_SYMBOL_BRKT_KIRI = auto()
    T_SYMBOL_BRKT_KNAN = auto()

    T_SYMBOL_SERU = auto()
    T_SYMBOL_AT = auto()
    T_SYMBOL_HSTG = auto()
    T_SYMBOL_DLLR = auto()
    T_SYMBOL_CRET = auto()
    T_SYMBOL_AMPD = auto()
    T_SYMBOL_TKMA = auto()
    T_SYMBOL_TKWA = auto()
    T_SYMBOL_TNYA = auto()
    T_SYMBOL_KCIL = auto()
    T_SYMBOL_BSAR = auto()
    T_SYMBOL_GRLR = auto()
    T_SYMBOL_KOMA = auto()
    T_SYMBOL_TTIK = auto()

# class Token(NamedTuple):
#     baris:int
#     kolom:int
#     tipe:tokenType
#     nilai:str

class tokenClass:
    __slots__ = ('baris', 'kolom', 'tipe', 'nilai')
    
    def __init__(self, p_baris:int, p_kolom:int, p_tipe:tokenType, p_nilai:str) -> None:
        self.baris : int = p_baris
        self.kolom : int = p_kolom
        self.tipe : tokenType = p_tipe
        self.nilai : str = p_nilai
    
    def isPrimitiveValues(self)->bool:
        from data_language.grammar import primitiveList
        return self.tipe in primitiveList.values()
    
    def isKeyword(self)->bool:
        from data_language.grammar import keywordList
        return self.tipe in keywordList.values()
    
    def __repr__(self) -> str:
        return f"{self.tipe.name} : {self.nilai}"
    
    def getValueLength(self)->int:
        return len(self.nilai)
    
    def isIdentifier(self)->bool:
        return self.tipe==tokenType.T_IDTF