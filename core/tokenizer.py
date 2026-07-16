from keywords import keywordList
from keywords import primitiveList
from keywords import primitiveList
import tataBahasa

class tokenizerClass:
    def __init__(self):
        self.leksem : list[str] = []
        self.tokens : list[str] = []
        pass
    
    def proses(self, p_tokens : list[str]) -> None:
        self.leksem = p_tokens
        
        for token in self.leksem:
            if (token in keywordList):
                self.tokens.append(keywordList.get(token, tataBahasa.KEYWORD_SYS_GTWW))
            elif (token in primitiveList):
                self.tokens.append(primitiveList.get(token, tataBahasa.KEYWORD_SYS_GTWW))
            else:
                if(token.isdigit()):
                    self.tokens.append(tataBahasa.TIPEDATA_INT+":"+token)
                else:
                    self.tokens.append(tataBahasa.KEYWORD_SYS_LTRL+":"+token)
    def getTokens(self) -> list[str]:
        return self.tokens