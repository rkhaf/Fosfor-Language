from errorHandler import errorHandlerClass
from modul_parsing.AST import ASTClass
# from pohon.node import nodeBikinFungsi
# from pohon.node import node.nodeClass
from pohon import node
from modul_semantik.simbolTableManager import scopeContainer
from modul_semantik.simbolTableManager import varibelObjek
from modul_semantik.simbolTableManager import fungsiObjek
from metadata.datatypeClass import datatypes
from metadata.datatypeClass import TIPEDATA_VOID
from metadata.datatypeClass import TIPEDATA_ANY
# from typing import Any
import json

fungsi_builtin : list[fungsiObjek] = [fungsiObjek("tampilin", TIPEDATA_VOID, [varibelObjek("p_inputCout", TIPEDATA_ANY)], node.nodeClass(-1, -1))]

class semantikClass:
    def __init__(self, p_errorHandlerRef : errorHandlerClass) -> None:
        self.errorHandlerObjek = p_errorHandlerRef
        self.scopes : list[scopeContainer] = []

    def cekScope(self, p_node: node.nodeClass, p_scope: scopeContainer)->None:
        match p_node:
            case node.nodeBikinFungsi():
                newScope : scopeContainer = scopeContainer()
                newScope.scopeParent=p_scope
                
                self.scopes.append(newScope)
                
                for param in p_node.parameterFungsi:
                    newVrblObj : varibelObjek = varibelObjek(param.nama, param.tipedata)
                    newScope.mappingVariabel.setdefault(param.nama, newVrblObj)
                
                for nodeKode in p_node.isiFungsi:
                    self.cekScope(nodeKode, newScope)
            
            case node.nodeBikinVariabel():
                newVariabelObj : varibelObjek = varibelObjek(p_node.namaVariabel, p_node.tipedataVariabel, p_node.baris)
                if(isinstance(p_node.nilaiVariabel, node.nodeIdentifier)):
                    
                    #ngecek apkh variabelnya ada discope
                    if(p_scope.cekVariabel(p_node.nilaiVariabel.identifierToken)):
                        
                        #yg ini buat ngecek tipedatanya
                        if(p_scope.getVariabel(p_node.nilaiVariabel.identifierToken).type != p_node.tipedataVariabel):
                            newVariabelObj.invalid=True
                            self.errorHandlerObjek.tambahinError(__name__, 2, p_node.baris, p_bagian=p_node.namaVariabel)

                    else:
                        newVariabelObj.invalid = True
                        self.errorHandlerObjek.tambahinErrorMultibaris(p_kelas= __name__, p_kodeError=1, p_baris=p_node.nilaiVariabel.baris, p_bagian=p_node.nilaiVariabel.identifierToken)

                p_scope.mappingVariabel.setdefault(p_node.namaVariabel, newVariabelObj)

            case node.nodeBalikin():
                self.cekScope(p_node.returnEkspresi, p_scope)
            
            case node.nodeBiner():
                
                kiriTipe : datatypes | None = None
                kananTipe : datatypes | None = None
                
                if(isinstance(p_node.operand1, node.nodeIdentifier)):
                    if(p_scope.cekVariabel(p_node.operand1.identifierToken)):
                        kiriTipe = p_scope.getVariabel(p_node.operand1.identifierToken).type
                        
                    else:
                        self.errorHandlerObjek.tambahinError(__name__, 1, p_node.baris, -1, p_node.operand1.identifierToken)
                else:
                    kiriTipe = p_node.operand1.tipe
                    
                if(isinstance(p_node.operand2, node.nodeIdentifier)):
                    if(p_scope.cekVariabel(p_node.operand2.identifierToken)):
                        kananTipe = p_scope.getVariabel(p_node.operand2.identifierToken).type
                    else:
                        self.errorHandlerObjek.tambahinError(__name__, 1, p_node.baris, -1, p_node.operand2.identifierToken)
                else:
                    kananTipe = p_node.operand2.tipe

                if(not kiriTipe is None and not kananTipe is None):
                    if(kiriTipe!=kananTipe):
                        self.errorHandlerObjek.tambahinError(__name__, 3, p_node.baris, -1, p_node.operator)

            case node.nodePanggilFungsi():
                if(p_scope.cekFungsi(p_node.namaFungsi.nilai)):
                    getFungsi : fungsiObjek = p_scope.getFungsi(p_node.namaFungsi.nilai)
                    
                    #mastiin klo input paramnya sesuai
                    if(len(p_node.parameterInput)<=len(getFungsi.parameters)):
                        for paramIndeks in range(0,len(p_node.parameterInput)):
                            tipeParam : datatypes = TIPEDATA_ANY
                            paramSkrg : node.nodeEkspresi = p_node.parameterInput[paramIndeks]
                            
                            if(isinstance(paramSkrg, node.nodeIdentifier)):
                                if(p_scope.cekVariabel(paramSkrg.identifierToken)):
                                    getVariabelDriScope : varibelObjek = p_scope.getVariabel(paramSkrg.identifierToken)
                                    # print("ada",getVariabelDriScope.type)
                                    tipeParam = getVariabelDriScope.type
                                else:
                                    print("gaada")
                            else:
                                tipeParam = p_node.parameterInput[paramIndeks].tipe
                                
                            if(tipeParam != getFungsi.parameters[paramIndeks].type):
                                if(type(paramSkrg) in [node.nodeString, node.nodeNomor]):
                                    self.errorHandlerObjek.tambahinError(__name__, 5, p_node.baris, -1, paramSkrg.nilai) #type: ignore

                                elif(isinstance(paramSkrg, node.nodeIdentifier)):
                                    self.errorHandlerObjek.tambahinError(__name__, 5, p_node.baris, -1, paramSkrg.identifierToken)
                                    
                    else:
                        self.errorHandlerObjek.tambahinError(__name__, 4, p_node.baris, -1, p_node.namaFungsi.nilai)
                else:
                    # print(p_node.namaFungsi,"gaada")
                    self.errorHandlerObjek.tambahinError(__name__, 1, p_node.baris, -1, p_node.namaFungsi.nilai)
                    
                
            case _:
                pass
        pass

    def registerFungsi(self, p_node : node.nodeBikinFungsi, p_rootScope: scopeContainer)->None:
        listParams : list[varibelObjek] = []
        for params in p_node.parameterFungsi:
            newVariabelObj : varibelObjek = varibelObjek(params.nama, params.tipedata)
            listParams.append(newVariabelObj)
        
        newFungsiObj : fungsiObjek = fungsiObjek(p_node.namaFungsi, p_node.tipedataFungsi, listParams, p_node)
        p_rootScope.mappingFungsi.setdefault(p_node.namaFungsi, newFungsiObj)
        pass

    def proses(self, p_tree : ASTClass)->None:
        counterMainLoop : int = 0
        counterFungsi : int = 0

        rootScope : scopeContainer = scopeContainer()
        self.scopes.append(rootScope)
        
        getTree : list[node.nodeClass] = p_tree.getTree()
        totalNode : int = len(getTree)
        
        #register fungsi builtin
        for fungsi in fungsi_builtin:
            rootScope.mappingFungsi.setdefault(fungsi.nama, fungsi)
        
        while counterMainLoop<2:
            
            match counterMainLoop:
                #loop pertama buat ngeregister fungsi
                case 0:
                    while counterFungsi<totalNode:
                        
                        getNode = getTree[counterFungsi]
                        if(isinstance(getNode, node.nodeBikinFungsi)):
                            self.registerFungsi(getNode, rootScope)

                        counterFungsi+=1
                    counterFungsi=0
                    
                case 1:
                    while counterFungsi<totalNode:
                        getNode = getTree[counterFungsi]
                #         # newScope : scopeContainer = scopeContainer()
                #         # newScope.scopeParent = rootScope
                        
                #         # getAttr = getattr(getNode, "evaluasi")()
                        
                        self.cekScope(getNode, rootScope)
                        
                #         # self.scopes.append(newScope)
                        counterFungsi+=1
                    counterFungsi=0
                    pass
                
                case _:
                    pass
                
            counterMainLoop+=1
        # for scope in self.scopes:
        #     print(json.dumps(scope.printDatas(), indent=2))
        #     pass
        pass