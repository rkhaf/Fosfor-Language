# import tataBahasa

from enum import Enum
from errorHandler import errorHandlerClass
from tokenizer import tokenizerClass
# from keywords import primitiveList
from dataFormat import Token

import tataBahasa

class states(Enum):
    default = 1,
    numerik = 2,
    string = 3
            
class lekserClass:
    def __init__(self):
        # self.fileMentahan : str = ""
        self.errorhandlerObjek = errorHandlerClass()
        self.tokenizerObjek = tokenizerClass()
        self.state : states = states.default
        # self.leksem : list[Token] = []
        self.pointerIterator : int = 0
        self.barisIterator : int = 0
        self.kolomIterator : int = 0
        self.temp : str = ""
        self.currentChar : str = ""
        self.dotCount : int = 0
        # self.strMode : bool = False
        self.fileOriginal : str = ""
        self.tokens : list[Token] = []
    
    def maju(self) -> None:
        self.pointerIterator+=1
        self.kolomIterator+=1
        # self.currentChar = self.fileOriginal[self.pointerIterator]
    
    def simpenCharKeTemp(self)->None:
        self.temp+=self.currentChar
    
    def gantiState(self, p_state : states)->None:
        self.state = p_state
    
    # def simpenTempKeLeksem(self)->None:
    #     self.leksem.append(self.temp)
    #     self.temp=""
    
    # def simpanListTempKeLeksem(self, p_datatype : str)->None:
    #     self.leksem.append([p_datatype, self.temp])
    #     self.temp=""
    
    def konversiDanPushKeToken(self, p_tipedata : str = "")->None:
        if(len(p_tipedata)!=0):
            self.tokens.append(self.tokenizerObjek.getToken(self.temp,p_tipedata))
            # pass
        # self.tokens.append(Token(p_tipe,self.temp))
        else:
            self.tokens.append(self.tokenizerObjek.getToken(self.temp))
            # pass
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
                # elif(self.currentChar==" " or self.currentChar==";"):
                    if(len(self.temp)!=0):
                        # self.simpenTempKeLeksem()
                        self.konversiDanPushKeToken()
                    self.maju()
                    
                elif(self.currentChar=="\n"):
                    # self.barisIterator+=1
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
                    # self.simpenTempKeLeksem("STR:")
                    # self.simpanListTempKeLeksem(primitiveList.get(tataBahasa.TIPEDATA_STR,""))
                    self.konversiDanPushKeToken(tataBahasa.TIPEDATA_STR)
                    self.state=states.default
                    self.maju()
                # if(self.currentChar!='"' and not self.strMode):
                #     simpenCharKeTemp()
                #     self.maju()
                # elif(self.currentChar!='"' and self.strMode):
                #     self.state=states.default
                # else:
                #     print("trapped")
                if(self.pointerIterator>=7):
                    pass
            pass
        else:
            # self.simpenCharKeTemp()
            self.konversiDanPushKeToken()
        # print(self.tokens)
        for token in self.tokens:
            print(token.tipe," : ", token.nilai)
                # if(p_fileMentahan[self.pointerIterator]==tataBahasa.KEYWORD_SYS_DLMR):
                #     if(len(self.temp)>0):
                #         self.leksem.append(self.temp)
                #     self.leksem.append(p_fileMentahan[self.pointerIterator])
                # elif(p_fileMentahan[self.pointerIterator]!=" "):
                #     self.temp+=p_fileMentahan[self.pointerIterator]
                # else:
                #     self.barisIterator+=1
                #     self.leksem.append(self.temp)
                #     self.temp=""
            
            # self.pointerIterator+=1
        
    
    # def getLeksem(self) -> list[str | list[str]]:
    #     return self.leksem

# if __name__ == "__main__":
#     print("lekser ready")