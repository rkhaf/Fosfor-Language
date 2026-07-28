# from core.data_language.tokens import Token
from data_language.tokens import tokenType
from data_language.tokens import tokenClass
from modul_parsing.AST import ASTClass
# from data_language import tataBahasa as tb
from data_language import grammar
from pohon import node
# from data_language import keywords
from errorHandler import errorHandlerClass
from data_language import pola
# from data_language import keywords as kyrwd
from data_language.tokens import tokenType as Ttype
from enum import Enum

class states(Enum):
    default = 0,
    variabel = 1

class parserClass:
    def __init__(self, p_errorHandlerReference : errorHandlerClass)->None:
        self.errorHandlerObjek : errorHandlerClass = p_errorHandlerReference
        self.ASTObjek : ASTClass = ASTClass()
        self.fullToken : list[tokenClass]
        self.tokenSkrg : tokenClass
        self.tokenDepan : tokenClass
        self.tokenBlkng : tokenClass
        self.idxIterator : int = 0
        self.state : states = states.default
        self.parseEkspresiInvalidFlag : bool = False
        self.punyaEntryPoint : bool = False
        pass
    
    def maju(self, p_nilai : int = 1):
        self.idxIterator+=p_nilai
        self.refresh()
        # if(self.idxIterator>=9):
        #     raise Exception("STOPPER1")
        pass
    
    def mundur(self, p_nilai : int = 1):
        self.idxIterator-=p_nilai
        self.refresh()
        # if(self.idxIterator>=9):
        #     raise Exception("STOPPER1")
        pass
    
    def refresh(self)->None:
        self.tokenSkrg = self.fullToken[self.idxIterator]
        self.tokenBlkng= self.fullToken[self.idxIterator-1]
        if(self.idxIterator<len(self.fullToken)-1):
            self.tokenDepan = self.fullToken[self.idxIterator+1]
        pass
    
    def getNextToken(self, p_tokenTipe : Ttype)->tokenClass | None:
        if(self.tokenSkrg.tipe==p_tokenTipe):
            return self.tokenDepan
    
    def parseLiteral(self)->node.nodeNomor | node.nodeString | node.nodeBoolean:
        if(self.tokenSkrg.tipe in [Ttype.T_LITERAL_INT, Ttype.T_LITERAL_FLOAT]):
            return node.nodeNomor(self.tokenSkrg)

        elif(self.tokenSkrg.tipe == Ttype.T_LITERAL_STR):
            return node.nodeString(self.tokenSkrg)
        
        elif(self.tokenSkrg.tipe == Ttype.T_LITERAL_BOOL):
            return node.nodeBoolean(self.tokenSkrg)
        
        else:
            raise AssertionError("eror ngeparse")

    def parseFaktor(self)->node.nodeEkspresi | node.nodeInvalidEkspresi:
        # print("PARSE FAKTOR")
        if(self.tokenSkrg.tipe==Ttype.T_LITERAL_FLOAT or self.tokenSkrg.tipe==Ttype.T_LITERAL_INT):
            if(not self.parseEkspresiInvalidFlag):
                tempToken = self.tokenSkrg
                if(self.tokenDepan.tipe in grammar.operatorList.values() or self.tokenDepan.tipe in [Ttype.T_PRTS_KIRI, Ttype.T_PRTS_KNAN]):
                # if(self.tokenDepan.tipe in grammar.keywordList or self.tokenDepan.tipe==Ttype.T_IDTF):
                    if(self.idxIterator==len(self.fullToken)-1):
                        tempLastValidToken = self.fullToken[self.idxIterator]
                        self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=9, p_baris=tempLastValidToken.baris, p_kolom=tempLastValidToken.kolom)
                    else:
                        self.maju()
                        pass
                elif(self.tokenDepan.tipe in grammar.literalList.keys() and not self.idxIterator==len(self.fullToken)-1):
                    self.parseEkspresiInvalidFlag=True
                    self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=12, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenDepan.nilai)
                    if(self.idxIterator==len(self.fullToken)-1):
                        
                        tempLastValidToken = self.fullToken[self.idxIterator]
                        self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=9, p_baris=tempLastValidToken.baris, p_kolom=tempLastValidToken.kolom)
                    else:
                        self.maju()
                        pass
                return node.nodeNomor(tempToken)
            else:
                return node.nodeInvalidEkspresi(self.tokenSkrg)
        
        elif(self.tokenSkrg.tipe==Ttype.T_LITERAL_STR):
            if(not self.parseEkspresiInvalidFlag):
                tempToken = self.tokenSkrg
                if(self.tokenDepan.tipe in grammar.operatorList.values() or self.tokenDepan.tipe in grammar.literalList.keys() or self.tokenDepan.tipe in [Ttype.T_PRTS_KIRI, Ttype.T_PRTS_KNAN]):
                    self.maju()
                return node.nodeString(tempToken)
            else:
                return node.nodeInvalidEkspresi(self.tokenSkrg)
        
        elif(self.tokenSkrg.tipe==Ttype.T_LITERAL_BOOL):
            if(not self.parseEkspresiInvalidFlag):
                tempToken = self.tokenSkrg
                if(self.tokenDepan.tipe in grammar.operatorList.values() or self.tokenDepan.tipe in grammar.literalList.keys() or self.tokenDepan.tipe in [Ttype.T_PRTS_KIRI, Ttype.T_PRTS_KNAN]):
                    self.maju()
                return node.nodeBoolean(tempToken)
            else:
                return node.nodeInvalidEkspresi(self.tokenSkrg)

        elif(self.tokenSkrg.tipe==Ttype.T_IDTF):
            if(not self.parseEkspresiInvalidFlag):
                tempToken = self.tokenSkrg
                # if(self.tokenDepan.tipe in grammar.operatorList.values() or self.tokenDepan.tipe in grammar.literalList.keys() or self.tokenDepan.tipe in [Ttype.T_PRTS_KIRI, Ttype.T_PRTS_KNAN]):
                if(self.tokenDepan.tipe in grammar.operatorList.values() or self.tokenDepan.tipe in [Ttype.T_PRTS_KIRI, Ttype.T_PRTS_KNAN]):
                    self.maju()
                elif(self.tokenDepan.tipe==Ttype.T_DLMR):
                    pass
                else:
                    print("yg ini")
                    self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=12, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenDepan.nilai)
                    # return node.nodeIdentifier(tempToken)
                    self.maju()
                    # pass
                return node.nodeIdentifier(tempToken)
            else:
                return node.nodeInvalidEkspresi(self.tokenSkrg)
        else:
            tempToken = self.fullToken[self.idxIterator-1]
            if(self.tokenSkrg.tipe==Ttype.T_PRTS_KIRI):
                self.maju()
                # if(not self.parseEkspresiInvalidFlag):
                nodee = self.parseEkspresi()
                if(self.tokenSkrg.tipe==Ttype.T_PRTS_KNAN): #type: ignore
                    if(self.tokenDepan.tipe in grammar.operatorList.values() or self.tokenDepan.tipe in grammar.literalList.keys() or self.tokenDepan.tipe in [Ttype.T_PRTS_KIRI, Ttype.T_PRTS_KNAN]):
                        self.maju()
                    return nodee
                else:
                    if(self.parseEkspresiInvalidFlag):
                        return node.nodeInvalidEkspresi(self.tokenSkrg)
                    else:
                    # print(self.tokenSkrg.tipe)
                        if(not self.parseEkspresiInvalidFlag):
                            # print("DEBUG 1")
                            self.parseEkspresiInvalidFlag=True
                            self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=13, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenDepan.nilai)
                            raise Exception("STOPPER1")
                            # return node.nodeInvalidEkspresi(self.tokenSkrg)
                        else:
                            raise Exception("INVALID")
                        # print("TEST2",self.tokenSkrg)
                        # raise Exception("ada yg aneh")
                    # raise Exception("ada yg aneh")
            else:
                # return node.nodeError
                # print("TEST",self.tokenSkrg)
                return node.nodeIdentifier(self.tokenSkrg)
                # raise Exception("ada yg aneh njr")
            # elif(self.tokenSkrg.tipe!=Ttype.T_IDTF):
            #     print("yg ini1",self.tokenSkrg.nilai)
            #     self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=7, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
            #     return node.nodeIdentifier(self.tokenSkrg)
            # else:
            #     print("yg ini2")
            #     self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=12, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=tempToken.nilai)
            #     return node.nodeIdentifier(tempToken)
        
    def parseTerm(self)->node.nodeEkspresi:
        # print("PARSE TERM")
        nodeKiri = self.parseFaktor()
        
        while self.tokenSkrg.tipe == Ttype.T_MULT or self.tokenSkrg.tipe == Ttype.T_DIVE:
            if(self.tokenDepan.tipe==Ttype.T_IDTF or self.tokenDepan.tipe in grammar.literalList.values()):
                operator = self.tokenSkrg
                self.maju()
                nodeKanan=self.parseFaktor()
                nodeKiri = node.nodeBiner(nodeKiri, operator, nodeKanan)
            else:
                self.parseEkspresiInvalidFlag=True
                self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=13, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenDepan.nilai)
                break
        return nodeKiri
    
    def parseEkspresi(self)->node.nodeEkspresi:
        # print("PARSE EKSPRESI")
        # if(self.tokenSkrg.tipe in grammar.literalList.values()):
            nodeKiri = self.parseTerm()
            
            while self.tokenSkrg.tipe==Ttype.T_PLUS or self.tokenSkrg.tipe==Ttype.T_MINS:
                if(self.tokenDepan.tipe==Ttype.T_IDTF or self.tokenDepan.tipe in grammar.literalList.values() or self.tokenDepan.tipe==grammar.SYMBOL_PRTS_KNAN):
                    operator = self.tokenSkrg
                    self.maju()
                    nodeKanan = self.parseTerm()
                    nodeKiri = node.nodeBiner(nodeKiri, operator, nodeKanan)
                    # print("TES1 : ",self.fullToken[self.idxIterator-1].tipe,self.fullToken[self.idxIterator].tipe,self.fullToken[self.idxIterator+1].tipe)
                else:
                    # print("operand kanan invalid")
                    self.parseEkspresiInvalidFlag=True
                    self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=13, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenDepan.nilai)
                    break
            return nodeKiri
        
    def parseParameter(self)->list[node.nodeParameter]:
        paramContainer : list[node.nodeParameter] = []
        tempNamaParam : tokenClass | None = None
        tempTipeParam : tokenClass | None = None
        tempNilaiParam : node.nodeClass | None = None
        
        state : int = 0
        errorFlag : bool = False
        while self.idxIterator<len(self.fullToken):
            tempNodeParam : node.nodeParameter = node.nodeParameter(self.tokenSkrg.baris, self.tokenSkrg.kolom)
            if(self.tokenSkrg.tipe!=Ttype.T_DLMR):
                
                if(not errorFlag):
                    #state default
                    if(state==0):
                        
                        if(self.tokenSkrg.tipe==Ttype.T_PRTS_KIRI):
                            state=1
                            self.maju()
                            
                        elif(self.tokenSkrg.tipe==Ttype.T_SYMBOL_KOMA):
                            state=12
                            self.maju()
                            
                        elif(self.tokenSkrg.tipe==Ttype.T_PRTS_KNAN):
                            state=12
                        
                        elif(self.tokenSkrg.tipe==Ttype.T_SYMBOL_TKWA):
                            state=2
                            self.maju()
                            
                        elif(self.tokenSkrg.tipe==Ttype.T_SMDG):
                            state=3
                            self.maju()
                        
                        elif(self.tokenSkrg.tipe in grammar.literalList.values()):
                            self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=11, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
                            # raise Exception("TES")
                            # print("DEBUG1")
                            errorFlag = True
                            self.maju()
                        
                        else:
                            # self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=7, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
                            # # raise Exception("TES")
                            # print("DEBUG2")
                            # errorFlag = True
                            self.maju()
                            
                    #state baca nama param
                    elif(state==1):
                        if(self.tokenSkrg.tipe in [Ttype.T_SYMBOL_TKWA, Ttype.T_SMDG, Ttype.T_SYMBOL_KOMA, Ttype.T_PRTS_KNAN]):
                            state=0
                        else:
                            if(not tempNamaParam is None):
                                self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=2, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
                                # errorFlag = True
                                # self.maju()
                            tempNamaParam=self.tokenSkrg
                            self.maju()
                        
                        # elif(self.tokenSkrg.tipe==Ttype.T_IVTF):
                        #     # print("DEBUG4")
                        #     self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=3, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
                        #     self.maju()
                        #     errorFlag = True
                            
                        # else:
                        #     tempNamaParam=self.tokenSkrg
                            # if(self.tokenSkrg.tipe!=Ttype.T_SYMBOL_TKWA):
                            #     print("DEBUG5")
                            #     self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=3, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
                        
                    #state baca tipedata
                    elif(state==2):
                        if(self.tokenSkrg.tipe in [Ttype.T_SYMBOL_TKWA, Ttype.T_SMDG, Ttype.T_SYMBOL_KOMA, Ttype.T_PRTS_KNAN]):
                            state=0
                        else:
                            if(not tempTipeParam is None):
                                self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=2, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
                            tempTipeParam = self.tokenSkrg
                            self.maju()
                        # if(self.tokenSkrg.tipe in grammar.primitiveList.values() or self.tokenSkrg.tipe==Ttype.T_IDTF):
                        #     if(not tempTipeParam is None):
                        #         self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=2, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
                        #     # else:
                        # else:
                        #     state=0
                        # self.maju()
                        # tempTipeParam = self.tokenSkrg
                    
                    #state baca value
                    elif(state==3):
                        if(self.tokenSkrg.tipe in [Ttype.T_SYMBOL_TKWA, Ttype.T_SMDG, Ttype.T_SYMBOL_KOMA, Ttype.T_PRTS_KNAN]):
                            state=0
                        else:
                            if(tempNodeParam.nilaiDefault is None):
                                tempNilaiParam=self.parseEkspresi()
                            else:
                                raise Exception("INVALID EKSPRESI")
                            if(self.tokenSkrg.tipe==Ttype.T_SYMBOL_KOMA):
                                self.maju()
                        # if(self.tokenSkrg.tipe==Ttype.T_SMDG):
                        #     self.maju()
                        # elif(self.tokenSkrg.tipe==Ttype.T_SYMBOL_KOMA):
                        #     state=0
                        # elif(self.tokenSkrg.tipe in grammar.literalList.values() or self.tokenSkrg.tipe==Ttype.T_IDTF):
                        #     if(tempNodeParam.nilaiDefault is None):
                        #         # tempNodeParam.nilaiDefault=self.parseEkspresi()
                        #         tempNilaiParam=self.parseEkspresi()
                        #         if(self.tokenSkrg.tipe!=Ttype.T_PRTS_KNAN):
                        #             self.maju() #if skrg ) then false
                        #         state=0
                        #     else:
                        #         raise Exception("ekspresi param invalid")
                            # self.maju()
                        # else:
                        #     state=0
                            
                    #state save ke node parameter
                    elif(state==12):
                        # match (tempNamaParam is None, tempTipeParam is None, tempNilaiParam is None):
                        tempNodeParam.nama = ("" if tempNamaParam is None else tempNamaParam.nilai)
                        tempNodeParam.tipedata = (Ttype.T_NULL if tempTipeParam is None else tempTipeParam.tipe)
                        tempNodeParam.nilaiDefault = tempNilaiParam
                        paramContainer.append(tempNodeParam)
                        tempNamaParam = None
                        tempTipeParam = None
                        tempNilaiParam = None
                        
                        if(self.tokenSkrg.tipe==Ttype.T_PRTS_KNAN):
                            break
                        else:
                            state=1
                    #state nentuin nilai default

                else:
                    break
        return paramContainer

    def parsePanggilFungsi(self)->node.nodePanggilFungsi:
        self.maju()
        if(self.tokenSkrg.isKeyword()):
            self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=7, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)


        return node.nodePanggilFungsi(self.tokenSkrg.baris, self.tokenSkrg.kolom, self.tokenSkrg)
        
    def parseBikinFungsi(self)->node.nodeBikinFungsi:
        self.maju(2)
        tempNode : node.nodeBikinFungsi = node.nodeBikinFungsi(self.tokenSkrg.baris, self.tokenSkrg.kolom)
        state : int = 0
        tempLastValidToken : tokenClass = tokenClass(-1,-1,Ttype.T_NULL,"NULL")
        while self.idxIterator<len(self.fullToken):
            if(self.tokenSkrg.tipe!=Ttype.T_DLMR):
                #state default nyari keyword yg dibutuhin
                if(state==0):
                    if(self.tokenSkrg.tipe==Ttype.T_NMNY):
                        state=1
                        self.maju()
                        
                    elif(self.tokenSkrg.tipe==Ttype.T_TPNY):
                        state=2
                        self.maju()
                        
                    elif(self.tokenSkrg.tipe==Ttype.T_PMNY):
                        state=3
                        self.maju()
                        
                    elif(self.tokenSkrg.tipe==Ttype.T_ISNY):
                        state=4
                        self.maju()
                        
                    elif(self.tokenSkrg.tipe==Ttype.T_DLMR): #type: ignore
                        break
                    
                    # elif(self.tokenSkrg.tipe==Ttype.T_AKHR):
                    #     tempLastValidToken = self.fullToken[self.idxIterator]
                    #     if(self.idxIterator==len(self.fullToken)-1):
                    #         break
                    #     else:
                    #         self.maju()
                    
                    elif(self.tokenSkrg.tipe==Ttype.T_BKIN):
                        tempLastValidToken = self.fullToken[self.idxIterator-1]
                        self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=9, p_baris=tempLastValidToken.baris, p_kolom=tempLastValidToken.kolom)
                        # print("TEST2",tempLastValidToken)
                        break
                    
                    elif(self.idxIterator==len(self.fullToken)-1):
                        tempLastValidToken = self.fullToken[self.idxIterator]
                        self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=9, p_baris=tempLastValidToken.baris, p_kolom=tempLastValidToken.kolom)
                        break
                    
                    else:
                        self.maju()
                #state nyari nama
                elif(state==1):
                    if(self.tokenSkrg.tipe!=Ttype.T_IDTF):
                        self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=3, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
                        # state=0
                        
                    elif(self.tokenSkrg.tipe in [Ttype.T_TPNY, Ttype.T_PMNY, Ttype.T_ISNY]):
                        # state=0
                        pass
                    else:
                        tempNode.namaFungsi = self.tokenSkrg.nilai
                        
                    state=0
                    if(self.idxIterator==len(self.fullToken)-1):
                        tempLastValidToken = self.fullToken[self.idxIterator]
                        self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=9, p_baris=tempLastValidToken.baris, p_kolom=tempLastValidToken.kolom)
                        break
                    else:
                        self.maju()
                
                #state nyari tipe
                elif(state==2):
                    if(not self.tokenSkrg.tipe in grammar.primitiveList.values() and self.tokenSkrg.tipe!=Ttype.T_VOID):
                        # print("test:",self.tokenSkrg.tipe)
                        self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=5, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
                        state=0
                        
                    elif(self.tokenSkrg.tipe in [Ttype.T_NMNY, Ttype.T_PMNY, Ttype.T_ISNY]):
                        state=0
                        
                    else:
                        tempNode.tipedataFungsi = self.tokenSkrg.nilai
                        state=0
                        
                    if(self.idxIterator==len(self.fullToken)-1):
                        tempLastValidToken = self.fullToken[self.idxIterator]
                        self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=9, p_baris=tempLastValidToken.baris, p_kolom=tempLastValidToken.kolom)
                        break
                    else:
                        self.maju()
                
                elif(state==3):
                    tempNode.parameterFungsi=self.parseParameter()
                    state=0
                    if(self.idxIterator==len(self.fullToken)-1):
                        tempLastValidToken = self.fullToken[self.idxIterator]
                        self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=9, p_baris=tempLastValidToken.baris, p_kolom=tempLastValidToken.kolom)
                        break
                    else:
                        self.maju()
                        
                #state ngebaca isi
                elif(state==4):
                    tempNode.isiFungsi = self.parseCodeContainer()
                    state=0
                    # tempLastValidToken = self.fullToken[self.idxIterator]
                    # print("TEST",tempLastValidToken)
                    # if(self.tokenSkrg in [Ttype.T_NMNY, Ttype.T_TPNY, Ttype.T_PMNY]):
                    #     state=0
                        
                    # self.maju()
                    pass
            else:
                break
        # raise Exception("TEST")
        return tempNode

    def parseBikinVariabel(self)->node.nodeBikinVariabel:
        self.maju(2)
        tempNode : node.nodeBikinVariabel = node.nodeBikinVariabel(self.tokenSkrg.baris, self.tokenSkrg.kolom)
        state : int = 0
        tempLastValidToken : tokenClass = tokenClass(-1,-1,tokenType.T_NULL,"NULL")
        errorFlag : bool = False
        while self.idxIterator<len(self.fullToken):
            if(self.tokenSkrg.tipe!=Ttype.T_DLMR):
                if(not errorFlag):
                    if(state==0):
                        if(self.tokenSkrg.tipe==Ttype.T_NMNY):
                            state=1
                            self.maju()
                            
                        elif(self.tokenSkrg.tipe==Ttype.T_TPNY):
                            state=2
                            self.maju()
                            
                        elif(self.tokenSkrg.tipe==Ttype.T_NLNY):
                            state=3
                            self.maju()
                            
                        elif(self.tokenSkrg.tipe==Ttype.T_BKIN):
                            tempLastValidToken = self.fullToken[self.idxIterator-1]
                            self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=10, p_baris=tempLastValidToken.baris, p_kolom=tempLastValidToken.kolom)
                            self.mundur()
                            break
                        else:
                            self.maju()
                            
                    elif(state==1):
                        if(self.tokenSkrg.tipe==Ttype.T_IDTF):
                            if(len(tempNode.namaVariabel)<=0):
                                tempNode.namaVariabel = self.tokenSkrg.nilai
                                # self.maju()
                            else:
                                self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=2, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
                                # self.maju()
                                errorFlag=True
                            if(self.idxIterator==len(self.fullToken)-1):
                                tempLastValidToken = self.fullToken[self.idxIterator]
                                self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=9, p_baris=tempLastValidToken.baris, p_kolom=tempLastValidToken.kolom)
                                break
                            else:
                                self.maju()
                        elif(self.tokenSkrg.tipe==Ttype.T_NMNY):
                            self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=4, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
                            if(self.idxIterator==len(self.fullToken)-1):
                                tempLastValidToken = self.fullToken[self.idxIterator]
                                self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=9, p_baris=tempLastValidToken.baris, p_kolom=tempLastValidToken.kolom)
                                break
                            else:
                                self.maju()
                            errorFlag=True
                        elif(self.tokenSkrg.tipe in [Ttype.T_TPNY, Ttype.T_TPNY]):
                            state=0
                        else:
                            tempNode.namaVariabel+= self.tokenSkrg.nilai
                            self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=3, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
                            # self.maju()
                            if(self.idxIterator==len(self.fullToken)-1):
                                tempLastValidToken = self.fullToken[self.idxIterator]
                                self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=9, p_baris=tempLastValidToken.baris, p_kolom=tempLastValidToken.kolom)
                                # self.mundur()
                                break
                            else:
                                self.maju()
                            errorFlag=True
                        # self.maju()
                
                    elif(state==2):
                        if(not self.tokenSkrg.tipe in grammar.primitiveList.values() and self.tokenSkrg.tipe!=Ttype.T_IDTF):
                            self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=3, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
                        tempNode.tipedataVariabel = self.tokenSkrg.tipe
                        if(self.idxIterator==len(self.fullToken)-1):
                            tempLastValidToken = self.fullToken[self.idxIterator]
                            self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=9, p_baris=tempLastValidToken.baris, p_kolom=tempLastValidToken.kolom)
                            break
                        else:
                            self.maju()
                        # self.maju()
                        state=0
                    
                    elif(state==3):
                        tempNode.nilaiVariabel = self.parseEkspresi()
                        self.parseEkspresiInvalidFlag=False
                        if(self.idxIterator==len(self.fullToken)-1):
                            tempLastValidToken = self.fullToken[self.idxIterator]
                            self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=9, p_baris=tempLastValidToken.baris, p_kolom=tempLastValidToken.kolom)
                            break
                        else:
                            self.maju()
                        # self.maju()
                        state=0
                else:
                    break
            else:
                if(len(tempNode.namaVariabel)<=0):
                    self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=1, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)

                # self.ASTObjek.addNode(tempNode)
                break
        return tempNode
    
    # def parsePanggilFungsi(self)->node.nodePanggilFungsi:
    #     tempNodePanggilFungsi : node.nodePanggilFungsi = node.nodePanggilFungsi(self.tokenSkrg.baris, self.tokenSkrg.kolom, self.tokenSkrg)
    #     state:int=0
        
    #     while self.idxIterator<len(self.fullToken)-1:
    #         if(state==0):
    #             if(self.tokenSkrg.tipe==Ttype.T_IDTF):
    #                 if()
    #                 tempNodePanggilFungsi.namaFungsi = self.tokenSkrg
        
    
    def parseCodeContainer(self)->list[node.nodeClass]:
        # nodeBlock : node.nodeBlock = node.nodeBlock(self.tokenSkrg.baris, self.tokenSkrg.kolom)
        kumpulanNode : list[node.nodeClass] = []
        
        while self.idxIterator<len(self.fullToken)-1:
            tempNode : node.nodeClass | None = None
            self.refresh()
            match [self.tokenSkrg.tipe, self.tokenDepan.tipe]:
                case pola.POLA_BIKIN_VARIABEL:
                    tempNode = self.parseBikinVariabel()
                    pass
                
                case pola.POLA_BIKIN_FUNGSI:
                    tempNode = self.parseBikinFungsi()
                    pass
                
                case [Ttype.T_BLKN,_]:
                    self.maju()
                    tempNodeReturn : node.nodeBalikin = node.nodeBalikin(self.tokenSkrg.baris, self.tokenSkrg.baris)
                    tempNodeReturn.returnEkspresi = self.parseEkspresi()
                    tempNode = tempNodeReturn
                #     break
                    pass
                
                case [Ttype.T_AKHR,_]:
                    break
                
                case _:
                    # print("ERR",self.tokenSkrg)
                    # self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=9, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom)
                    pass
            if(not tempNode is None):
                # nodeBlock.isiBlock.append(tempNode)
                kumpulanNode.append(tempNode)
            if(self.idxIterator<len(self.fullToken)-1):
                self.maju()
        return kumpulanNode

    def parseGlobal(self)->None:
        outerScopeFlag : bool = False
        outerScopeList : list[list[tokenClass]] = []
        outerScopeRecorder : list[tokenClass] = []
        while self.idxIterator<len(self.fullToken)-1:
            tempNode : node.nodeClass = node.nodeError(0,0)
            self.refresh()
            match [self.tokenSkrg.tipe, self.tokenDepan.tipe]:
                # case pola.POLA_BIKIN_VARIABEL:
                #     tempNode = self.parseBikinVariabel()
                #     pass
                
                case pola.POLA_BIKIN_FUNGSI:
                    if(outerScopeFlag):
                        outerScopeFlag=False
                        outerScopeList.append(outerScopeRecorder.copy())
                        outerScopeRecorder.clear()
                        
                    tempNode = self.parseBikinFungsi()
                    pass
                
                case pola.POLA_ENTRY_POINT:
                    if(self.tokenDepan.nilai==grammar.KEYWORD_ENTRY_POINT):
                        self.punyaEntryPoint=True
                        self.maju(3)
                        tempNode = node.nodeBikinFungsi(self.tokenSkrg.baris, self.tokenSkrg.kolom, self.tokenSkrg.nilai, grammar.KEYWORD_VOID)
                        tempNode.isiFungsi = self.parseCodeContainer()
                    else:
                        raise Exception("APENI WOI")
                    pass
                case _:
                    outerScopeRecorder.append(self.tokenSkrg)
                    # self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=14, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
                    
                    outerScopeFlag=True
            
            if(not isinstance(tempNode,node.nodeError)):
                self.ASTObjek.nodeRoot.nodeContainer.append(tempNode)
                
                    
            if(self.idxIterator<len(self.fullToken)-1):
                self.maju()
                if(self.idxIterator==len(self.fullToken)-1):
                    if(outerScopeFlag):
                        outerScopeFlag=False
                        outerScopeRecorder.append(self.tokenSkrg)
                        outerScopeList.append(outerScopeRecorder.copy())
                        outerScopeRecorder.clear()
                # if(self.idxIterator>15):
                #     pass
                
        
        if(len(outerScopeList)>0):
            for outerScopePiece in outerScopeList:
                if(outerScopePiece[0].baris!=outerScopePiece[-1].baris):
                    self.errorHandlerObjek.tambahinError(p_kelas=__name__,\
                        p_kodeError=14, p_baris=outerScopePiece[0].baris, p_bagian=f"mulai dari ({outerScopePiece[0].nilai}) sampe ({outerScopePiece[-1].nilai}) baris : {outerScopePiece[-1].baris} kolom : "+str(outerScopePiece[-1].kolom-(outerScopePiece[-1].getValueLength() if outerScopePiece[-1].getValueLength()>1 else 0)))
                else:
                    self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=14, p_baris=outerScopePiece[0].baris, p_bagian=f"mulai dari ({outerScopePiece[0].nilai}) sampe ({outerScopePiece[-1].nilai})")

    def proses(self, p_tokens : list[tokenClass])->None:
        self.fullToken = p_tokens
        self.parseGlobal()
        
        if(not self.punyaEntryPoint):
            self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=15)
        
