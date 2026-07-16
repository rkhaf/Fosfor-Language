from lekser import lekserClass
from tokenizer import tokenizerClass

def run(fileOriginal : str) -> None:
    lekserObjek = lekserClass()
    tokenizerObjek = tokenizerClass()
    
    lekserProsesing : str | None = lekserObjek.proses(fileOriginal)
    if(lekserProsesing is None):
        leksems : list[str] = lekserObjek.getLeksem()
        tokenizerProsesing : str|None = tokenizerObjek.proses(leksems)
        
        if(tokenizerProsesing is None):
            print(leksems)
            print(tokenizerObjek.getTokens())
            
        else:print(tokenizerProsesing)
    
    else:print(lekserProsesing)