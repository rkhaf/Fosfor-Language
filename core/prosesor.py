# from lekser import lekserClass
from modul_baca.lekser import lekserClass
from modul_parsing.parser import parserClass
# from data_language.tokens import tokenType
from modul_semantik.analisa import semantikClass
# from modul_parsing.AST import ASTClass
from modul_translator.codeGenerator import codeGeneratorClass

from data_language.tokens import tokenClass
from errorHandler import errorHandlerClass
from modul_translator.LLVMMerger import LLVMMergerClass
# from tokenizer import tokenizerClass

def run(fileOriginal : str, p_namaFile : str) -> None:
    errorHandlerObjek = errorHandlerClass()
    lekserObjek : lekserClass = lekserClass(errorHandlerObjek)
    parserObjek : parserClass = parserClass(errorHandlerObjek)
    semantikObjek : semantikClass = semantikClass(errorHandlerObjek)
    codegenObjek : codeGeneratorClass = codeGeneratorClass(errorHandlerObjek)
    konverterObjek : LLVMMergerClass = LLVMMergerClass()
    # tokenizerObjek = tokenizerClass()

    # codegenObjek.
    lekserObjek.proses(fileOriginal)
    tokens : list[tokenClass] = lekserObjek.ambilTokens()
    # print(tokens)
    parserObjek.proses(tokens)

    if(errorHandlerObjek.adaError()):
        errorHandlerObjek.displayError()
    else:
        # parserObjek.getTree().printTree()
        semantikObjek.proses(parserObjek.getTree())
        if(errorHandlerObjek.adaError()):
            errorHandlerObjek.displayError()
        else:
            codegenObjek.proses(parserObjek.getTree())
            if(errorHandlerObjek.adaError()):
                errorHandlerObjek.displayError()
            else:
                konverterObjek.proses(p_namaFile, codegenObjek.getModul(), "")
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