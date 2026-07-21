# from lekser import lekserClass
from modul_baca.lekser import lekserClass
from modul_parsing.parser import parserClass

from data_language.dataFormat import Token
# from tokenizer import tokenizerClass

def run(fileOriginal : str) -> None:
    lekserObjek = lekserClass()
    parserObjek = parserClass()
    # tokenizerObjek = tokenizerClass()
    
    lekserProsesing : str | None = lekserObjek.proses(fileOriginal)
    if(lekserProsesing is None):
        tokens : list[Token] = lekserObjek.ambilTokens()
        parserProsesing : str | None = parserObjek.proses(tokens)

        if(parserProsesing is None):
            pass
        
        else:
            pass
        
        # print("\n")
        # for token in tokens:
        #     print("[",token.tipe,":", token.nilai,"]")
        #     if("T_DLMR" == token.tipe):
        #         print("\n")
        # tokenizerProsesing : str|None = tokenizerObjek.proses(leksems)
        
        # if(tokenizerProsesing is None):
        #     print(leksems)
        #     print(tokenizerObjek.getTokens())
            
        # else:print(tokenizerProsesing)
    
    else:print(lekserProsesing)