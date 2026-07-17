# import tataBahasa

from enum import Enum
from errorHandler import errorHandlerClass
from modul_baca.tokenizer import tokenizerClass
from data_language.dataFormat import Token

import data_language.tataBahasa as tataBahasa

class states(Enum):
    default = 1,
    numerik = 2,
    string = 3
            
class lekserClass:
    def __init__(self):
        self.errorhandlerObjek = errorHandlerClass()
        self.tokenizerObjek = tokenizerClass()
        self.state : states = states.default
        self.pointerIterator : int = 0
        self.barisIterator : int = 0
        self.kolomIterator : int = 0
        self.temp : str = ""
        self.currentChar : str = ""
        self.dotCount : int = 0
        self.fileOriginal : str = ""
        self.tokens : list[Token] = []
    
    def maju(self) -> None:
        self.pointerIterator+=1
        self.kolomIterator+=1
    
    def simpenCharKeTemp(self)->None:
        self.temp+=self.currentChar
    
    def gantiState(self, p_state : states)->None:
        self.state = p_state

    def konversiDanPushKeToken(self, p_tipedata : str = "")->None:
        if(len(p_tipedata)!=0):
            self.tokens.append(self.tokenizerObjek.getToken(self.temp,p_tipedata))

        else:
            self.tokens.append(self.tokenizerObjek.getToken(self.temp))

        self.temp=""
    
    def gantiBaris(self)->None:
        self.barisIterator+=1
        self.kolomIterator=0
    
    def proses(self, p_fileMentahan : str) -> str | None:
        while self.pointerIterator < len(p_fileMentahan):
            self.fileOriginal = p_fileMentahan
            self.currentChar = p_fileMentahan[self.pointerIterator]
            if(self.state==states.default):
                if(self.currentChar.isdigit()):
                    self.gantiState(states.numerik)
                    
                elif(self.currentChar=='"'):
                    self.gantiState(states.string)
                    self.maju()
                    
                elif(self.currentChar==";"):
                    self.konversiDanPushKeToken()
                    self.simpenCharKeTemp()
                    self.maju()
                    
                elif(self.currentChar==" "):
                    if(len(self.temp)!=0):
                        self.konversiDanPushKeToken()
                    self.maju()
                    
                elif(self.currentChar=="\n"):
                    self.konversiDanPushKeToken()
                    self.gantiBaris()
                    self.maju()

                    
                else:
                    self.simpenCharKeTemp()
                    self.maju()
                
            elif(self.state==states.numerik):
                if(self.currentChar.isdigit()):
                    self.simpenCharKeTemp()
                    self.maju()

                elif(self.currentChar=="."):
                    if(self.dotCount<1):
                        self.dotCount+=1
                        self.simpenCharKeTemp()
                        self.maju()
                    else:
                        return self.errorhandlerObjek.kirimError(self.barisIterator, self.kolomIterator, __name__, self.temp, 1)
                else:
                    if(self.dotCount<1):
                        self.konversiDanPushKeToken(tataBahasa.TIPEDATA_INT)
                        
                    else:
                        self.konversiDanPushKeToken(tataBahasa.TIPEDATA_FLOAT)
                        
                    self.gantiState(states.default)
            
            elif(self.state==states.string):
                self.simpenCharKeTemp()
                self.maju()
                if(p_fileMentahan[self.pointerIterator]=='"'):
                    self.konversiDanPushKeToken(tataBahasa.TIPEDATA_STR)
                    self.state=states.default
                    self.maju()
                if(self.pointerIterator>=7):
                    pass
            pass
        else:
            self.konversiDanPushKeToken()
        for token in self.tokens:
            print("[",token.tipe,":", token.nilai,"]")