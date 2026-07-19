from data_language.keywords import keywordList
from data_language.keywords import primitiveList
from data_language.keywords import operatorList
from data_language.keywords import literalList
from data_language.dataFormat import Token
import data_language.tataBahasa as tataBahasa

class tokenizerClass:
    def __init__(self):
        pass
    
    def getToken(self, p_leksem : str, p_datatype : str = "")->Token:
        if(len(p_datatype)==0):
            if(p_leksem in literalList.keys()):
                return Token(literalList.get(p_leksem, "ERR"), p_leksem)
            
            elif(p_leksem in keywordList.keys()):
                return Token(keywordList.get(p_leksem, "ERR"), p_leksem)
                # return Token(tataBahasa.KEYWORD_SYS_KYWR,keywordList.get(p_leksem, "ERR"))
            
            elif(p_leksem in primitiveList.keys()):
                return Token(primitiveList.get(p_leksem, "ERR"), p_leksem)
                # return Token(tataBahasa.KEYWORD_SYS_KYWR,primitiveList.get(p_leksem, "ERR"))
            
            elif(p_leksem in operatorList.keys()):
                return Token(operatorList.get(p_leksem,"ERR"), p_leksem)
                # return Token(tataBahasa.KEYWORD_SYS_OPRT,operatorList.get(p_leksem,"ERR"))
            
            else:
                return Token(tataBahasa.T_IDTF, p_leksem)
            
        else:
            if(p_datatype in literalList.keys()):
                return Token(literalList.get(p_datatype, tataBahasa.SYS_ERR), p_leksem)
            else:
                return Token("ERROR", "ERROR")
