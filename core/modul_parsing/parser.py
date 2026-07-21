from data_language.dataFormat import Token
from modul_parsing.AST import ASTClass
from data_language import tataBahasa as tb
from pohon import node
# from data_language import keywords
from data_language import pola
from enum import Enum

class states(Enum):
    default = 0,
    variabel = 1

class parserClass:
    def __init__(self)->None:
        self.ASTObjek : ASTClass = ASTClass()
        self.fullToken : list[Token]
        self.tokenSkrg : Token
        self.tokenDepan : Token
        self.idxIterator : int = 0
        self.state : states = states.default
        pass
    
    def maju(self, p_nilai : int = 1):
        self.idxIterator+=p_nilai
        self.refresh()
        pass
    
    def refresh(self)->None:
        self.tokenSkrg = self.fullToken[self.idxIterator]
        if(self.idxIterator<len(self.fullToken)-1):
            self.tokenDepan = self.fullToken[self.idxIterator+1]
        pass
    
    def getNextToken(self, p_tokenTipe : str)->Token | None:
        if(self.tokenSkrg.tipe==p_tokenTipe):
            return self.tokenDepan
    
    def parseLiteral(self)->node.nodeNomor | node.nodeString | node.nodeBoolean:
        if(self.tokenSkrg.tipe in [tb.T_LITERAL_INT, tb.T_LITERAL_FLOAT]):
            return node.nodeNomor(self.tokenSkrg)

        elif(self.tokenSkrg.tipe == tb.T_LITERAL_STR):
            return node.nodeString(self.tokenSkrg)
        
        elif(self.tokenSkrg.tipe == tb.T_LITERAL_BOOL):
            return node.nodeBoolean(self.tokenSkrg)
        
        else:
            raise AssertionError("eror ngeparse")

    def parseEkspresi(self)->node.nodeEkspresi:
        self.maju()
        # tempNode : node.nodeEkspresi = node.nodeEkspresi(self.tokenSkrg.baris, self.tokenSkrg.kolom)
        operandKiri : node.nodeEkspresi = self.parseLiteral()
        return operandKiri
        # operandKiri : node.nodeEkspresi | None = None
        # while self.idxIterator<len(self.fullToken)-1:
        #     print(self.tokenSkrg)
            # if(self.tokenSkrg.tipe in keywords.literalList.keys()):
                # operandKiri = self.parseLiteral()
                # if(type(temp) is node.nodeNomor):
                #     return node.nodeNomor(self.tokenSkrg)
                
                # return "idk"
                # pass
            # self.maju()
        # return "RRR"

    def parseBikinVariabel(self)->None:
        self.maju()
        tempNode : node.nodeBikinVariabel = node.nodeBikinVariabel(self.tokenSkrg.baris, self.tokenSkrg.kolom)
        # self.maju()
        while self.idxIterator<len(self.fullToken):
            if(self.tokenSkrg.tipe!=tb.T_DLMR):
                if(self.tokenSkrg.tipe==tb.T_NMNY):
                    # print("nama varnya : ",self.tokenDepan.nilai)
                    tempNode.namaVariabel = self.tokenDepan.nilai
                    self.maju()
                    
                elif(self.tokenSkrg.tipe==tb.T_TPNY):
                    # print("tipe varnya : ",self.tokenDepan.nilai)
                    tempNode.tipedataVariabel = self.tokenDepan.nilai
                    self.maju()
                    
                elif(self.tokenSkrg.tipe==tb.T_NLNY):
                    tempNode.nilaiVariabel = self.parseEkspresi()
                    # print("nilai varnya : ",tempNode)
                    # self.maju()
                self.maju()
            else:
                self.ASTObjek.addNode(tempNode)
                # print("DETAIL")
                # print(tempNode.baris,tempNode.kolom,tempNode.namaVariabel,tempNode.nilaiVariabel,tempNode.tipedataVariabel)
                break
            pass
        
    def proses(self, p_tokens : list[Token])->str | None:
        # tokenDepan : Token = p_tokens[idxIterator+1]
        self.fullToken = p_tokens
        while self.idxIterator<len(self.fullToken)-1:
            self.refresh()
            match [self.tokenSkrg.tipe, self.tokenDepan.tipe]:
                case pola.POLA_BIKIN_VARIABEL:
                    self.parseBikinVariabel()
                    pass
                
                case _:
                    pass
                    
            if(self.idxIterator<len(self.fullToken)-1):
                self.maju()
                
            
            # match [self.tokenSkrg.tipe, self.tokenDepan.tipe]:
            #     case pola.POLA_BIKIN_VARIABEL:
            #         print("ada yg bikin variabel nih")
            #         if(self.tokenSkrg.tipe==tb.T_NMNY):
            #             print("  namanya: ",self.tokenDepan.nilai)
            #         self.maju()
                
            #     case _:
            #         print(self.tokenSkrg.tipe, self.tokenDepan.tipe)
            #         pass
                
            # print(self.tokenSkrg)
            # self.maju()
        self.ASTObjek.printTree()
    
    # def ambilPohon(self)