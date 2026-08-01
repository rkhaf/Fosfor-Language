from errorHandler import errorHandlerClass
from modul_parsing.AST import ASTClass
from pohon.node import nodeBikinFungsi
from pohon.node import nodeClass
from modul_semantik.simbolTableManager import scopeContainer
from modul_semantik.simbolTableManager import varibelObjek
from modul_semantik.simbolTableManager import fungsiObjek
from metadata.datatypeClass import datatypes
from metadata.datatypeClass import TIPEDATA_NULL
import json

class semantikClass:
    def __init__(self, p_errorHandlerRef : errorHandlerClass) -> None:
        self.errorHandlerObjek = p_errorHandlerRef
        self.scopes : list[scopeContainer] = []
        pass

    def proses(self, p_tree : ASTClass)->None:
        counterMainLoop : int = 0
        counterFungsi : int = 0
        
        rootScope : scopeContainer = scopeContainer()
        self.scopes.append(rootScope)
        
        getTree : list[nodeClass] = p_tree.getTree()
        totalNode : int = len(getTree)
        while counterMainLoop<2:
            
            match counterMainLoop:
                #loop pertama buat ngeregister fungsi
                case 0:
                    while counterFungsi<totalNode:
                        getNode = getTree[counterFungsi]
                        getAttr = getattr(getNode, "registerFungsi")()
                        
                        tempNamaFungsi : str = ""
                        tempTipeReturnFungsi : datatypes = TIPEDATA_NULL
                        tempParameterFungsi : list[varibelObjek] = []
                        
                        for key, val in getAttr.items():
                            match key:
                                case "nama":
                                    tempNamaFungsi = val
                                
                                case "tipeReturn":
                                    tempTipeReturnFungsi = val
                                
                                case "parameter":
                                    if(len(val)>0):
                                        tempNamaParam : str = ""
                                        tempTipeParam : datatypes = TIPEDATA_NULL
                                        for indeks in range(0,len(val)):
                                            pass
                                            for keyParam, valParam in val[indeks].items():
                                                if(keyParam=="nama"):
                                                    tempNamaParam = valParam
                                                    
                                                elif(keyParam=="tipeParam"):
                                                    tempTipeParam = valParam
                                                
                                            tempVariabelObjek : varibelObjek = varibelObjek(tempNamaParam, tempTipeParam)
                                            tempParameterFungsi.append(tempVariabelObjek)
                                        # rootScope.mappingVariabel.setdefault(tempNamaParam, tempVariabelObjek)
                                        pass
                                case _:
                                    pass
                                    
                            
                        newFungsiObjek : fungsiObjek = fungsiObjek(tempNamaFungsi, tempTipeReturnFungsi, tempParameterFungsi, getNode)
                        rootScope.mappingFungsi.setdefault(tempNamaFungsi, newFungsiObjek)
                        
                        counterFungsi+=1
                    counterFungsi=0
                    
                case 1:
                    while counterFungsi<totalNode:
                        # print(getTree[counterFungsi])
                        newScope : scopeContainer = scopeContainer()
                        newScope.scopeParent = rootScope
                        
                        getAttr = getattr(getTree[counterFungsi], "evaluasi")()
                        
                        
                        
                        self.scopes.append(newScope)
                        counterFungsi+=1
                    counterFungsi=0
                    pass
                
                case _:
                    pass
                
            counterMainLoop+=1
        for scope in self.scopes:
            # scope.printDatas()
            print(json.dumps(scope.printDatas(), indent=2))
            # print(json.dumps(json.dumps(scope.printDatas())))
        pass