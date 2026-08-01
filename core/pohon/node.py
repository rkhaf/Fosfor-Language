
from data_language.tokens import tokenClass
# from data_language.tokens import tokenType as Ttype
from typing import Any
# from metadata import datatypeClass
# from metadata.datatypeClass import datatypesFactory
from metadata.datatypeClass import datatypes
# from metadata.datatypeClass import primitiveDatatype
from metadata.datatypeClass import TIPEDATA_BOOLEAN
from metadata.datatypeClass import TIPEDATA_FLOAT
from metadata.datatypeClass import TIPEDATA_INTEGER
from metadata.datatypeClass import TIPEDATA_STRING
# from metadata.datatypeClass import TIPEDATA_VOID
from metadata.datatypeClass import TIPEDATA_NULL

class nodeClass:
    """
    node sepuh yg jadi tumpuan seluruh node
    """
    def __init__(self, p_baris : int, p_kolom : int)->None:
        self.baris : int = p_baris
        self.kolom : int = p_kolom
    
    def getDatas(self)->dict[str, Any]:
        return {}
    
    def getRealDatas(self)->dict[str, Any]:
        return {}

class nodeRoot(nodeClass):
    """
    node buat representasi dari scope root
    """
    def __init__(self, p_baris : int = 0, p_kolom : int = 0)->None:
        self.baris : int = p_baris
        self.kolom : int = p_kolom
        self.nodeContainer : list[nodeClass] = []
        super().__init__(p_baris, p_kolom)
    
    # def getDatas(self) -> dict[Any, Any]:
    #     temp : dict[str, Any] = {}
    #     for node in self.nodeContainer:
    #             node.getDatas()
        
    #     return self.nodeContainer

class nodeError(nodeClass):
    """
    buat bahan return-an klo semisal ada node yg gk valid
    """
    
class nodeEkspresi(nodeClass):
    """
    nodeParent buat node yg bisa ngereturn di kodenya
    """
    def __init__(self, p_baris : int, p_kolom : int, p_tipe : datatypes)->None:
        super().__init__(p_baris, p_kolom)
        self.tipe : datatypes = p_tipe
        pass
    
    def __repr__(self) -> str:
        return f"{self.tipe}"
    
    # def reset(self)->None:
    #     self.

class nodeStatement(nodeClass):
    """
    nodeParent buat node yg gak return apa2 di kodenya
    """
    def __init__(self, p_baris : int, p_kolom : int)->None:
        super().__init__(p_baris, p_kolom)
        pass

class nodeNomor(nodeEkspresi):
    """
    node buat ngecontain numerik
    """
    def __init__(self, p_token : tokenClass, p_tipedata : datatypes)->None:
        # print(p_tipedata)
        # assert p_token.tipe==Ttype.T_LITERAL_FLOAT or p_token.tipe==Ttype.T_LITERAL_INT, "ERRORDEV: nodeNomor hrusnya cmn nerima token numerik"
        assert p_tipedata==TIPEDATA_INTEGER or p_tipedata==TIPEDATA_FLOAT, "ERRORDEV: nodeNomor hrusnya cmn nerima token numerik"
        
        self.tipe : datatypes = p_tipedata
        self.nilai : str = p_token.nilai
        super().__init__(p_token.baris, p_token.kolom, self.tipe)
    
    def getDatas(self) -> dict[Any, Any]:
        return {"tipe" : "literal", "tipeNilai" : self.tipe.__repr__(), "nilai" : self.nilai}
    
    def getRealDatas(self)->dict[str, Any]:
        return {"tipe" : "literal", "tipeNilai" : self.tipe, "nilai" : self.nilai}

class nodeString(nodeEkspresi):
    """
    node buat ngecontain string
    """
    def __init__(self, p_token : tokenClass, p_tipedata : datatypes)->None:
        assert p_tipedata==TIPEDATA_STRING, "ERRORDEV: nodeString hrusnya cmn nerima token string"
        
        self.tipe : datatypes = p_tipedata
        self.nilai : str = p_token.nilai
        super().__init__(p_token.baris, p_token.kolom, self.tipe)
    
    def getDatas(self) -> dict[Any, Any]:
        return {"tipe" : "literal", "tipeNilai" : self.tipe.__repr__(), "nilai" : self.nilai}
        # return {"tipe" : self.tipe.name, "nilai" : self.nilai}
        
    def getRealDatas(self) -> dict[Any, Any]:
        return {"tipe" : "literal", "tipeNilai" : self.tipe, "nilai" : self.nilai}

class nodeBalikin(nodeStatement):
    def __init__(self, p_baris: int, p_kolom: int) -> None:
        self.returnEkspresi : nodeEkspresi
        super().__init__(p_baris, p_kolom)
    
    def getDatas(self) -> dict[Any, Any]:
        return {"tipe" : "pernyataanReturn", "nilai" : self.returnEkspresi.getDatas()}
        # return {"ngereturn : " : self.returnEkspresi.getDatas()}
        
    def getRealDatas(self) -> dict[str, Any]:
        return {"tipe" : "pernyataanReturn", "nilai" : self.returnEkspresi.getRealDatas()}

class nodeIdentifier(nodeEkspresi):
    """
    node buat ngecontain identifier
    """
    def __init__(self, p_token : tokenClass) -> None:
    # def __init__(self, p_token : tokenClass, p_tipedata : datatypes, p_tipe: str="") -> None:
        self.identifierToken : str = p_token.nilai
        super().__init__(p_token.baris, p_token.kolom, TIPEDATA_NULL)
    
    def getDatas(self) -> dict[Any, Any]:
        # return {"tipe numerik" : self.tipe, "nilai numerik" : self.nilai}
        # return {self.identifierToken.tipe.name : self.identifierToken.nilai}
        return {"tipe" : "identifier", "nama" : self.identifierToken}
        
class nodeBoolean(nodeEkspresi):
    """
    node buat ngecontain boolean
    """
    def __init__(self, p_token : tokenClass, p_tipedata : datatypes)->None:
        assert p_tipedata==TIPEDATA_BOOLEAN, "ERRORDEV: nodeBoolean hrusnya cmn nerima token boolean"
        # assert p_token.tipe==Ttype.T_LITERAL_BOOL, "ERRORDEV: nodeBoolean hrusnya cmn nerima token boolean"
        
        self.tipe : datatypes = p_tipedata
        self.nilai : str = p_token.nilai
        super().__init__(p_token.baris, p_token.kolom, self.tipe)
    
    def getDatas(self) -> dict[Any, Any]:
        return {"tipe" : "literal", "tipeNilai" : self.tipe.__repr__(), "nilai" : self.nilai}
        # return {"tipe numerik" : self.tipe.name, "nilai numerik" : self.nilai}

class nodeInvalidEkspresi(nodeEkspresi):
    """
    node buat ngewakilin ekspresi invalid boolean
    """
    def __init__(self, p_token : tokenClass, p_tipedata : datatypes)->None:
        super().__init__(p_token.baris, p_token.kolom, p_tipedata)


class nodeParameter(nodeEkspresi):
    """
    node buat ngecontain parameter
    """
    def __init__(self, p_baris: int, p_kolom: int, p_nama: str = "", p_tipe: datatypes = TIPEDATA_NULL) -> None:
        self.tipe : datatypes = p_tipe
        self.nama : str = p_nama
        self.tipedata : datatypes = TIPEDATA_NULL
        self.nilaiDefault : nodeEkspresi | None = None
        super().__init__(p_baris, p_kolom, self.tipe)
    
    def getDatas(self) -> dict[Any, Any]:
        if(self.nilaiDefault is None):
            return {"tipe" : "deklarasiParameter", "nama" : self.nama, "tipeParam" : self.tipedata.__repr__(), "nilaiDefault" : "NULL"}

        else:
            return {"tipe" : "deklarasiParameter", "nama" : self.nama, "tipeParam" : self.tipedata.__repr__(), "nilaiDefault" : self.nilaiDefault.getDatas()}

    def getRealDatas(self)->dict[Any, Any]:
        if(self.nilaiDefault is None):
            return {"tipe" : "deklarasiParameter", "nama" : self.nama, "tipeParam" : self.tipedata, "nilaiDefault" : "NULL"}

        else:
            return {"tipe" : "deklarasiParameter", "nama" : self.nama, "tipeParam" : self.tipedata, "nilaiDefault" : self.nilaiDefault.getRealDatas()}

class nodeBiner(nodeEkspresi):
    """
    node buat ngecontain operasi biner
    """
    def __init__(self, p_operand1 : nodeEkspresi, p_operatorToken : tokenClass, p_operand2 : nodeEkspresi)->None:
        self.operand1 : nodeEkspresi = p_operand1
        self.operator : str = p_operatorToken.nilai
        self.operand2 : nodeEkspresi = p_operand2
        self.tipeData : datatypes 
    
        if(self.operand1.tipe==self.operand2.tipe or (self.operand1.tipe==TIPEDATA_NULL or self.operand2.tipe==TIPEDATA_NULL)):
            self.tipeData = self.operand1.tipe
            
        else:
            raise Exception("ngejumlahin tpi tipedatanya beda")
        
        super().__init__(p_operatorToken.baris, p_operatorToken.kolom, self.tipeData)
    
    def getDatas(self) -> dict[Any, Any]:
        return {"tipe" : "oprBiner", "operator" : self.operator, "kiri" : self.operand1.getDatas(), "kanan" : self.operand2.getDatas()}
        # return {"operator" : self.operator, "operand1" : self.operand1.getDatas(), "operand2" : self.operand2.getDatas()}

class nodeBikinVariabel(nodeStatement):
    """
    node representasi utk bikin variabel
    """
    def __init__(self, p_baris : int, p_kolom : int)->None:
        super().__init__(p_baris, p_kolom)
        
        self.namaVariabel : str = ""
        self.tipedataVariabel : datatypes = TIPEDATA_NULL
        # self.tipedataVariabel : Ttype = Ttype.T_NULL
        self.nilaiVariabel : nodeEkspresi = nodeEkspresi(p_baris, p_kolom, self.tipedataVariabel)

    def getDatas(self) ->dict[str, Any]:
        return {"tipe" : "deklarasiVariabel", "nama" : self.namaVariabel, "tipeNilai" : self.tipedataVariabel.__repr__(), "nilai" : self.nilaiVariabel.getDatas()}
        # return {"nama variabel" : self.namaVariabel, "tipedata variabel" : self.tipedataVariabel.name, "nilai variabel" : self.nilaiVariabel.getDatas(),}

class nodePanggilFungsi(nodeEkspresi):
    """
    node representasi utk manggil fungsi
    """
    def __init__(self, p_baris: int, p_kolom: int, p_namaFungsi: tokenClass, p_parameterInput: list[nodeEkspresi] | None = None) -> None:
        super().__init__(p_baris, p_kolom, TIPEDATA_NULL)
        self.namaFungsi : tokenClass = p_namaFungsi
        if p_parameterInput is None:
            self.parameterInput = []
        else:
            # if(not p_parameterInput is None):
            self.parameterInput : list[nodeEkspresi] = p_parameterInput
        # self.parameterInput : list[nodeEkspresi] = p_parameterInput
    
    def getDatas(self) -> dict[str, Any]:
        temp1 : list[dict[str, Any]] = []
        for input in self.parameterInput:
            temp1.append(input.getDatas())
        return {"tipe" : "panggilFungsi", "nama" : self.namaFungsi.nilai, "parameter" : temp1}
        # return {"panggil fungsi" : self.namaFungsi.nilai, "parameter input" : temp1}
    
    def __repr__(self) -> str:
        return str(self.getDatas())
        

class nodeBikinFungsi(nodeStatement):
    """
    node representasi utk bikin fungsi
    """
    def __init__(self, p_baris : int, p_kolom : int, p_namaFungsi : str = "", p_tipedataFungsi : str = "")->None:
        super().__init__(p_baris, p_kolom)
        
        self.namaFungsi : str = p_namaFungsi
        self.tipedataFungsi : str = p_tipedataFungsi
        self.parameterFungsi : list[nodeParameter] = []
        self.isiFungsi : list[nodeClass] = []
    
    def getDatas(self) -> dict[Any, Any]:
        # tempStore : dict[str, Any] = {}
        temp1 : list[dict[str, Any]] = []
        temp2 : list[dict[str, Any]] = []
        
        for node in self.isiFungsi:
            temp1.append(node.getDatas())
            
        # tempStore2 : dict[str, Any] = {}
        for nodeParam in self.parameterFungsi:
            temp2.append(nodeParam.getDatas())
            
        return {"tipe" : "deklarasiFungsi", "nama" : self.namaFungsi, "tipeReturn" : self.tipedataFungsi, "parameter" : temp2, "badan" : temp1}
    
    def registerFungsi(self)->dict[str, Any]:
        temp2 : list[dict[str, Any]] = []
        for nodeParam in self.parameterFungsi:
            temp2.append(nodeParam.getRealDatas())
        return {"nama" : self.namaFungsi, "tipeReturn" : self.tipedataFungsi, "parameter" : temp2}
    
    def evaluasi(self)->None:
        print("nama gwh:",hex(id(self)))