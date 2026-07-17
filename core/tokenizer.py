from keywords import keywordList
from keywords import primitiveList
from dataFormat import Token
# from keywords import primitiveList
import tataBahasa

class tokenizerClass:
    def __init__(self):
        # self.leksem : list[str] = []
        # self.tokens : list[str] = []
        pass
    
    # def proses(self, p_tokens : list[str]) -> str | None:
    #     self.leksem = p_tokens
        
    #     for token in self.leksem:
    #         if (token in keywordList):
    #             self.tokens.append(keywordList.get(token, tataBahasa.KEYWORD_SYS_GTWW))
    #         elif (token in primitiveList):
    #             self.tokens.append(primitiveList.get(token, tataBahasa.KEYWORD_SYS_GTWW))
    #         else:
    #             if(token.isdigit()):
    #                 self.tokens.append(tataBahasa.TIPEDATA_INT+":"+token)
    #             else:
    #                 self.tokens.append(tataBahasa.KEYWORD_SYS_LTRL+":"+token)
                    
    # def getTokens(self) -> list[str]:
    #     return self.tokens
    
    def getToken(self, p_leksem : str, p_datatype : str = "")->Token:
        if(len(p_datatype)==0):
            # print("[TOKENIZER1]")
            if(p_leksem in keywordList.keys()):
                return Token(tataBahasa.KEYWORD_SYS_KYWR,keywordList.get(p_leksem, "ERR"))
            
            elif(p_leksem in primitiveList.keys()):
                return Token(tataBahasa.KEYWORD_SYS_KYWR,primitiveList.get(p_leksem, "ERR"))
                # return keywordList.get(p_leksem, "ERR")
            
            # elif(p_leksem in primitiveList.keys()):
            #     temp : str = primitiveList.get(p_leksem, tataBahasa.SYS_ERR)
            #     if(temp!=tataBahasa.SYS_ERR):
            #         return Token(temp, p_leksem)
            #         # return [temp, p_leksem]
                
            #     else:
            #         return Token(tataBahasa.KEYWORD_SYS_LTRL, p_leksem)
            #         # return [tataBahasa.KEYWORD_SYS_LTRL, p_leksem]
            
            else:
                return Token(tataBahasa.KEYWORD_SYS_LTRL, p_leksem)
                # return [tataBahasa.KEYWORD_SYS_LTRL, p_leksem]
            pass
        else:
            # print("[TOKENIZER2]")
            if(p_datatype in primitiveList.keys()):
                return Token(primitiveList.get(p_datatype, tataBahasa.SYS_ERR), p_leksem)
            else:
                return Token("ERROR", "ERROR")
            pass