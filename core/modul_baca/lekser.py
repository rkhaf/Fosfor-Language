# import tataBahasa

from enum import Enum
from errorHandler import errorHandlerClass
from modul_baca.tokenizer import tokenizerClass
# from data_language.dataFormat import Token
from data_language.tokens import tokenClass
# from core.data_language.tokens import tokenType
from data_language import grammar
# from data_language.grammar import simbolList
# from data_language.grammar import kurungList
# from data_language.grammar import punctuationList
# from data_language.grammar import operatorList
# from data_language.grammar import perbandinganList

# import data_language.grammar as tataBahasa

class states(Enum):
    default = 1,
    numerik = 2,
    string = 3,
    simbol = 4,
    identifier = 5,
    singleLineComment = 6,
    multiLineComment = 7,
    punctuatorBracket = 8
            
class lekserClass:
    def __init__(self, p_errorHandlerReference : errorHandlerClass):
        self.errorhandlerObjek : errorHandlerClass = p_errorHandlerReference
        self.tokenizerObjek = tokenizerClass()
        self.state : states = states.default
        self.pointerIterator : int = 0
        self.barisIterator : int = 1
        self.kolomIterator : int = 1
        self.temp : str = ""
        self.currentChar : str = ""
        self.forwardChar : str = ""
        self.fileOriginal : str = ""
        self.tokens : list[tokenClass] = []
        self.commentStart : list[int] = [0,0]
        
    def maju(self) -> None:
        self.pointerIterator+=1
        self.kolomIterator+=1
        if(self.pointerIterator>=20):
            pass
    
    def simpenCharKeTemp(self)->None:
        self.temp+=self.currentChar
        
    def simpenKeTemp(self, p_val : str)->None:
        self.temp+=p_val
    
    def gantiState(self, p_state : states)->None:
        self.state = p_state

    def konversiDanPushKeToken(self, p_tipedata : str = "")->None:
        if(len(p_tipedata)!=0):
            self.tokens.append(self.tokenizerObjek.getToken(self.barisIterator, self.kolomIterator, self.temp,p_tipedata))
            
        else:
            self.tokens.append(self.tokenizerObjek.getToken(self.barisIterator, self.kolomIterator, self.temp))
        self.temp=""
    
    # def pushTempKeToken(self, p_tipeToken : str)->None:
    #     self.tokens.append(Token(self.barisIterator, self.kolomIterator, p_tipeToken, self.temp))
    #     self.temp=""
    
    def clearTemp(self)->None:
        self.temp=""
    
    def gantiBaris(self)->None:
        self.barisIterator+=1
        self.kolomIterator=0
        self.commentFlag=False
    
    def konversiTempJikaBerisi(self)->None:
        if(len(self.temp)>0):
            self.konversiDanPushKeToken()
    
    def ambilTokens(self)->list[tokenClass]:
        return self.tokens
    
    def proses(self, p_fileMentahan : str) -> str | None:
        kedalamanMultiComment : int = 0
        invalidFlag : bool = False
        dotCount : int = 0
        # commentStartLine : int = 0
        
        while self.pointerIterator < len(p_fileMentahan):
            self.fileOriginal = p_fileMentahan #nyalin sourcecode
            
            #ngesinkronin currentChar
            self.currentChar = self.fileOriginal[self.pointerIterator]
            if(self.pointerIterator<len(self.fileOriginal)-1):
                self.forwardChar = self.fileOriginal[self.pointerIterator+1]
            
            # state default
            if(self.state==states.default):
                dotCount=0
                invalidFlag=False
                
                # if dibawah ini smpe ke else fungsinya bwt deteksi state doang
                if(self.currentChar+self.forwardChar==grammar.CMNT_SNGL):
                    self.gantiState(states.singleLineComment)
                    
                elif(self.currentChar+self.forwardChar==grammar.CMNT_MLTI_OPEN):
                    self.gantiState(states.multiLineComment)
                    
                elif(self.currentChar.isdigit()):
                    self.konversiTempJikaBerisi()
                    self.gantiState(states.numerik)
                    
                elif(self.currentChar=='"'):
                    self.gantiState(states.string)
                    self.maju()
                    
                elif(self.currentChar in grammar.simbolList.keys() or self.currentChar in grammar.perbandinganList.keys() or self.currentChar in grammar.operatorList.keys()):
                    self.gantiState(states.simbol)

                elif(self.currentChar==grammar.KEYWORD_DLMR):
                    self.konversiTempJikaBerisi()
                    self.simpenCharKeTemp()
                    self.konversiDanPushKeToken()
                    self.maju()
                    
                elif(self.currentChar==" "):
                    self.konversiTempJikaBerisi()
                    self.maju()
                    
                elif(self.currentChar=="\n"):
                    self.konversiTempJikaBerisi()
                    self.gantiBaris()
                    self.clearTemp()
                    self.maju()
                
                else:
                    self.gantiState(states.identifier)

            # state numerik
            elif(self.state==states.numerik):
                # deteksi apkh karakter numerik
                if(self.currentChar.isdigit()):
                    self.simpenCharKeTemp()
                    self.maju()

                # deteksi dot buat float
                elif(self.currentChar=="."):
                    # ngecek validitas pengisian literal float
                    if(dotCount<1):
                        dotCount+=1
                        self.simpenCharKeTemp()
                        self.maju()
                    else:
                        self.errorhandlerObjek.tambahinError(__name__, 1, self.barisIterator, self.kolomIterator, self.temp)
                        self.maju()
                    
                else:
                    # selain elemen yg boleh dibaca berbarengan dgn numerik
                    if(self.currentChar==" " or self.currentChar=="\n" or self.currentChar==grammar.KEYWORD_DLMR or self.currentChar in grammar.kurungList.keys() or self.currentChar in grammar.punctuationList.keys() or self.currentChar in grammar.operatorList.keys()):
                        # ngecek apkh udh diflag invalid apa nggk
                        if(invalidFlag):
                            # print("invld")
                            self.konversiDanPushKeToken(grammar.T_IVTF)
                            
                        else:
                            # ngecek jenis literal
                            if(dotCount<1):
                                self.konversiDanPushKeToken(grammar.T_LITERAL_INT)
                                
                            else:
                                self.konversiDanPushKeToken(grammar.T_LITERAL_FLOAT)
                        self.gantiState(states.default)

                    else:
                        # ngeflag token jdi invalid
                        invalidFlag=True
                        self.simpenCharKeTemp()
                        self.maju()
                        
            # state string
            elif(self.state==states.string):
                self.simpenCharKeTemp()
                self.maju()
                
                #safeguard bwt stopper klo semisal lupa ditutup
                if(self.pointerIterator<len(self.fileOriginal)):
                    # ngecek stopper utk stringnya
                    if(p_fileMentahan[self.pointerIterator]=='"'):
                        self.konversiDanPushKeToken(grammar.T_LITERAL_STR)
                        self.state=states.default
                        self.maju()
                else:
                    self.errorhandlerObjek.tambahinError(__name__, 2, self.barisIterator, self.kolomIterator, self.temp)
                    
            
            # state simbol
            elif(self.state==states.simbol):
                # ngecek apkh char skrg masih didalem simbol, operator, perbandingan
                if(self.currentChar in grammar.simbolList.keys() or self.currentChar in grammar.operatorList.keys() or self.currentChar in grammar.perbandinganList.keys()):
                    tempMerged : str = self.currentChar+self.forwardChar
                    # # state default
                    # if(tempMerged==grammar.CMNT_SNGL):
                    #     self.maju()
                    #     self.gantiState(states.singleLineComment)
                    if(tempMerged in grammar.perbandinganList.keys() or tempMerged in grammar.operatorList.keys()):
                        self.konversiTempJikaBerisi()
                        self.simpenKeTemp(tempMerged)
                        self.maju()
                        self.konversiDanPushKeToken()
                        self.maju()
                    else:
                        self.konversiTempJikaBerisi()
                        self.simpenCharKeTemp()
                        self.konversiDanPushKeToken()
                        self.maju()
                else:
                    self.state=states.default
                    
            elif(self.state==states.identifier):
                if(self.currentChar==" " or self.currentChar=="\n" or self.currentChar==grammar.KEYWORD_DLMR or self.currentChar in grammar.perbandinganList.keys() or self.currentChar in grammar.operatorList.keys() or self.currentChar+self.forwardChar in grammar.perbandinganList.keys()):
                    if(invalidFlag):
                        self.konversiDanPushKeToken(grammar.T_IVTF)
                    self.gantiState(states.default)

                elif(self.currentChar in grammar.kurungList.keys() or self.currentChar in grammar.punctuationList.keys()):
                    if(invalidFlag):
                        self.konversiDanPushKeToken(grammar.T_IVTF)
                    self.gantiState(states.punctuatorBracket)
                    
                elif(self.currentChar in grammar.simbolList.keys()):
                    invalidFlag=True
                    self.simpenCharKeTemp()
                    self.maju()
                    
                else:
                    self.simpenCharKeTemp()
                    self.maju()
                pass
            
            elif(self.state==states.singleLineComment):
                
                if(self.currentChar=="\n"):
                    self.gantiBaris()
                    self.maju()
                    self.gantiState(states.default)
                else:
                    self.maju()
                    
            elif(self.state==states.multiLineComment):
                if(self.currentChar==grammar.OPERATOR_DIVE and self.forwardChar==grammar.OPERATOR_MULT):
                    if(kedalamanMultiComment<=0):
                        self.commentStart[0] = self.barisIterator
                        self.commentStart[1] = self.kolomIterator
                    kedalamanMultiComment+=1
                    self.maju()
                    
                if(kedalamanMultiComment>0):
                    if(self.currentChar==grammar.OPERATOR_MULT and self.forwardChar==grammar.OPERATOR_DIVE):
                        if(kedalamanMultiComment<=0):
                            self.maju()
                            self.maju()
                            self.gantiState(states.default)
                        else:
                            self.maju()
                            kedalamanMultiComment-=1
                    elif(self.currentChar=="\n"):
                        self.gantiBaris()
                        self.maju()
                    else:
                        if(self.pointerIterator>=len(self.fileOriginal)-1 and kedalamanMultiComment>0):
                            self.errorhandlerObjek.tambahinError(__name__, 3, self.commentStart[0], self.commentStart[1], self.temp)
                        self.maju()
                else:
                    self.maju()
                    self.gantiState(states.default)
                
            elif(self.state==states.punctuatorBracket):
                if(self.currentChar in grammar.kurungList.keys() or self.currentChar in grammar.punctuationList.keys()):
                    self.konversiTempJikaBerisi()
                    self.simpenCharKeTemp()
                    self.konversiDanPushKeToken()
                    self.maju()
                else:
                    self.gantiState(states.default)
        else:
            self.konversiTempJikaBerisi()