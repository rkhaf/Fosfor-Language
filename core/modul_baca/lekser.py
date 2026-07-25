# import tataBahasa

from enum import Enum
from errorHandler import errorHandlerClass
from modul_baca.tokenizer import tokenizerClass
from data_language.dataFormat import Token
from data_language.keywords import simbolList
from data_language.keywords import kurungList
from data_language.keywords import punctuationList
from data_language.keywords import operatorList
from data_language.keywords import perbandinganList

import data_language.tataBahasa as tataBahasa

class states(Enum):
    default = 1,
    numerik = 2,
    string = 3,
    simbol = 4,
    identifier = 5,
    singleLineComment = 6,
    multiLineComment = 7,
    punctuatorBracket = 8
            
class lekserClass:
    def __init__(self, p_errorHandlerReference : errorHandlerClass):
        self.errorhandlerObjek : errorHandlerClass = p_errorHandlerReference
        self.tokenizerObjek = tokenizerClass()
        self.state : states = states.default
        self.pointerIterator : int = 0
        self.barisIterator : int = 1
        self.kolomIterator : int = 1
        self.temp : str = ""
        self.currentChar : str = ""
        self.forwardChar : str = ""
        # dotCount : int = 0
        self.fileOriginal : str = ""
        self.tokens : list[Token] = []
        # invalidFlag : bool = False
        # self.commentFlag : bool = False
    
    def maju(self) -> None:
        self.pointerIterator+=1
        self.kolomIterator+=1
        if(self.pointerIterator>=20):
            pass
    
    def simpenCharKeTemp(self)->None:
        self.temp+=self.currentChar
        
    def simpenKeTemp(self, p_val : str)->None:
        self.temp+=p_val
    
    def gantiState(self, p_state : states)->None:
        self.state = p_state

    def konversiDanPushKeToken(self, p_tipedata : str = "")->None:
        if(len(p_tipedata)!=0):
            self.tokens.append(self.tokenizerObjek.getToken(self.barisIterator, self.kolomIterator, self.temp,p_tipedata))
            
        else:
            self.tokens.append(self.tokenizerObjek.getToken(self.barisIterator, self.kolomIterator, self.temp))
        self.temp=""
    
    def pushTempKeToken(self, p_tipeToken : str)->None:
        self.tokens.append(Token(self.barisIterator, self.kolomIterator, p_tipeToken, self.temp))
        self.temp=""
    
    def clearTemp(self)->None:
        self.temp=""
    
    def gantiBaris(self)->None:
        self.barisIterator+=1
        self.kolomIterator=0
        self.commentFlag=False
    
    def konversiTempJikaBerisi(self)->None:
        if(len(self.temp)>0):
            self.konversiDanPushKeToken()
    
    def ambilTokens(self)->list[Token]:
        return self.tokens
    
    def proses(self, p_fileMentahan : str) -> str | None:
        kedalamanMultiComment : int = 0
        invalidFlag : bool = False
        dotCount : int = 0
        
        while self.pointerIterator < len(p_fileMentahan):
            self.fileOriginal = p_fileMentahan
            self.currentChar = self.fileOriginal[self.pointerIterator]
            if(self.pointerIterator<len(self.fileOriginal)-1):
                self.forwardChar = self.fileOriginal[self.pointerIterator+1]
            
            if(self.state==states.default):
                dotCount=0
                invalidFlag=False
                
                if(self.currentChar+self.forwardChar==tataBahasa.CMNT_SNGL):
                    self.gantiState(states.singleLineComment)
                    
                elif(self.currentChar+self.forwardChar==tataBahasa.CMNT_MLTI_OPEN):
                    self.gantiState(states.multiLineComment)
                    
                elif(self.currentChar.isdigit()):
                    self.konversiTempJikaBerisi()
                    self.gantiState(states.numerik)
                    
                elif(self.currentChar=='"'):
                    self.gantiState(states.string)
                    self.maju()
                    
                elif(self.currentChar in simbolList.keys() or self.currentChar in perbandinganList.keys() or self.currentChar in operatorList.keys()):
                    self.gantiState(states.simbol)
                
                # elif(self.currentChar in perbandinganList.keys()):
                #     self.gantiState(states.simbol)
                
                elif(self.currentChar==tataBahasa.KEYWORD_DLMR):
                    # self.simpenCharKeTemp()
                    self.konversiTempJikaBerisi()
                    # self.clearTemp()
                    self.simpenCharKeTemp()
                    self.konversiDanPushKeToken()
                    self.maju()
                    
                elif(self.currentChar==" "):
                    self.konversiTempJikaBerisi()
                    self.maju()
                    
                elif(self.currentChar=="\n"):
                    self.konversiTempJikaBerisi()
                    self.gantiBaris()
                    self.clearTemp()
                    self.maju()
                
                else:
                    self.gantiState(states.identifier)
                        
                # elif(self.currentChar=="\n"):
                #     self.gantiBaris()
                #     self.maju()
                # else:
                #     self.maju()
                
            elif(self.state==states.numerik):
                if(self.currentChar.isdigit()):
                    self.simpenCharKeTemp()
                    self.maju()

                elif(self.currentChar=="."):
                    if(dotCount<1):
                        dotCount+=1
                        self.simpenCharKeTemp()
                        self.maju()
                    else:   
                        # self.errorhandlerObjek.tambahinError(self.barisIterator, self.kolomIterator, __name__, self.temp, 1)
                        self.errorhandlerObjek.tambahinError(__name__, 1, self.barisIterator, self.kolomIterator, self.temp)
                        # self.errorhandlerObjek.kirimError(__name__, 1, self.barisIterator, self.kolomIterator, self.temp)
                        self.maju()
                        # return self.errorhandlerObjek.kirimError(self.barisIterator, self.kolomIterator, __name__, self.temp, 1)
                # elif(self.currentChar in kurungList or self.currentChar in punctuationList):
                #     self.gantiState(states.punctuatorBracket)
                    
                else:
                    if(self.currentChar==" " or self.currentChar=="\n" or self.currentChar==tataBahasa.KEYWORD_DLMR or self.currentChar in kurungList or self.currentChar in punctuationList):
                        if(invalidFlag):
                            # print("invld")
                            self.konversiDanPushKeToken(tataBahasa.T_IVTF)
                        else:
                            if(dotCount<1):
                                self.konversiDanPushKeToken(tataBahasa.T_LITERAL_INT)
                                # self.pushTempKeToken(tataBahasa.T_LITERAL_INT)
                                
                            else:
                                self.konversiDanPushKeToken(tataBahasa.T_LITERAL_FLOAT)
                        self.gantiState(states.default)

                    else:
                        invalidFlag=True
                        self.simpenCharKeTemp()
                        self.maju()
                        
            
            elif(self.state==states.string):
                self.simpenCharKeTemp()
                self.maju()
                if(p_fileMentahan[self.pointerIterator]=='"'):
                    self.konversiDanPushKeToken(tataBahasa.T_LITERAL_STR)
                    self.state=states.default
                    self.maju()
                if(self.pointerIterator>=7):
                    pass
            
            elif(self.state==states.simbol):
                if(self.currentChar in simbolList.keys() or self.currentChar in operatorList.keys() or self.currentChar in perbandinganList.keys()):
                    tempMerged : str = self.currentChar+self.forwardChar
                    if(tempMerged==tataBahasa.CMNT_SNGL):
                        self.maju()
                        self.gantiState(states.singleLineComment)
                    elif(tempMerged in perbandinganList.keys() or tempMerged in operatorList.keys()):
                        self.konversiTempJikaBerisi()
                        # self.simpenCharKeTemp()
                        self.simpenKeTemp(tempMerged)
                        self.maju()
                        # self.simpenCharKeTemp()
                        self.konversiDanPushKeToken()
                        self.maju()
                    else:
                        self.konversiTempJikaBerisi()
                        self.simpenCharKeTemp()
                        self.konversiDanPushKeToken()
                        self.maju()
                else:
                    self.state=states.default
                    
            elif(self.state==states.identifier):
                # if(self.currentChar==" " or self.currentChar=="\n" or self.currentChar==tataBahasa.KEYWORD_DLMR):
                if(self.currentChar==" " or self.currentChar=="\n" or self.currentChar==tataBahasa.KEYWORD_DLMR or self.currentChar in perbandinganList.keys() or self.currentChar in operatorList.keys() or self.currentChar+self.forwardChar in perbandinganList.keys()):
                    if(invalidFlag):
                        self.konversiDanPushKeToken(tataBahasa.T_IVTF)
                    self.gantiState(states.default)

                elif(self.currentChar in kurungList.keys() or self.currentChar in punctuationList.keys()):
                    self.gantiState(states.punctuatorBracket)
                
                # elif(self.currentChar==tataBahasa.OPERATOR_PLUS or self.currentChar==tataBahasa.OPERATOR_MINS):
                #     # self.konversiTempJikaBerisi()
                #     # self.simpenCharKeTemp()
                #     # self.konversiDanPushKeToken()
                #     # self.maju()
                #     self.gantiState(states.simbol)
                    
                elif(self.currentChar in simbolList.keys()):
                    invalidFlag=True
                    self.simpenCharKeTemp()
                    self.maju()
                else:
                    # if(self.currentChar==tataBahasa.OPERATOR_DIVE and self.forwardChar==tataBahasa.OPERATOR_DIVE):
                    #     self.maju()
                    #     self.gantiState(states.singleLineComment)
                        
                    # elif(self.currentChar==tataBahasa.OPERATOR_DIVE and self.forwardChar==tataBahasa.OPERATOR_MULT):
                    #     self.maju()
                    #     self.gantiState(states.multiLineComment)
                        
                    # else:
                    #     self.simpenCharKeTemp()
                    self.simpenCharKeTemp()
                    self.maju()
            
            elif(self.state==states.singleLineComment):
                
                if(self.currentChar=="\n"):
                    self.gantiBaris()
                    self.maju()
                    self.gantiState(states.default)
                else:
                    self.maju()
                    
            elif(self.state==states.multiLineComment):
                if(self.currentChar==tataBahasa.OPERATOR_MULT and self.forwardChar==tataBahasa.OPERATOR_DIVE):
                    if(kedalamanMultiComment<=0):
                        self.maju()
                        self.maju()
                        self.gantiState(states.default)
                    else:
                        self.maju()
                        kedalamanMultiComment-=1
                    
                elif(self.currentChar==tataBahasa.OPERATOR_DIVE and self.forwardChar==tataBahasa.OPERATOR_MULT):
                    kedalamanMultiComment+=1
                    self.maju()
                    # self.gantiState(states.multiLineComment)
                else:
                    self.maju()
                
            elif(self.state==states.punctuatorBracket):
                if(self.currentChar in kurungList or self.currentChar in punctuationList):
                    self.konversiTempJikaBerisi()
                    self.simpenCharKeTemp()
                    self.konversiDanPushKeToken()
                    self.maju()
                else:
                    self.gantiState(states.default)
        else:
            self.konversiTempJikaBerisi()
            # if(len(self.temp)>0):
            #     self.konversiDanPushKeToken()
            # self.konversiDanPushKeToken()
            
        # print("\n")
        # for token in self.tokens:
        #     print("[",token.tipe,":", token.nilai,"]")
        #     if("T_DLMR" == token.tipe):
        #         print("\n")