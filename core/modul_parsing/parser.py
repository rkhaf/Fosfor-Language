from data_language.dataFormat import Token
from modul_parsing.AST import ASTClass
from data_language import tataBahasa as tb
from pohon import node
# from data_language import keywords
from errorHandler import errorHandlerClass
from data_language import pola
from data_language import keywords as kyrwd
from enum import Enum

class states(Enum):
    default = 0,
    variabel = 1

class parserClass:
    def __init__(self, p_errorHandlerReference : errorHandlerClass)->None:
        self.errorHandlerObjek : errorHandlerClass = p_errorHandlerReference
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

    def parseFaktor(self)->node.nodeEkspresi:
        # print("PARSE FAKTOR")
        if(self.tokenSkrg.tipe==tb.T_LITERAL_FLOAT or self.tokenSkrg.tipe==tb.T_LITERAL_INT):
            tempToken = self.tokenSkrg
            if(self.tokenDepan.tipe in kyrwd.operatorList.values() or self.tokenDepan.tipe in kyrwd.literalList.keys() or self.tokenDepan.tipe in [tb.T_PRTS_KIRI, tb.T_PRTS_KNAN]):
            # if(self.tokenDepan.tipe in kyrwd.keywordList or self.tokenDepan.tipe==tb.T_IDTF):
                self.maju()
            return node.nodeNomor(tempToken)
        
        elif(self.tokenSkrg.tipe==tb.T_LITERAL_STR):
            tempToken = self.tokenSkrg
            if(self.tokenDepan.tipe in kyrwd.operatorList.values() or self.tokenDepan.tipe in kyrwd.literalList.keys() or self.tokenDepan.tipe in [tb.T_PRTS_KIRI, tb.T_PRTS_KNAN]):
                self.maju()
            return node.nodeString(tempToken)
        
        elif(self.tokenSkrg.tipe==tb.T_LITERAL_BOOL):
            tempToken = self.tokenSkrg
            if(self.tokenDepan.tipe in kyrwd.operatorList.values() or self.tokenDepan.tipe in kyrwd.literalList.keys() or self.tokenDepan.tipe in [tb.T_PRTS_KIRI, tb.T_PRTS_KNAN]):
                self.maju()
            return node.nodeBoolean(tempToken)

        else:
            if(self.tokenSkrg.tipe==tb.T_PRTS_KIRI):
                self.maju()
                nodee = self.parseEkspresi()
                if(self.tokenSkrg.tipe==tb.T_PRTS_KNAN):
                    if(self.tokenDepan.tipe in kyrwd.operatorList.values() or self.tokenDepan.tipe in kyrwd.literalList.keys() or self.tokenDepan.tipe in [tb.T_PRTS_KIRI, tb.T_PRTS_KNAN]):
                        self.maju()
                    return nodee
                else:
                    print(self.tokenSkrg.tipe)
                    raise Exception("ada yg aneh")
                    
            else:
                raise Exception("ada yg aneh")
        
    def parseTerm(self)->node.nodeEkspresi:
        # print("PARSE TERM")
        nodeKiri = self.parseFaktor()
        
        while self.tokenSkrg.tipe == tb.T_MULT or self.tokenSkrg.tipe == tb.T_DIVE:
            operator = self.tokenSkrg
            self.maju()
            nodeKanan=self.parseFaktor()
            nodeKiri = node.nodeBiner(nodeKiri, operator, nodeKanan)
        return nodeKiri
    
    def parseEkspresi(self)->node.nodeEkspresi:
        # print("PARSE EKSPRESI")
        nodeKiri = self.parseTerm()
        
        while self.tokenSkrg.tipe==tb.T_PLUS or self.tokenSkrg.tipe==tb.T_MINS:
            operator = self.tokenSkrg
            self.maju()
            nodeKanan = self.parseTerm()
            nodeKiri = node.nodeBiner(nodeKiri, operator, nodeKanan)
        return nodeKiri
    

    def parseBikinVariabel(self)->None:
        self.maju(2)
        tempNode : node.nodeBikinVariabel = node.nodeBikinVariabel(self.tokenSkrg.baris, self.tokenSkrg.kolom)
        state : int = 0
        # self.maju()
        while self.idxIterator<len(self.fullToken):
            if(self.tokenSkrg.tipe!=tb.T_DLMR):
                if(state==0):
                    if(self.tokenSkrg.tipe==tb.T_NMNY):
                        state=1
                        self.maju()
                        
                    elif(self.tokenSkrg.tipe==tb.T_TPNY):
                        state=2
                        self.maju()
                        
                    elif(self.tokenSkrg.tipe==tb.T_NLNY):
                        state=3
                        self.maju()
                        
                elif(state==1):
                    if(self.tokenSkrg.tipe==tb.T_IDTF):
                        if(len(tempNode.namaVariabel)<=0):
                            tempNode.namaVariabel = self.tokenSkrg.nilai
                            self.maju()
                        else:
                            self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=2, p_baris=self.tokenSkrg.baris)
                            self.maju()
                    elif(self.tokenSkrg.tipe==tb.T_NMNY):
                        self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=4, p_baris=self.tokenSkrg.baris)
                        self.maju()
                    elif(self.tokenSkrg.tipe in [tb.T_TPNY, tb.T_TPNY]):
                        state=0
                    else:
                        tempNode.namaVariabel+= self.tokenSkrg.nilai
                        self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=3, p_baris=self.tokenSkrg.baris)
                        self.maju()
                    # self.maju()
            
                elif(state==2):
                    tempNode.tipedataVariabel = self.tokenSkrg.nilai
                    self.maju()
                    state=0
                
                elif(state==3):
                    tempNode.nilaiVariabel = self.parseEkspresi()
                    self.maju()
                    state=0
            else:
                if(len(tempNode.namaVariabel)<=0):
                    self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=1, p_baris=self.tokenSkrg.baris)

                self.ASTObjek.addNode(tempNode)
                break
            
            # if(self.tokenSkrg.tipe!=tb.T_DLMR):
            #     if(self.tokenSkrg.tipe==tb.T_NMNY):
            #         if(len(tempNode.namaVariabel)<=0):tempNode.namaVariabel = self.tokenDepan.nilai
            #         else:self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=2, p_baris=self.tokenSkrg.baris)
            #         if(self.tokenDepan.tipe!=tb.T_IDTF):self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=3, p_baris=self.tokenSkrg.baris)
            #         self.maju()
                    
            #     elif(self.tokenSkrg.tipe==tb.T_TPNY):
            #         # print("tipe varnya : ",self.tokenDepan.nilai)
            #         tempNode.tipedataVariabel = self.tokenDepan.nilai
            #         self.maju()
                    
            #     elif(self.tokenSkrg.tipe==tb.T_NLNY):
            #         self.maju()
            #         tempNode.nilaiVariabel = self.parseEkspresi()
            #         # print("nilai varnya : ",tempNode)
            #         # self.maju()
            #     self.maju()
            # else:
            #     if(len(tempNode.namaVariabel)<=0):
            #         self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=1, p_baris=self.tokenSkrg.baris)

            #     self.ASTObjek.addNode(tempNode)
            #     break
            # pass
        
    def proses(self, p_tokens : list[Token])->None:
        # tokenDepan : Token = p_tokens[idxIterator+1]
        self.fullToken = p_tokens
        while self.idxIterator<len(self.fullToken)-1:
            self.refresh()
            match [self.tokenSkrg.tipe, self.tokenDepan.tipe]:
                case pola.POLA_BIKIN_VARIABEL:
                    parsingBikinVariabel : None = self.parseBikinVariabel()
                    # if(type(parsingBikinVariabel) is str):
                    #     return parsingBikinVariabel
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
        # self.ASTObjek.printTree()
    
    # def ambilPohon(self)