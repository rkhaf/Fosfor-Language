from lekser import lekserClass
from tokenizer import tokenizerClass

def run(fileOriginal : str) -> None:
    lekserObjek = lekserClass()
    tokenizerObjek = tokenizerClass()
    
    lekserObjek.proses(fileOriginal)
    
    leksems : list[str] = lekserObjek.getLeksem()
    
    tokenizerObjek.proses(leksems)
    
    print(leksems)
    print(tokenizerObjek.getTokens())
    pass