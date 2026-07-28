# from data_language.keywords import keywordList
# from data_language.keywords import primitiveList
# from data_language.keywords import operatorList
# from data_language.keywords import literalList
# from data_language.keywords import simbolList
# from data_language.keywords import kurungList
# from data_language.keywords import punctuationList
# from data_language.keywords import perbandinganList
# from data_language.dataFormat import Token
from data_language.tokens import tokenClass
from data_language.tokens import tokenType
# import data_language.tataBahasa as tataBahasa
from data_language import grammar

class tokenizerClass:
    def __init__(self):
        pass
    
    def getToken(self, p_baris : int, p_kolom : int, p_leksem : str, p_datatype : str = "")->tokenClass:
        if(len(p_datatype)==0):
            if(p_leksem in grammar.literalList.keys()):
                return tokenClass(p_baris, p_kolom, grammar.literalList.get(p_leksem, tokenType.T_EROR), p_leksem)
            
            elif(p_leksem in grammar.keywordList.keys()):
                return tokenClass(p_baris, p_kolom, grammar.keywordList.get(p_leksem, tokenType.T_EROR), p_leksem)
                # return tokenClass(tataBahasa.KEYWORD_SYS_KYWR,keywordList.get(p_leksem, tokenType.T_EROR))
            
            elif(p_leksem in grammar.primitiveList.keys()):
                return tokenClass(p_baris, p_kolom, grammar.primitiveList.get(p_leksem, tokenType.T_EROR), p_leksem)
                # return tokenClass(tataBahasa.KEYWORD_SYS_KYWR,primitiveList.get(p_leksem, tokenType.T_EROR))
            
            elif(p_leksem in grammar.operatorList.keys()):
                return tokenClass(p_baris, p_kolom, grammar.operatorList.get(p_leksem,tokenType.T_EROR), p_leksem)
            
            elif(p_leksem in grammar.simbolList.keys()):
                return tokenClass(p_baris, p_kolom, grammar.simbolList.get(p_leksem,tokenType.T_EROR), p_leksem)
            
            elif(p_leksem in grammar.kurungList.keys()):
                return tokenClass(p_baris, p_kolom, grammar.kurungList.get(p_leksem,tokenType.T_EROR), p_leksem)
            
            elif(p_leksem in grammar.punctuationList.keys()):
                return tokenClass(p_baris, p_kolom, grammar.punctuationList.get(p_leksem,tokenType.T_EROR), p_leksem)
            
            elif(p_leksem in grammar.perbandinganList.keys()):
                return tokenClass(p_baris, p_kolom, grammar.perbandinganList.get(p_leksem,tokenType.T_EROR), p_leksem)
            
            # elif(p_leksem in perbandinganList.keys()):
            #     return tokenClass(p_baris, p_kolom, perbandinganList.get(p_leksem,tokenType.T_EROR), p_leksem)
            
            else:
                return tokenClass(p_baris, p_kolom, tokenType.T_IDTF, p_leksem)
            
        else:
            if(p_datatype in grammar.literalList.keys()):
                return tokenClass(p_baris, p_kolom, grammar.literalList.get(p_datatype, tokenType.T_EROR), p_leksem)
            if(p_datatype == grammar.T_IVTF):
                return tokenClass(p_baris, p_kolom, tokenType.T_IVTF, p_leksem)
            else:
                return tokenClass(0, 0, tokenType.T_EROR, "ERROR")
