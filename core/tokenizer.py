from keywords import keywordList
from keywords import primitiveList
from dataFormat import Token
# from keywords import primitiveList
import tataBahasa

class tokenizerClass:
    def __init__(self):
        # self.leksem : list[str] = []
        # self.tokens : list[str] = []
        pass
    
    def getToken(self, p_leksem : str, p_datatype : str = "")->Token:
        if(len(p_datatype)==0):
            if(p_leksem in keywordList.keys()):
                return Token(tataBahasa.KEYWORD_SYS_KYWR,keywordList.get(p_leksem, "ERR"))
            
            elif(p_leksem in primitiveList.keys()):
                return Token(tataBahasa.KEYWORD_SYS_KYWR,primitiveList.get(p_leksem, "ERR"))
            
            else:
                return Token(tataBahasa.KEYWORD_SYS_LTRL, p_leksem)
            pass
        else:
            if(p_datatype in primitiveList.keys()):
                return Token(primitiveList.get(p_datatype, tataBahasa.SYS_ERR), p_leksem)
            else:
                return Token("ERROR", "ERROR")
            pass