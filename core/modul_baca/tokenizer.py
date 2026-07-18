from data_language.keywords import keywordList
from data_language.keywords import primitiveList
from data_language.keywords import operatorList
from data_language.dataFormat import Token
import data_language.tataBahasa as tataBahasa

class tokenizerClass:
    def __init__(self):
        pass
    
    def getToken(self, p_leksem : str, p_datatype : str = "")->Token:
        if(len(p_datatype)==0):
            if(p_leksem in keywordList.keys()):
                return Token(tataBahasa.KEYWORD_SYS_KYWR,keywordList.get(p_leksem, "ERR"))
            
            elif(p_leksem in primitiveList.keys()):
                return Token(tataBahasa.KEYWORD_SYS_KYWR,primitiveList.get(p_leksem, "ERR"))
            
            elif(p_leksem in operatorList.keys()):
                return Token(tataBahasa.KEYWORD_SYS_OPRT,operatorList.get(p_leksem,"ERR"))
            
            else:
                return Token(tataBahasa.KEYWORD_SYS_LTRL, p_leksem)
            pass
        else:
            if(p_datatype in primitiveList.keys()):
                return Token(primitiveList.get(p_datatype, tataBahasa.SYS_ERR), p_leksem)
            else:
                return Token("ERROR", "ERROR")
            pass