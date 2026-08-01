# from lekser import lekserClass
from modul_baca.lekser import lekserClass
from modul_parsing.parser import parserClass
# from data_language.tokens import tokenType
from modul_semantik.analisa import semantikClass
from modul_parsing.AST import ASTClass

from data_language.tokens import tokenClass
from errorHandler import errorHandlerClass
# from tokenizer import tokenizerClass

def run(fileOriginal : str) -> None:
    errorHandlerObjek = errorHandlerClass()
    lekserObjek = lekserClass(errorHandlerObjek)
    parserObjek = parserClass(errorHandlerObjek)
    semantikObjek = semantikClass(errorHandlerObjek)
    # tokenizerObjek = tokenizerClass()

    lekserProsesing : None = lekserObjek.proses(fileOriginal)
    tokens : list[tokenClass] = lekserObjek.ambilTokens()
    # print(tokens)
    parserProsesing : None = parserObjek.proses(tokens)

    if(errorHandlerObjek.adaError()):
        errorHandlerObjek.displayError()
    else:
        # parserObjek.getTree().printTree()
        semantikProsesing : None = semantikObjek.proses(parserObjek.getTree())
        pass
    
    # if(lekserProsesing is None):
    #     tokens : list[Token] = lekserObjek.ambilTokens()
    #     parserProsesing : str | None = parserObjek.proses(tokens)

    #     if(parserProsesing is None):
    #         pass
        
    #     else:
    #         print(parserProsesing)
    #         pass
        
    # #     # print("\n")
    # for token in tokens:
    #     print("[",token.tipe,":", token.nilai,"]")
    #     if(token.tipe == tokenType.T_DLMR or token.tipe == tokenType.T_AKHR):
    #         print("\n")
    #         pass
    #     # tokenizerProsesing : str|None = tokenizerObjek.proses(leksems)
        
    #     # if(tokenizerProsesing is None):
    #     #     print(leksems)
    #     #     print(tokenizerObjek.getTokens())
            
    #     # else:print(tokenizerProsesing)
    
    # else:print(lekserProsesing)