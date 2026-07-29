# from llvmFolder.library import LLVM_PRIMITIVE_TYPES
from data_language.tokens import tokenClass
# from data_language import tataBahasa as tb
from data_language.tokens import tokenType as Ttype
# from data_language.keywords import primitiveList as PL
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
    def __init__(self, p_baris : int, p_kolom : int, p_tipe : Ttype)->None:
        super().__init__(p_baris, p_kolom)
        self.tipe : Ttype = p_tipe
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

# class nodeBlock(nodeStatement):
#     """
#     node container utk contain node
#     """
#     def __init__(self, p_baris : int, p_kolom : int)->None:
#         super().__init__(p_baris, p_kolom)
#         self.isiBlock : list[nodeClass] = []
    
#     def getDatas(self) -> dict[Any, Any]:
#         tempStore : dict[str, Any] = {}
#         for node in self.isiBlock:
#             test = list(node.getDatas().keys())
#             test2 = list(node.getDatas().values())
#             test3 = test[0]
#             test4 = test2[0]
#             tempStore[test3] = test4
#         return {"isi block" : tempStore}

class nodeNomor(nodeEkspresi):
    """
    node buat ngecontain numerik
    """
    def __init__(self, p_token : tokenClass)->None:
        assert p_token.tipe==Ttype.T_LITERAL_FLOAT or p_token.tipe==Ttype.T_LITERAL_INT, "ERRORDEV: nodeNomor hrusnya cmn nerima token numerik"

        super().__init__(p_token.baris, p_token.kolom, p_token.tipe)
        self.tipe : Ttype = p_token.tipe
        self.nilai : str = p_token.nilai
    
    def getDatas(self) -> dict[Any, Any]:
        return {"tipe" : "literal", "tipeNilai" : self.tipe.name, "nilai" : self.nilai}
        # return {"tipe numerik" : self.tipe.name, "nilai numerik" : self.nilai}

class nodeString(nodeEkspresi):
    """
    node buat ngecontain string
    """
    def __init__(self, p_token : tokenClass)->None:
        assert p_token.tipe==Ttype.T_LITERAL_STR, "ERRORDEV: nodeString hrusnya cmn nerima token string"
        
        super().__init__(p_token.baris, p_token.kolom, p_token.tipe)
        self.tipe : Ttype = p_token.tipe
        self.nilai : str = p_token.nilai
    
    def getDatas(self) -> dict[Any, Any]:
        return {"tipe" : "literal", "tipeNilai" : self.tipe.name, "nilai" : self.nilai}
        # return {"tipe" : self.tipe.name, "nilai" : self.nilai}

class nodeBalikin(nodeStatement):
    def __init__(self, p_baris: int, p_kolom: int) -> None:
        self.returnEkspresi : nodeEkspresi
        super().__init__(p_baris, p_kolom)
    
    def getDatas(self) -> dict[Any, Any]:
        return {"tipe" : "pernyataanReturn", "nilai" : self.returnEkspresi.getDatas()}
        # return {"ngereturn : " : self.returnEkspresi.getDatas()}
        

class nodeIdentifier(nodeEkspresi):
    """
    node buat ngecontain identifier
    """
    def __init__(self, p_token : tokenClass, p_tipe: str="") -> None:
        self.identifierToken : tokenClass = p_token
        super().__init__(p_token.baris, p_token.kolom, Ttype.T_IDTF)
    
    def getDatas(self) -> dict[Any, Any]:
        # return {"tipe numerik" : self.tipe, "nilai numerik" : self.nilai}
        # return {self.identifierToken.tipe.name : self.identifierToken.nilai}
        return {"tipe" : "identifier", "nama" : self.identifierToken.nilai}
        
class nodeBoolean(nodeEkspresi):
    """
    node buat ngecontain boolean
    """
    def __init__(self, p_token : tokenClass)->None:
        assert p_token.tipe==Ttype.T_LITERAL_BOOL, "ERRORDEV: nodeBoolean hrusnya cmn nerima token string"
        
        super().__init__(p_token.baris, p_token.kolom, p_token.tipe)
        self.tipe : Ttype = p_token.tipe
        self.nilai : str = p_token.nilai
    
    def getDatas(self) -> dict[Any, Any]:
        return {"tipe" : "literal", "tipeNilai" : self.tipe.name, "nilai" : self.nilai}
        # return {"tipe numerik" : self.tipe.name, "nilai numerik" : self.nilai}

class nodeInvalidEkspresi(nodeEkspresi):
    """
    node buat ngewakilin ekspresi invalid boolean
    """
    def __init__(self, p_token : tokenClass)->None:
        super().__init__(p_token.baris, p_token.kolom, p_token.tipe)


class nodeParameter(nodeEkspresi):
    """
    node buat ngecontain parameter
    """
    def __init__(self, p_baris: int, p_kolom: int, p_tipe: str = "") -> None:
        self.tipe : Ttype = Ttype.T_NULL
        self.nama : str = ""
        self.tipedata : Ttype 
        self.nilaiDefault : nodeEkspresi | None = None
        super().__init__(p_baris, p_kolom, self.tipe)
    
    def getDatas(self) -> dict[Any, Any]:
        # tempKumpulanNama : list[str] = []
        # tempKumpulanTipedata : list[str] = []
        
        # for token in self.nama:
        #     tempKumpulanNama.append(token.nilai)
            
        # for token in self.tipedata:
        #     tempKumpulanTipedata.append(token.tipe)
        if(self.nilaiDefault is None):
            return {"tipe" : "deklarasiParameter", "nama" : self.nama, "tipeParam" : self.tipedata.name, "nilaiDefault" : "NULL"}
            # return {self.tipedata.name : [self.nama]}
        else:
            return {"tipe" : "deklarasiParameter", "nama" : self.nama, "tipeParam" : self.tipedata.name, "nilaiDefault" : self.nilaiDefault.getDatas()}
            # return {self.tipedata.name : [self.nama, self.nilaiDefault.getDatas()]}
            # return {self.tipedata : [self.nama, self.nilaiDefault.getDatas()]}
        # return {"list nama" : tempKumpulanNama, "list tipedatanya" : tempKumpulanTipedata}

class nodeBiner(nodeEkspresi):
    """
    node buat ngecontain operasi biner
    """
    def __init__(self, p_operand1 : nodeEkspresi, p_operatorToken : tokenClass, p_operand2 : nodeEkspresi)->None:
        self.operand1 : nodeEkspresi = p_operand1
        self.operator : str = p_operatorToken.nilai
        self.operand2 : nodeEkspresi = p_operand2
        self.tipeData : Ttype 
    
        if(self.operand1.tipe==self.operand2.tipe or self.operand1.tipe==Ttype.T_IDTF or self.operand2.tipe==Ttype.T_IDTF):
            # test = list(PL.values())
            # print(test)
            self.tipeData = self.operand1.tipe
            # print("sama",self.tipeData)
        else:
            raise Exception("ngejumlahin tpi tipedatanya beda")
        super().__init__(p_operatorToken.baris, p_operatorToken.kolom, self.tipeData)
        
    # def generateTipeData(self)->None:
        # pass
    
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
        self.tipedataVariabel : Ttype = Ttype.T_NULL
        self.nilaiVariabel : nodeEkspresi = nodeEkspresi(p_baris, p_kolom, self.tipedataVariabel)
    
    def getDatas(self) ->dict[str, Any]:
        return {"tipe" : "deklarasiVariabel", "nama" : self.namaVariabel, "tipeNilai" : self.tipedataVariabel.name, "nilai" : self.nilaiVariabel.getDatas()}
        # return {"nama variabel" : self.namaVariabel, "tipedata variabel" : self.tipedataVariabel.name, "nilai variabel" : self.nilaiVariabel.getDatas(),}

class nodePanggilFungsi(nodeEkspresi):
    """
    node representasi utk manggil fungsi
    """
    def __init__(self, p_baris: int, p_kolom: int, p_namaFungsi: tokenClass, p_parameterInput: list[nodeEkspresi] | None = None) -> None:
        super().__init__(p_baris, p_kolom, Ttype.T_NULL)
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
        tempStore : dict[str, Any] = {}
        temp1 : list[dict[str, Any]] = []
        temp2 : list[dict[str, Any]] = []
        
        for node in self.isiFungsi:
            temp1.append(node.getDatas())
            test = list(node.getDatas().keys())
            test2 = list(node.getDatas().values())
            test3 = test[0]
            test4 = test2[0]
            tempStore[test3] = test4
            # print("PRINTING1.1",node.getDatas())
            # print("PRINTING1.2",test)
            # print("PRINTING1.2",test2)
            
        tempStore2 : dict[str, Any] = {}
        for nodeParam in self.parameterFungsi:
            temp2.append(nodeParam.getDatas())
            test = list(nodeParam.getDatas().keys())
            test2 = list(nodeParam.getDatas().values())
            test3 = test[0]
            test4 = test2[0][0]
            tempStore2[test4] = test3 
            # print("PRINTING2",test2)
        # return {"isi fungsi" : tempStore}
        pass
        return {"tipe" : "deklarasiFungsi", "nama" : self.namaFungsi, "tipeReturn" : self.tipedataFungsi, "parameter" : temp2, "badan" : temp1}