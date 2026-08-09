from __future__ import annotations
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
from metadata.datatypeClass import TIPEDATA_VOID
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
    
    def getRealDatas(self)->nodeClass:
        return self

class nodeRoot(nodeClass):
    """
    node buat representasi dari scope root
    """
    def __init__(self, p_baris : int = 0, p_kolom : int = 0)->None:
        self.baris : int = p_baris
        self.kolom : int = p_kolom
        self.nodeContainer : list[nodeClass] = []
        super().__init__(p_baris, p_kolom)
    

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
    
    # def __repr__(self) -> str:
    #     return f"{self.tipe}"
    
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
    
    # def getRealDatas(self)->dict[str, Any]:
    #     return {"tipe" : "literal", "tipeNilai" : self.tipe, "nilai" : self.nilai}

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

class nodeBalikin(nodeStatement):
    def __init__(self, p_baris: int, p_kolom: int) -> None:
        self.returnEkspresi : nodeEkspresi
        super().__init__(p_baris, p_kolom)
    
    def getDatas(self) -> dict[Any, Any]:
        return {"tipe" : "pernyataanReturn", "nilai" : self.returnEkspresi.getDatas()}

class nodeIdentifier(nodeEkspresi):
    """
    node buat ngecontain identifier
    """
    def __init__(self, p_token : tokenClass) -> None:
        self.identifierToken : str = p_token.nilai
        super().__init__(p_token.baris, p_token.kolom, TIPEDATA_NULL)
    
    def getDatas(self) -> dict[Any, Any]:
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

class nodeBiner(nodeEkspresi):
    """
    node buat ngecontain operasi biner
    """
    def __init__(self, p_operand1 : nodeEkspresi, p_operatorToken : tokenClass, p_operand2 : nodeEkspresi)->None:
        self.operand1 : nodeEkspresi = p_operand1
        self.operator : str = p_operatorToken.nilai
        self.operand2 : nodeEkspresi = p_operand2
        self.tipeData : datatypes = self.operand1.tipe
    
        super().__init__(p_operatorToken.baris, p_operatorToken.kolom, self.tipeData)
    
    def getDatas(self) -> dict[Any, Any]:
        return {"tipe" : "oprBiner", "operator" : self.operator, "kiri" : self.operand1.getDatas(), "kanan" : self.operand2.getDatas()}

class nodeBanding(nodeEkspresi):
    """
    node buat ngecontain operasi biner
    """
    def __init__(self, p_operand1 : nodeEkspresi, p_operatorToken : tokenClass, p_operand2 : nodeEkspresi)->None:
        self.operand1 : nodeEkspresi = p_operand1
        self.operator : tokenClass = p_operatorToken
        self.operand2 : nodeEkspresi = p_operand2
        self.tipeData : datatypes = self.operand1.tipe
    
        super().__init__(p_operatorToken.baris, p_operatorToken.kolom, self.tipeData)
    
    def getDatas(self) -> dict[Any, Any]:
        return {"tipe" : "oprBanding", "operator" : self.operator.nilai, "kiri" : self.operand1.getDatas(), "kanan" : self.operand2.getDatas()}

class nodeAksesProperti(nodeEkspresi):
    def __init__(self, p_baris: int, p_kolom: int, p_tipe: datatypes) -> None:
        super().__init__(p_baris, p_kolom, p_tipe)
        self.objek : nodeIdentifier | nodeAksesProperti
        self.properti : nodeIdentifier
    
    def getDatas(self) -> dict[str, Any]:
        return {"tipe" : "aksesProperti", "properti" : self.properti.getDatas(), "objek" : self.objek.getDatas()}

class nodePenugasan(nodeStatement):
    def __init__(self, p_baris: int, p_kolom: int) -> None:
        super().__init__(p_baris, p_kolom)
        self.referensi : nodeAksesProperti | nodeIdentifier
        self.ekspresi : nodeEkspresi
    
    def getDatas(self) -> dict[str, Any]:
        return {"tipe" : "statementPenugasan", "referensi" : self.referensi.getDatas(), "ekspresi" : self.ekspresi.getDatas()}

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

class nodeKalau(nodeStatement):
    def __init__(self, p_baris: int, p_kolom: int) -> None:
        super().__init__(p_baris, p_kolom)
        self.kondisi : nodeEkspresi
        self.isiKalau : list[nodeClass] = []
        self.listElif : list[nodeKalau] = []
        self.isiElse : list[nodeClass] = []
    
    def getDatas(self) -> dict[str, Any]:
        isiKalau : list[dict[str, Any]] = []
        listElif : list[dict[str, Any]] = []
        isiElse : list[dict[str, Any]] = []
        
        if(len(self.isiKalau)>0):
            for isi in self.isiKalau:
                isiKalau.append(isi.getDatas())
                
        if(len(self.listElif)>0):
            for elife in self.listElif:
                listElif.append(elife.getDatas())
                
        if(len(self.isiElse)>0):
            for isi in self.isiElse:
                isiElse.append(isi.getDatas())
                
        return {"tipe" : "statementKalau", "kondisi" : self.kondisi.getDatas(), "isi" : isiKalau, "elif" : listElif, "else" : isiElse}

class nodeBikinFungsi(nodeStatement):
    """
    node representasi utk bikin fungsi
    """
    def __init__(self, p_baris : int, p_kolom : int, p_namaFungsi : str = "", p_tipedataFungsi : datatypes = TIPEDATA_VOID)->None:
        super().__init__(p_baris, p_kolom)
        
        self.namaFungsi : str = p_namaFungsi
        self.tipedataFungsi : datatypes = p_tipedataFungsi
        self.parameterFungsi : list[nodeParameter] = []
        self.isiFungsi : list[nodeClass] = []
    
    def getDatas(self) -> dict[str, Any]:
        # tempStore : dict[str, Any] = {}
        temp1 : list[dict[str, Any]] = []
        temp2 : list[dict[str, Any]] = []
        
        for node in self.isiFungsi:
            temp1.append(node.getDatas())
            
        # tempStore2 : dict[str, Any] = {}
        for nodeParam in self.parameterFungsi:
            temp2.append(nodeParam.getDatas())
            
        return {"tipe" : "deklarasiFungsi", "nama" : self.namaFungsi, "tipeReturn" : self.tipedataFungsi.__repr__(), "parameter" : temp2, "badan" : temp1}

    def evaluasi(self)->None:
        print("nama gwh:",hex(id(self)))

class nodePerulanganSelama(nodeStatement):
    def __init__(self, p_baris: int, p_kolom: int) -> None:
        super().__init__(p_baris, p_kolom)
        self.kondisi : nodeEkspresi = nodeEkspresi(-1, -1, TIPEDATA_NULL)
        self.isiLoop : list[nodeClass] = []
    
    def getDatas(self) -> dict[str, Any]:
        temp1 : list[dict[str, Any]] = []
        
        for node in self.isiLoop:
            temp1.append(node.getDatas())
            
        return {"tipe" : "statementPerulanganSelama", "kondisi" : self.kondisi.getDatas(), "badan" : temp1}