# from llvmFolder.library import LLVM_PRIMITIVE_TYPES
from data_language.dataFormat import Token
from data_language import tataBahasa as tb
from data_language.keywords import primitiveList as PL
from typing import Any

class nodeClass:
    """
    node sepuh yg jadi tumpuan seluruh node
    """
    def __init__(self, p_baris : int, p_kolom : int)->None:
        self.baris : int = p_baris
        self.kolom : int = p_kolom
    
    def getDatas(self)->dict[str, Any]:
        return {}

class nodeError(nodeClass):
    """
    buat bahan return-an klo semisal ada node yg gk valid
    """
    
class nodeEkspresi(nodeClass):
    """
    nodeParent buat node yg bisa ngereturn di kodenya
    """
    def __init__(self, p_baris : int, p_kolom : int, p_tipe : str)->None:
        super().__init__(p_baris, p_kolom)
        self.tipe : str = p_tipe
        pass

class nodeStatement(nodeClass):
    """
    nodeParent buat node yg gak return apa2 di kodenya
    """
    def __init__(self, p_baris : int, p_kolom : int)->None:
        super().__init__(p_baris, p_kolom)
        pass

class nodeBlock(nodeStatement):
    """
    node container utk contain node
    """
    def __init__(self, p_baris : int, p_kolom : int, p_namaVariabel : str, p_tipedataVariabel : str)->None:
        super().__init__(p_baris, p_kolom)
        self.isiBlock : list[nodeClass] = []

class nodeNomor(nodeEkspresi):
    """
    node buat ngecontain numerik
    """
    def __init__(self, p_token : Token)->None:
        assert p_token.tipe==tb.T_LITERAL_FLOAT or p_token.tipe==tb.T_LITERAL_INT, "ERRORDEV: nodeNomor hrusnya cmn nerima token numerik"

        super().__init__(p_token.baris, p_token.kolom, p_token.tipe)
        self.tipe : str = p_token.tipe
        self.nilai : str = p_token.nilai
    
    def getDatas(self) -> dict[str, Any]:
        return {"tipe numerik" : self.tipe, "nilai numerik" : self.nilai}

class nodeString(nodeEkspresi):
    """
    node buat ngecontain string
    """
    def __init__(self, p_token : Token)->None:
        assert p_token.tipe==tb.T_LITERAL_STR, "ERRORDEV: nodeString hrusnya cmn nerima token string"
        
        super().__init__(p_token.baris, p_token.kolom, p_token.tipe)
        self.tipe : str = p_token.tipe
        self.nilai : str = p_token.nilai
    
    def getDatas(self) -> dict[str, Any]:
        return {"tipe numerik" : self.tipe, "nilai numerik" : self.nilai}
        
class nodeBoolean(nodeEkspresi):
    """
    node buat ngecontain boolean
    """
    def __init__(self, p_token : Token)->None:
        assert p_token.tipe==tb.T_LITERAL_BOOL, "ERRORDEV: nodeBoolean hrusnya cmn nerima token string"
        
        super().__init__(p_token.baris, p_token.kolom, p_token.tipe)
        self.tipe : str = p_token.tipe
        self.nilai : str = p_token.nilai
    
    def getDatas(self) -> dict[str, Any]:
        return {"tipe numerik" : self.tipe, "nilai numerik" : self.nilai}

class nodeBiner(nodeEkspresi):
    """
    node buat ngecontain operasi biner
    """
    def __init__(self, p_operand1 : nodeEkspresi, p_operatorToken : Token, p_operand2 : nodeEkspresi)->None:
        self.operand1 : nodeEkspresi = p_operand1
        self.operator : str = p_operatorToken.nilai
        self.operand2 : nodeEkspresi = p_operand2
        self.tipeData : str = ""
    
        if(self.operand1.tipe==self.operand2.tipe):
            test = list(PL.values())
            print(test)
            self.tipeData = self.operand1.tipe
            # print("sama",self.tipeData)
        else:
            raise Exception("ngejumlahin tpi tipedatanya beda")
        super().__init__(p_operatorToken.baris, p_operatorToken.kolom, self.tipeData)
        
    # def generateTipeData(self)->None:
        # pass
    
    def getDatas(self) -> dict[str, Any]:
        return {"[OPERASI_BINER] : operand1" : self.operand1.getDatas(),"operator" : self.operator,"operand2" : self.operand2.getDatas()}

class nodeBikinVariabel(nodeStatement):
    """
    node representasi utk bikin variabel
    """
    def __init__(self, p_baris : int, p_kolom : int)->None:
        super().__init__(p_baris, p_kolom)
        
        self.namaVariabel : str = ""
        self.tipedataVariabel : str = ""
        self.nilaiVariabel : nodeEkspresi
    
    def getDatas(self) ->dict[str, Any]:
        return {"nama variabel" : self.namaVariabel, "tipedata variabel" : self.tipedataVariabel, "nilai variabel" : self.nilaiVariabel.getDatas(),}

class nodeBikinFungsi(nodeStatement):
    """
    node representasi utk bikin fungsi
    """
    def __init__(self, p_baris : int, p_kolom : int, p_namaFungsi : str, p_tipedataFungsi : str)->None:
        super().__init__(p_baris, p_kolom)
        
        self.namaVariabel : str = ""
        self.namaFungsi : str = p_namaFungsi
        self.tipedataFungsi : str = p_tipedataFungsi
        self.isiFungsi : nodeBlock