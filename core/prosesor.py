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
import subprocess
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
    parserObjek.proses(tokens)

    # print(tokens)
    
    if(errorHandlerObjek.adaError()):
        errorHandlerObjek.displayError()
    else:
        # parserObjek.getTree().printTree()
        semantikObjek.proses(parserObjek.getTree())
        # semantikObjek.printScopes()
        if(errorHandlerObjek.adaError()):
            errorHandlerObjek.displayError()
        else:
            codegenObjek.proses(parserObjek.getTree())
            if(errorHandlerObjek.adaError()):
                errorHandlerObjek.displayError()
            else:
                # print(str(codegenObjek.modul))
                konverterObjek.proses(True,p_namaFile, codegenObjek.getModul(), "")
                # subprocess.run(["./"+str()])
        # pass