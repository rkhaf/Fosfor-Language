
from data_language.tokens import tokenClass
from data_language.tokens import tokenType
from modul_parsing.AST import ASTClass
from data_language import grammar
from pohon import node
from errorHandler import errorHandlerClass
from data_language import pola
from data_language.tokens import tokenType as Ttype
from enum import Enum
from metadata.datatypeClass import datatypesFactory
from metadata.datatypeClass import TIPEDATA_NULL
from metadata.datatypeClass import TIPEDATA_VOID
from metadata.datatypeClass import TIPEDATA_INTEGER
from typing import Any
import copy

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
        """buat majuin token sekiter p_nilai kali
        """
        self.idxIterator+=p_nilai
        self.refresh()
        pass
    
    def mundur(self, p_nilai : int = 1):
        """sama kyk maju(), tpi ini mundur
        """
        self.idxIterator-=p_nilai
        self.refresh()
        pass
    
    def refresh(self)->None:
        """buat ngesinkronin antar property token (belakang, skrg, depan) sama indeks token yg lagi dibaca
        + ada fitur proteksi out of bounds buat token depannya 
        """
        self.tokenSkrg = self.fullToken[self.idxIterator]
        self.tokenBlkng= self.fullToken[self.idxIterator-1]
        if(self.idxIterator<len(self.fullToken)-1):
            self.tokenDepan = self.fullToken[self.idxIterator+1]
        pass
    
    def parseFaktor(self)->node.nodeEkspresi | node.nodeInvalidEkspresi | None:
        """fungsi ini buat ngeparse bentuk ekspresi terkecil kyk literal/identifier, jg buat nangkep ekspresi dlm kurung & manfaatin fungsi rekursif
        """
        if(self.tokenSkrg.tipe==Ttype.T_LITERAL_FLOAT or self.tokenSkrg.tipe==Ttype.T_LITERAL_INT):
            if(not self.parseEkspresiInvalidFlag):
                tempToken = self.tokenSkrg
                if(self.tokenDepan.tipe in grammar.operatorList.values() or self.tokenDepan.tipe in grammar.perbandinganList.values() or self.tokenDepan.tipe in [Ttype.T_PRTS_KIRI, Ttype.T_PRTS_KNAN, Ttype.T_SYMBOL_KOMA]):
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
                # print("parseFaktor, numerik",datatypesFactory.konversi(tempToken.tipe))
                temp = node.nodeNomor(tempToken, datatypesFactory.konversi(tempToken.tipe))
                return temp
            else:
                return node.nodeInvalidEkspresi(self.tokenSkrg, datatypesFactory.konversi(self.tokenSkrg.tipe))
                # return node.nodeInvalidEkspresi(self.tokenSkrg)
        
        elif(self.tokenSkrg.tipe==Ttype.T_LITERAL_STR):
            if(not self.parseEkspresiInvalidFlag):
                tempToken = self.tokenSkrg
                if(self.tokenDepan.tipe in grammar.operatorList.values() or self.tokenDepan.tipe in grammar.perbandinganList.values() or self.tokenDepan.tipe in grammar.literalList.keys() or self.tokenDepan.tipe in [Ttype.T_PRTS_KIRI, Ttype.T_PRTS_KNAN, Ttype.T_SYMBOL_KOMA]):
                    self.maju()
                return node.nodeString(tempToken, datatypesFactory.konversi(tempToken.tipe))
                # return node.nodeString(tempToken)
            else:
                return node.nodeInvalidEkspresi(self.tokenSkrg, datatypesFactory.konversi(self.tokenSkrg.tipe))
                # return node.nodeInvalidEkspresi(self.tokenSkrg)
        
        elif(self.tokenSkrg.tipe==Ttype.T_LITERAL_BOOL):
            if(not self.parseEkspresiInvalidFlag):
                tempToken = self.tokenSkrg
                if(self.tokenDepan.tipe in grammar.operatorList.values() or self.tokenDepan.tipe in grammar.perbandinganList.values() or self.tokenDepan.tipe in grammar.literalList.keys() or self.tokenDepan.tipe in [Ttype.T_PRTS_KIRI, Ttype.T_PRTS_KNAN, Ttype.T_SYMBOL_KOMA]):
                    self.maju()
                return node.nodeBoolean(tempToken, datatypesFactory.konversi(tempToken.tipe))
                # return node.nodeBoolean(tempToken)
            else:
                return node.nodeInvalidEkspresi(self.tokenSkrg, datatypesFactory.konversi(self.tokenSkrg.tipe))
                # return node.nodeInvalidEkspresi(self.tokenSkrg)

        elif(self.tokenSkrg.tipe==Ttype.T_IDTF):
            if(not self.parseEkspresiInvalidFlag):
                tempToken = self.tokenSkrg
                if(self.tokenDepan.tipe in grammar.operatorList.values() or self.tokenDepan.tipe in grammar.perbandinganList.values() or self.tokenDepan.tipe in [Ttype.T_PRTS_KIRI, Ttype.T_PRTS_KNAN, Ttype.T_SYMBOL_KOMA]):
                    self.maju()
                # print("parseFaktor, identifier",datatypesFactory.konversi(tempToken.tipe))
                return node.nodeIdentifier(tempToken)
                # return node.nodeIdentifier(tempToken)
            else:
                return node.nodeInvalidEkspresi(self.tokenSkrg, datatypesFactory.konversi(self.tokenSkrg.tipe))
                # return node.nodeInvalidEkspresi(self.tokenSkrg)
        else:
            tempToken = self.fullToken[self.idxIterator-1]
            if(self.tokenSkrg.tipe==Ttype.T_PRTS_KIRI):
                self.maju()
                nodee = self.parseEkspresi()
                if(self.tokenSkrg.tipe==Ttype.T_PRTS_KNAN): #type: ignore
                    # if(self.tokenDepan.tipe in grammar.operatorList.values() or self.tokenDepan.tipe in grammar.literalList.keys() or self.tokenDepan.tipe in [Ttype.T_PRTS_KIRI, Ttype.T_PRTS_KNAN]):
                    if(self.tokenDepan.tipe in grammar.operatorList.values() or self.tokenDepan.tipe in grammar.literalList.keys()):
                        self.maju()
                    return nodee
                elif(self.tokenSkrg.tipe==Ttype.T_SYMBOL_KOMA): #type: ignore
                    if(self.tokenDepan.tipe in grammar.operatorList.values() or self.tokenDepan.tipe in grammar.literalList.keys() or self.tokenDepan.tipe in [Ttype.T_PRTS_KIRI, Ttype.T_PRTS_KNAN]):
                        self.maju()
                    return nodee
                else:
                    if(self.parseEkspresiInvalidFlag):
                        return node.nodeInvalidEkspresi(self.tokenSkrg, datatypesFactory.konversi(self.tokenSkrg.tipe))
                        # return node.nodeInvalidEkspresi(self.tokenSkrg)
                    
                    else:
                        if(not self.parseEkspresiInvalidFlag):
                            self.parseEkspresiInvalidFlag=True
                            self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=13, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenDepan.nilai)
                            raise Exception("STOPPER1")
                        else:
                            raise Exception("INVALID")
            elif(self.tokenSkrg.tipe==Ttype.T_PRTS_KNAN):
                return None
                # return node.nodeEkspresi(self.tokenSkrg.baris,self.tokenSkrg.kolom,TIPEDATA_NULL)
                # return node.nodeEkspresi(self.tokenSkrg.baris,self.tokenSkrg.kolom,Ttype.T_NULL)
            else:
                return node.nodeIdentifier(self.tokenSkrg)
                # return node.nodeIdentifier(self.tokenSkrg)
            
    def parseTerm(self)->node.nodeEkspresi | None:
        """fungsi ini buat ngeparse bentuk ekspresi dgn prioritas tinggi (kali, bagi)
        dgn cara ngoper token ke fungsi parseFaktor() & juga nangkap operasi kali bagi
        """
        nodeKiri = self.parseFaktor()
        
        while self.tokenSkrg.tipe == Ttype.T_MULT or self.tokenSkrg.tipe == Ttype.T_DIVE:
            if(self.tokenDepan.tipe==Ttype.T_IDTF or self.tokenDepan.tipe in grammar.literalList.values() or self.tokenDepan.tipe in [Ttype.T_PRTS_KIRI, Ttype.T_PRTS_KNAN]):
                operator = self.tokenSkrg
                self.maju()
                nodeKanan=self.parseFaktor()
                if((not nodeKanan is None) and (not nodeKiri is None)):
                    nodeKiri = node.nodeBiner(nodeKiri, operator, nodeKanan)
            else:
                self.parseEkspresiInvalidFlag=True
                self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=13, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenDepan.nilai)
                break
        if(not nodeKiri is None):
            return nodeKiri
        else:return None
        
    def parseAditif(self)->node.nodeEkspresi | None:
        nodeKiri = self.parseTerm()
        
        while self.tokenSkrg.tipe==Ttype.T_PLUS or self.tokenSkrg.tipe==Ttype.T_MINS:
            if(self.tokenDepan.tipe==Ttype.T_IDTF or self.tokenDepan.tipe in grammar.literalList.values() or self.tokenDepan.tipe in [Ttype.T_PRTS_KIRI, Ttype.T_PRTS_KNAN]):
                operator = self.tokenSkrg
                self.maju()
                nodeKanan = self.parseTerm()
                if((not nodeKanan is None) and (not nodeKiri is None)):
                    nodeKiri = node.nodeBiner(nodeKiri, operator, nodeKanan)
            else:
                self.parseEkspresiInvalidFlag=True
                self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=13, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenDepan.nilai)
                break
        if(not nodeKiri is None):
            return nodeKiri
        else:
            return None
    
    def parsePerbandingan(self)-> node.nodeEkspresi | None:
        nodeKiri = self.parseAditif()
        
        while self.tokenSkrg.tipe in [Ttype.T_CMPR_KCIL, Ttype.T_CMPR_GSMA, Ttype.T_CMPR_BSAR, Ttype.T_CMPR_SAMA, Ttype.T_CMPR_SBSR, Ttype.T_CMPR_SKCL]:
            if(self.tokenDepan.tipe==Ttype.T_IDTF or self.tokenDepan.tipe in grammar.literalList.values() or self.tokenDepan.tipe in [Ttype.T_PRTS_KIRI, Ttype.T_PRTS_KNAN]):
                operator = self.tokenSkrg
                self.maju()
                nodeKanan = self.parseAditif()
                if((not nodeKanan is None) and (not nodeKiri is None)):
                    nodeKiri = node.nodeBanding(nodeKiri, operator, nodeKanan)
            else:
                self.parseEkspresiInvalidFlag=True
                self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=13, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenDepan.nilai)
                break
        if(not nodeKiri is None):
            return nodeKiri
        else:
            return None
    
    def parseEkspresi(self)->node.nodeEkspresi | None:
        """fungsi ini buat ngeparse bentuk ekspresi apapun,
        klo semisal ekspresi perhitungan nnti bakal ngeprosesing dgn cara manggil ke fungsi parseTerm()
        tpi klo ekspresi assignment & invoke beda lgi treatmentnya, cek ajalh fungsinya kocak
        """
        match [self.tokenSkrg.tipe, self.tokenDepan.tipe]:
            case [Ttype.T_IDTF, Ttype.T_PRTS_KIRI]:
                return self.parsePanggilFungsi()
            
            case _:
                return self.parsePerbandingan()

        
    def parseParameter(self)->list[node.nodeParameter]:
        """fungsi ini cmn ditujuin buat parameter bikin fungsi utk bagian pembacaan parameter
        """
        paramContainer : list[node.nodeParameter] = []
        tempNamaParam : tokenClass | None = None
        tempTipeParam : tokenClass | None = None
        tempNilaiParam : node.nodeClass | None = None
        
        state : int = 0
        errorFlag : bool = False
        while self.idxIterator<len(self.fullToken):
            tempNodeParam : node.nodeParameter = node.nodeParameter(self.tokenSkrg.baris, self.tokenSkrg.kolom)
            # tempNodeParam : node.nodeParameter = node.nodeParameter(self.tokenSkrg.baris, self.tokenSkrg.kolom)
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
                            errorFlag = True
                            self.maju()
                        
                        else:
                            self.maju()
                            
                    #state baca nama param
                    elif(state==1):
                        if(self.tokenSkrg.tipe in [Ttype.T_SYMBOL_TKWA, Ttype.T_SMDG, Ttype.T_SYMBOL_KOMA, Ttype.T_PRTS_KNAN]):
                            state=0
                        else:
                            if(not tempNamaParam is None):
                                self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=2, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
                            tempNamaParam=self.tokenSkrg
                            self.maju()
                            
                    #state baca tipedata
                    elif(state==2):
                        if(self.tokenSkrg.tipe in [Ttype.T_SYMBOL_TKWA, Ttype.T_SMDG, Ttype.T_SYMBOL_KOMA, Ttype.T_PRTS_KNAN]):
                            state=0
                        else:
                            if(not tempTipeParam is None):
                                self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=2, p_baris=self.tokenSkrg.baris, p_kolom=self.tokenSkrg.kolom, p_bagian=self.tokenSkrg.nilai)
                            tempTipeParam = self.tokenSkrg
                            self.maju()
                            
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
                                state=0
                                # self.maju()
                                
                    #state save ke node parameter
                    elif(state==12):
                        tempNodeParam.nama = ("" if tempNamaParam is None else tempNamaParam.nilai)
                        tempNodeParam.tipedata = (TIPEDATA_NULL if tempTipeParam is None else datatypesFactory.konversi(tempTipeParam.tipe))
                        # tempNodeParam.tipedata = (Ttype.T_NULL if tempTipeParam is None else tempTipeParam.tipe)
                        tempNodeParam.nilaiDefault = tempNilaiParam
                        # tempNodeParam : node.nodeParameter = node.nodeParameter(self.tokenSkrg.baris, self.tokenSkrg.kolom)
                        paramContainer.append(tempNodeParam)
                        tempNamaParam = None
                        tempTipeParam = None
                        tempNilaiParam = None
                        
                        if(self.tokenSkrg.tipe==Ttype.T_PRTS_KNAN):
                            break
                        else:
                            state=1
                else:
                    break
        return paramContainer

    # def parseKalauBranch(self)->node

    def parsePanggilFungsi(self)->node.nodePanggilFungsi:
        """fungsi ini ditujuin utk ngehandle kalo ada pemanggilan fungsi, sambil ngecall fungsi parseEkspresi jg utk ngehandle isinya
        """
        tempNodePanggilFungsi : node.nodePanggilFungsi = node.nodePanggilFungsi(self.tokenSkrg.baris, self.tokenSkrg.kolom, self.tokenSkrg)
        state : int = 0
        
        while self.idxIterator<len(self.fullToken):
            if(self.tokenSkrg.tipe!=Ttype.T_DLMR):
                
                #state default
                if(state==0):
                    if(self.tokenSkrg.isIdentifier()):
                        state=1
                        
                    elif(self.tokenSkrg.tipe==Ttype.T_PRTS_KIRI):
                        state=2
                    
                    elif(self.tokenSkrg.tipe==Ttype.T_PRTS_KNAN):
                        if(self.tokenDepan.tipe!=Ttype.T_PRTS_KNAN):
                            self.maju()
                        # self.maju()
                        break
                    
                    elif(self.tokenSkrg.tipe==Ttype.T_SYMBOL_KOMA):
                        state=2
                        self.maju()
                    
                    else:
                        state=1
                        self.errorHandlerObjek.tambahinError(__name__, 3, self.tokenSkrg.baris, self.tokenSkrg.kolom, self.tokenSkrg.nilai)
                        # print(self.tokenSkrg.nilai)
                        # raise Exception("stopper")
                    
                #ngepick identifier
                elif(state==1):
                    if(self.tokenSkrg.tipe==tokenType.T_IDTF):
                        tempNodePanggilFungsi.namaFungsi = self.tokenSkrg
                    self.maju()
                    state=0
                    
                elif(state==2):
                    temp : node.nodeEkspresi | None = self.parseEkspresi()
                    if(not temp is None):
                        tempNodePanggilFungsi.parameterInput.append(temp)

                    state=0
                    pass
                    
            else:break
        return tempNodePanggilFungsi
    
    def parseBikinFungsi(self)->node.nodeBikinFungsi:
        """fungsi ini buat ngehandle sintaks bikin fungsi, returnnya objek node bikin fungsi dgn data isian dri token yg udh dibaca
        """
        self.maju(2)
        tempNode : node.nodeBikinFungsi = node.nodeBikinFungsi(self.tokenSkrg.baris, self.tokenSkrg.kolom,"", TIPEDATA_VOID)
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
                        # self.maju()
                        break

                    elif(self.tokenSkrg.tipe==Ttype.T_BKIN):
                        tempLastValidToken = self.fullToken[self.idxIterator-1]
                        self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=9, p_baris=tempLastValidToken.baris, p_kolom=tempLastValidToken.kolom)
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
                        tempNode.tipedataFungsi = datatypesFactory.konversi(self.tokenSkrg.tipe)
                        # tempNode.tipedataFungsi = self.tokenSkrg.nilai
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
                    pass
            else:
                break
        return tempNode

    def parseBikinVariabel(self)->node.nodeBikinVariabel:
        """fungsi ini buat ngehandle sintaks bikin variabel, returnnya objek node bikin variabel dgn data isian dri token yg udh dibaca
        """
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
                        tempNode.tipedataVariabel = datatypesFactory.konversi(self.tokenSkrg.tipe)
                        # tempNode.tipedataVariabel = self.tokenSkrg.tipe
                        if(self.idxIterator==len(self.fullToken)-1):
                            tempLastValidToken = self.fullToken[self.idxIterator]
                            self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=9, p_baris=tempLastValidToken.baris, p_kolom=tempLastValidToken.kolom)
                            break
                        else:
                            self.maju()
                        # self.maju()
                        state=0
                    
                    elif(state==3):
                        temp : node.nodeEkspresi | None = self.parseEkspresi()
                        if(not temp is None):
                            tempNode.nilaiVariabel = temp
                            
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
                break
        return tempNode
    
    def parsePerulanganSelama(self)->node.nodePerulanganSelama:
        self.maju(2)
        state : int = 0
        
        tempNode : node.nodePerulanganSelama = node.nodePerulanganSelama(self.tokenSkrg.baris, self.tokenSkrg.kolom)
        
        # kondisiLoop : node.nodeEkspresi
        
        while self.idxIterator<len(self.fullToken)-1:
            if(state==0):
                
                if(self.tokenBlkng.tipe==Ttype.T_SLMA):
                    if(self.tokenSkrg.tipe==Ttype.T_PRTS_KIRI):
                        state=1
                    else:
                        self.errorHandlerObjek.tambahinError(__name__, 16, self.tokenSkrg.baris, self.tokenSkrg.kolom, self.tokenSkrg.nilai)
                        self.maju()
                
                elif(self.tokenSkrg.tipe==Ttype.T_ISNY):
                    state=2
                
                elif(self.tokenSkrg.tipe==Ttype.T_AKHR):
                    state=3
                
                else:
                    self.maju()
            
            elif(state==1):
                getter : node.nodeEkspresi | None = self.parseEkspresi()
                if(not getter is None):
                    # kondisiLoop = getter
                    tempNode.kondisi = getter
                    
                self.maju()
                state = 0
            
            elif(state==2):
                # isiLoop = self.parseCodeContainer()
                self.maju()
                tempNode.isiLoop = self.parseCodeContainer()
                state = 0
                pass
                
            elif(state==3):
                self.maju()
                break
            
            # print(self.tokenSkrg)
        return tempNode

    def parseIdentifier(self)->node.nodePenugasan:
        parentIdentifier : node.nodeIdentifier = node.nodeIdentifier(self.tokenSkrg)

        tempPenugasan : node.nodePenugasan = node.nodePenugasan(self.tokenSkrg.baris, self.tokenSkrg.kolom)
        tempPenugasan.referensi = parentIdentifier
        tempPenugasan.ekspresi = node.nodeEkspresi(-1, -1, TIPEDATA_NULL)
        
        test : node.nodeAksesProperti | node.nodeIdentifier = parentIdentifier
        
        while(self.tokenDepan.tipe in [Ttype.T_SYMBOL_TTIK]):
            self.maju(2)
            tempNodeAkses = node.nodeAksesProperti(self.tokenSkrg.baris, self.tokenSkrg.kolom, TIPEDATA_NULL)
            tempNodeAkses.properti = node.nodeIdentifier(self.tokenSkrg)
            tempNodeAkses.objek = test
            test = tempNodeAkses
            
        self.maju()
        if(self.tokenSkrg.tipe==Ttype.T_SMDG):
            self.maju(1)
            tempPenugasan.referensi = test
            getter : node.nodeEkspresi | None = self.parseEkspresi()
            if(not getter is None):
                tempPenugasan.ekspresi = getter
        elif(self.tokenSkrg.tipe in [Ttype.T_ICRT, Ttype.T_DCRT]):
            if(self.tokenSkrg.tipe==Ttype.T_ICRT):
                tempPenugasan.ekspresi = node.nodeBiner(parentIdentifier, tokenClass(self.tokenSkrg.baris, self.tokenSkrg.kolom, Ttype.T_PLUS, "+"), node.nodeNomor(tokenClass(self.tokenSkrg.baris, self.tokenSkrg.kolom, Ttype.T_LITERAL_INT, "1"), TIPEDATA_INTEGER))
            
        self.maju(1)
        return tempPenugasan
    
    def parseUnary(self)->node.nodeBiner:
        identifier : tokenClass = tokenClass(-1, -1, Ttype.T_EROR, "-1")
        tokenOperator : tokenClass = tokenClass(-1, -1, Ttype.T_EROR, "-1")
        
        tokenBwtLiteral : tokenClass = tokenClass(-1, -1, Ttype.T_EROR, "-1")
        nodeLiteral : node.nodeNomor = node.nodeNomor(tokenClass(-1, -1, Ttype.T_EROR, "-1"), TIPEDATA_INTEGER)
        nodeIdentifier : node.nodeIdentifier = node.nodeIdentifier(tokenClass(-1, -1, Ttype.T_EROR, "-1"))
        
        state = 0
        invalidFlag : bool = False
        delimiterError : bool = False
        while self.idxIterator<len(self.fullToken)-1:
            
            if(state==0):
                
                if(self.tokenSkrg.tipe in [Ttype.T_IDTF, Ttype.T_IVTF]):state=1
                elif(self.tokenSkrg.tipe==Ttype.T_ICRT):state=2
                elif(self.tokenSkrg.tipe==Ttype.T_DCRT):state=3
                elif(self.tokenSkrg.tipe==Ttype.T_DLMR):
                    # self.maju()
                    break
                elif(self.tokenSkrg.tipe in grammar.keywordList.values()):
                    invalidFlag = True
                    delimiterError = True
                    self.errorHandlerObjek.tambahinError(__name__, 19, self.tokenSkrg.baris, self.tokenSkrg.kolom, f"{self.tokenSkrg.nilai}{self.tokenDepan.nilai}")
                    break
                
                else:
                    invalidFlag = True
                    self.errorHandlerObjek.tambahinError(__name__, 18, self.tokenSkrg.baris, self.tokenSkrg.kolom, f"{self.tokenSkrg.nilai}{self.tokenDepan.nilai}")
                    self.maju()
                    # print("invalid")
                    # break
                    
            elif(state==1):
                if(self.tokenSkrg.tipe in [Ttype.T_IDTF, Ttype.T_IVTF]):
                    identifier = self.tokenSkrg
                    self.maju()
                else:
                    state=0
            
            elif(state==2):
                if(self.tokenSkrg.tipe==Ttype.T_ICRT):
                    tokenOperator = tokenClass(self.tokenSkrg.baris, self.tokenSkrg.kolom, Ttype.T_PLUS, "+")
                    self.maju()
                else:
                    state=0
            
            elif(state==3):
                if(self.tokenSkrg.tipe==Ttype.T_DCRT):
                    tokenOperator = tokenClass(self.tokenSkrg.baris, self.tokenSkrg.kolom, Ttype.T_MINS, "-")
                    self.maju()
                else:
                    state=0
        
        # if(not tokenOperator is None and not identifier is None):
        if(not invalidFlag):
            tokenBwtLiteral = tokenClass(tokenOperator.baris, tokenOperator.kolom, Ttype.T_LITERAL_INT, "1")
            nodeLiteral = node.nodeNomor(tokenBwtLiteral, TIPEDATA_INTEGER)
            nodeIdentifier = node.nodeIdentifier(identifier)
            
            tempNodeBiner : node.nodeBiner = node.nodeBiner(nodeIdentifier, tokenOperator, nodeLiteral)
            return tempNodeBiner
        else:
            if(delimiterError):
                self.mundur()
            return node.nodeBiner(node.nodeEkspresi(-1, -1, TIPEDATA_NULL), tokenClass(-1, -1, Ttype.T_EROR, "-1"), node.nodeEkspresi(-1, -1, TIPEDATA_NULL))
        # else:raise Exception("UNEXPECTED ERROR")
    
    def parseKalauMisal(self)->node.nodeKalau:
        pass
    
    def parseKalau(self)->node.nodeKalau:
        print("kalau dibaris",self.tokenSkrg.baris)
        tempNodeKalau : node.nodeKalau = node.nodeKalau(self.tokenSkrg.baris, self.tokenSkrg.kolom)
        state:int=0
        
        while self.idxIterator<len(self.fullToken)-1:
            if(state==0):
                if(self.tokenSkrg.tipe==Ttype.T_KLAU):
                    if(self.tokenDepan.tipe==Ttype.T_PRTS_KIRI):
                        state=1
                    elif(self.tokenDepan.tipe==Ttype.T_MSAL):
                        self.maju()
                        state=1
                    else:
                        self.errorHandlerObjek.tambahinError(__name__, 16, self.tokenSkrg.baris, self.tokenSkrg.kolom, self.tokenSkrg.nilai)
                        break
                    
                elif(self.tokenSkrg.tipe==Ttype.T_ISNY):
                    state=2
                
                elif (self.tokenSkrg.tipe==Ttype.T_AKHR):
                    if(self.tokenDepan.tipe==Ttype.T_KLAU):
                        self.maju()
                        if(self.tokenDepan.tipe==Ttype.T_MSAL):
                            # print("ketemu elif")
                            reader : node.nodeKalau | None = self.parseKalau()
                            if(not reader is None):
                                tempNodeKalau.listElif.append(reader)
                            pass
                        elif(self.tokenDepan.tipe==Ttype.T_NGGK):
                            self.maju(3)
                            test = self.parseCodeContainer()
                            tempNodeKalau.isiElse = test
                            # state=0
                            # self.maju()
                            # self.mundur()
                            pass
                            break
                            # reader : node.nodeKalau | None = self.parseKalau()
                            # if(not reader is None):
                            #     tempNodeKalau.el
                        else:
                            self.mundur()
                            self.maju()
                            break
                    else:
                        self.maju()
                        break
                elif(self.tokenSkrg.tipe==Ttype.T_MSAL):
                    self.maju()
            
            elif(state==1):
                self.maju()
                getter : node.nodeEkspresi | None = self.parseEkspresi()
                if(not getter is None):
                    tempNodeKalau.kondisi = getter
                self.maju()
                state=0
                pass
            elif(state==2):
                self.maju()
                getList = self.parseCodeContainer()
                if(len(getList)>0):
                    tempNodeKalau.isiKalau = getList
                state=0
        print("return kalaunya baris",tempNodeKalau.baris)
        return tempNodeKalau
    
    def parseCodeContainer(self)->list[node.nodeClass]:
        """fungsi ini buat ngeparse barisan kode didalem scope (kyk isinya if, perulangan, fungsi, dll),
        returnnya sekumpulan node dari sekumpulan token yg udh dibaca
        """
        kumpulanNode : list[node.nodeClass] = []
        tokensGkDikenal : list[list[tokenClass]] = []
        tempTokensGkDikenal : list[tokenClass] = []
        print("parsing container",self.tokenSkrg.baris, self.tokenSkrg.nilai)
        
        while self.idxIterator<len(self.fullToken)-1:
            tempNode : node.nodeClass | None = None
            self.refresh()
            match [self.tokenSkrg.tipe, self.tokenDepan.tipe]:
                
                case pola.POLA_BIKIN_VARIABEL:
                    if(len(tempTokensGkDikenal)>0):
                        tokensGkDikenal.append(copy.copy(tempTokensGkDikenal))
                        tempTokensGkDikenal.clear()
                    tempNode = self.parseBikinVariabel()
                    pass
                
                case [Ttype.T_BLKN,_]:
                    if(len(tempTokensGkDikenal)>0):
                        tokensGkDikenal.append(copy.copy(tempTokensGkDikenal))
                        tempTokensGkDikenal.clear()
                    self.maju()
                    tempNodeReturn : node.nodeBalikin = node.nodeBalikin(self.tokenSkrg.baris, self.tokenSkrg.baris)
                    tempEkspresi : node.nodeEkspresi | None = self.parseEkspresi()
                    if(not tempEkspresi is None):
                        tempNodeReturn.returnEkspresi = tempEkspresi
                        
                    tempNode = tempNodeReturn
                    pass
                
                case pola.POLA_PANGGIL_FUNGSI:
                    if(len(tempTokensGkDikenal)>0):
                        tokensGkDikenal.append(copy.copy(tempTokensGkDikenal))
                        tempTokensGkDikenal.clear()
                    temp : node.nodePanggilFungsi  = self.parsePanggilFungsi()
                    kumpulanNode.append(copy.deepcopy(temp))
                    pass

                case pola.POLA_PERULANGAN_SELAMA:
                    if(len(tempTokensGkDikenal)>0):
                        tokensGkDikenal.append(copy.copy(tempTokensGkDikenal))
                        tempTokensGkDikenal.clear()
                    temp : node.nodePerulanganSelama = self.parsePerulanganSelama()
                    kumpulanNode.append(temp)
                
                case [Ttype.T_AKHR,_]:
                    if(len(tempTokensGkDikenal)>0):
                        tokensGkDikenal.append(copy.copy(tempTokensGkDikenal))
                        tempTokensGkDikenal.clear()
                    break
                
                case [Ttype.T_IDTF, _]:
                    if(len(tempTokensGkDikenal)>0):
                        tokensGkDikenal.append(copy.copy(tempTokensGkDikenal))
                        tempTokensGkDikenal.clear()
                    temp : node.nodePenugasan = self.parseIdentifier()
                    kumpulanNode.append(temp)
                
                case [Ttype.T_KLAU, _]:
                    if(len(tempTokensGkDikenal)>0):
                        tokensGkDikenal.append(copy.copy(tempTokensGkDikenal))
                        tempTokensGkDikenal.clear()
                    temp : node.nodeKalau = self.parseKalau()
                    kumpulanNode.append(temp)
                case _:
                    tempTokensGkDikenal.append(self.tokenSkrg)
                    # tokensGkDikenal.append(self.tokenSkrg)
                    pass
                
            if(not tempNode is None):
                kumpulanNode.append(tempNode)
            if(self.idxIterator<len(self.fullToken)-1):
                self.maju()
        if(len(tokensGkDikenal)>0):
            for listToken in tokensGkDikenal:
                    if(listToken[0].baris!=listToken[-1].baris):
                        self.errorHandlerObjek.tambahinError(p_kelas=__name__,\
                            p_kodeError=17, p_baris=listToken[0].baris, p_bagian=f"mulai dari ({listToken[0].nilai}) sampe ({listToken[-1].nilai}) baris : {listToken[-1].baris} kolom : "+str(listToken[-1].kolom-(listToken[-1].getValueLength() if listToken[-1].getValueLength()>1 else 0)))
                    else:
                        self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=17, p_baris=listToken[0].baris, p_bagian=f"mulai dari ({listToken[0].nilai}) sampe ({listToken[-1].nilai})")
        print("exiting contread")
        return kumpulanNode

    def parseGlobal(self)->None:
        """fungsi ini buat ngeparse scope global (utk saat ini cmn fungsi) & mastiin klo fungsi main udh dibentuk
        """
        outerScopeFlag : bool = False
        outerScopeList : list[list[tokenClass]] = []
        outerScopeRecorder : list[tokenClass] = []
        while self.idxIterator<len(self.fullToken)-1:
            tempNode : node.nodeClass = node.nodeError(0,0)
            self.refresh()
            match [self.tokenSkrg.tipe, self.tokenDepan.tipe]:
                
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
                        tempNode = node.nodeBikinFungsi(self.tokenDepan.baris, self.tokenDepan.kolom, self.tokenDepan.nilai, TIPEDATA_VOID)
                        self.maju(3)
                        pass
                        tempNode.isiFungsi = self.parseCodeContainer()
                        # self.maju()
                    else:
                        raise Exception("APENI WOI")
                    pass
                
                case _:
                    outerScopeRecorder.append(self.tokenSkrg)
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
        
        if(len(outerScopeList)>0):
            for outerScopePiece in outerScopeList:
                if(outerScopePiece[0].baris!=outerScopePiece[-1].baris):
                    self.errorHandlerObjek.tambahinError(p_kelas=__name__,\
                        p_kodeError=14, p_baris=outerScopePiece[0].baris, p_bagian=f"mulai dari ({outerScopePiece[0].nilai}) sampe ({outerScopePiece[-1].nilai}) baris : {outerScopePiece[-1].baris} kolom : "+str(outerScopePiece[-1].kolom-(outerScopePiece[-1].getValueLength() if outerScopePiece[-1].getValueLength()>1 else 0)))
                else:
                    self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=14, p_baris=outerScopePiece[0].baris, p_bagian=f"mulai dari ({outerScopePiece[0].nilai}) sampe ({outerScopePiece[-1].nilai})")
        pass
    def proses(self, p_tokens : list[tokenClass])->None:
        """klo fungsi ini fungsinya sbg gerbang masuk sma pengecekan entry point
        """
        self.fullToken = p_tokens
        self.parseGlobal()
        
        if(not self.punyaEntryPoint):
            self.errorHandlerObjek.tambahinError(p_kelas=__name__, p_kodeError=15)
        
        pass
    def getTree(self)->ASTClass:
        return self.ASTObjek