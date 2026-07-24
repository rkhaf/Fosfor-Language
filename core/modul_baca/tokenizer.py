from data_language.keywords import keywordList
from data_language.keywords import primitiveList
from data_language.keywords import operatorList
from data_language.keywords import literalList
from data_language.keywords import simbolList
from data_language.dataFormat import Token
import data_language.tataBahasa as tataBahasa

class tokenizerClass:
    def __init__(self):
        pass
    
    def getToken(self, p_baris : int, p_kolom : int, p_leksem : str, p_datatype : str = "")->Token:
        if(len(p_datatype)==0):
            if(p_leksem in literalList.keys()):
                return Token(p_baris, p_kolom, literalList.get(p_leksem, "ERR"), p_leksem)
            
            elif(p_leksem in keywordList.keys()):
                return Token(p_baris, p_kolom, keywordList.get(p_leksem, "ERR"), p_leksem)
                # return Token(tataBahasa.KEYWORD_SYS_KYWR,keywordList.get(p_leksem, "ERR"))
            
            elif(p_leksem in primitiveList.keys()):
                return Token(p_baris, p_kolom, primitiveList.get(p_leksem, "ERR"), p_leksem)
                # return Token(tataBahasa.KEYWORD_SYS_KYWR,primitiveList.get(p_leksem, "ERR"))
            
            elif(p_leksem in operatorList.keys()):
                return Token(p_baris, p_kolom, operatorList.get(p_leksem,"ERR"), p_leksem)
            
            elif(p_leksem in simbolList.keys()):
                return Token(p_baris, p_kolom, simbolList.get(p_leksem,"ERR"), p_leksem)
            
            else:
                return Token(p_baris, p_kolom, tataBahasa.T_IDTF, p_leksem)
            
        else:
            if(p_datatype in literalList.keys()):
                return Token(p_baris, p_kolom, literalList.get(p_datatype, tataBahasa.SYS_ERR), p_leksem)
            if(p_datatype == tataBahasa.T_IVTF):
                return Token(p_baris, p_kolom, tataBahasa.T_IVTF, p_leksem)
            else:
                return Token(0, 0, "ERROR", "ERROR")
