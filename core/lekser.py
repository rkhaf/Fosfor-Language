# import tataBahasa
from enum import Enum
from errorHandler import errorHandlerClass

class states(Enum):
    default = 1,
    numerik = 2
            
class lekserClass:
    def __init__(self):
        # self.fileMentahan : str = ""
        self.errorhandlerObjek = errorHandlerClass()
        self.state : states = states.default
        self.leksem : list[str] = []
        self.kolomIterator : int = 0
        self.barisIterator : int = 0
        self.temp : str = ""
        self.currentChar : str = ""
        self.dotCount : int = 0
    
    def maju(self) -> None:
        self.kolomIterator+=1
        
    def proses(self, p_fileMentahan : str) -> None:
        while self.kolomIterator < len(p_fileMentahan):
            self.currentChar = p_fileMentahan[self.kolomIterator]
            if(self.state==states.default):
                if(self.currentChar.isdigit()):
                    self.state=states.numerik
                elif(self.currentChar==" "):
                    self.leksem.append(self.temp)
                    self.temp=""
                    self.maju()
                else:
                    self.temp+=self.currentChar
                    # print("default: "+self.currentChar)
                    self.maju()
                
            elif(self.state==states.numerik):
                if(self.currentChar.isdigit()):
                    self.temp+=self.currentChar
                    self.maju()
                elif(self.currentChar=="."):
                    if(self.dotCount<1):
                        self.dotCount+=1
                        self.temp+=self.currentChar
                        self.maju()
                    else:
                        print(self.errorhandlerObjek.kirimError(self.barisIterator, self.kolomIterator, __name__, 1))
                        return
                else:
                    self.state = states.default
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
    
    def getLeksem(self) -> list[str]:
        return self.leksem

# if __name__ == "__main__":
#     print("lekser ready")