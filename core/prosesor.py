# from lekser import lekserClass
from modul_baca.lekser import lekserClass
from modul_parsing.parser import parserClass
# from data_language.tokens import tokenType
from modul_semantik.analisa import semantikClass
# from modul_parsing.AST import ASTClass
from modul_translator.codeGenerator import codeGeneratorClass
from modul_linker.importHandler import importHandler

from data_language.tokens import tokenClass
from errorHandler import errorHandlerClass
from modul_translator.LLVMMerger import LLVMMergerClass
from metadata.builtins import builtinClass
import subprocess
# from tokenizer import tokenizerClass

def run(fileOriginal : str, p_namaFile : str) -> None:
    errorHandlerObjek = errorHandlerClass()
    lekserObjek : lekserClass = lekserClass(errorHandlerObjek)
    parserObjek : parserClass = parserClass(errorHandlerObjek)
    konverterObjek : LLVMMergerClass = LLVMMergerClass()
    importHandlerObjek : importHandler = importHandler()
    builtinObjek : builtinClass = builtinClass()
    codegenObjek : codeGeneratorClass = codeGeneratorClass(errorHandlerObjek, builtinObjek)
    semantikObjek : semantikClass = semantikClass(errorHandlerObjek, builtinObjek)
    # tokenizerObjek = tokenizerClass()

    # codegenObjek.
    lekserObjek.proses(fileOriginal)
    tokens : list[tokenClass] = lekserObjek.ambilTokens()
    parserObjek.proses(tokens)

    # print(tokens)
    
    if(errorHandlerObjek.adaError()):
        errorHandlerObjek.displayError()
    else:
        parserObjek.getTree().printTree()
    #     importHandlerObjek.proses(parserObjek.getTree())
    #     builtinObjek.proses(importHandlerObjek.getLLVMBuiltinMapping(), importHandlerObjek.getFosBuiltinMapping())
    #     semantikObjek.proses(parserObjek.getTree())
    # #     # # semantikObjek.printScopes()
    #     if(errorHandlerObjek.adaError()):
    #         errorHandlerObjek.displayError()
    #     else:
    #         codegenObjek.proses(parserObjek.getTree())
    #         if(errorHandlerObjek.adaError()):
    #             errorHandlerObjek.displayError()
    #         else:
    #             # print(str(codegenObjek.modul))
    #             # print(importHandlerObjek.getRuntimePathList(), "done")
    #             konverterObjek.proses(True,p_namaFile, codegenObjek.getModul(), "", importHandlerObjek.getRuntimePathList())
                # subprocess.run(["./"+str()])
        pass