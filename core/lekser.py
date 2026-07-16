# import tataBahasa

from enum import Enum
from errorHandler import errorHandlerClass
from keywords import primitiveList
import tataBahasa

class states(Enum):
    default = 1,
    numerik = 2,
    string = 3
            
class lekserClass:
    def __init__(self):
        # self.fileMentahan : str = ""
        self.errorhandlerObjek = errorHandlerClass()
        self.state : states = states.default
        self.leksem : list[str | list[str]] = []
        self.kolomIterator : int = 0
        self.barisIterator : int = 0
        self.temp : str = ""
        self.currentChar : str = ""
        self.dotCount : int = 0
        self.strMode : bool = False
        self.fileOriginal : str = ""
    
    def maju(self) -> None:
        self.kolomIterator+=1
        # self.currentChar = self.fileOriginal[self.kolomIterator]
    
    def simpenCharKeTemp(self)->None:
        self.temp+=self.currentChar
    
    def gantiState(self, p_state : states)->None:
        self.state = p_state
    
    def simpenTempKeLeksem(self)->None:
        self.leksem.append(self.temp)
        self.temp=""
    
    def simpanListTempKeLeksem(self, p_datatype : str)->None:
        self.leksem.append([p_datatype, self.temp])
        self.temp=""
    
    def proses(self, p_fileMentahan : str) -> str | None:
        while self.kolomIterator < len(p_fileMentahan):
            self.fileOriginal = p_fileMentahan
            self.currentChar = p_fileMentahan[self.kolomIterator]
            if(self.state==states.default):
                if(self.currentChar.isdigit()):
                    self.gantiState(states.numerik)
                    
                elif(self.currentChar=='"'):
                    self.gantiState(states.string)
                    self.maju()
                    
                elif(self.currentChar==" " or self.currentChar==";"):
                    self.simpenTempKeLeksem()
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
                    self.gantiState(states.default)
            
            elif(self.state==states.string):
                self.simpenCharKeTemp()
                self.maju()
                if(p_fileMentahan[self.kolomIterator]=='"'):
                    # self.simpenTempKeLeksem("STR:")
                    self.simpanListTempKeLeksem(primitiveList.get(tataBahasa.TIPEDATA_STR,""))
                    self.state=states.default
                    self.maju()
                # if(self.currentChar!='"' and not self.strMode):
                #     simpenCharKeTemp()
                #     self.maju()
                # elif(self.currentChar!='"' and self.strMode):
                #     self.state=states.default
                # else:
                #     print("trapped")
            pass
            
                # if(p_fileMentahan[self.kolomIterator]==tataBahasa.KEYWORD_SYS_DLMR):
                #     if(len(self.temp)>0):
                #         self.leksem.append(self.temp)
                #     self.leksem.append(p_fileMentahan[self.kolomIterator])
                # elif(p_fileMentahan[self.kolomIterator]!=" "):
                #     self.temp+=p_fileMentahan[self.kolomIterator]
                # else:
                #     self.barisIterator+=1
                #     self.leksem.append(self.temp)
                #     self.temp=""
            
            # self.kolomIterator+=1
        
    
    def getLeksem(self) -> list[str | list[str]]:
        return self.leksem

# if __name__ == "__main__":
#     print("lekser ready")