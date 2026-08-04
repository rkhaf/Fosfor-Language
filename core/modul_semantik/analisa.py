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
from metadata.datatypeClass import TIPEDATA_NULL
from metadata.datatypeClass import TIPEDATA_ANY
# from typing import Any
import json

fungsi_builtin : list[fungsiObjek] = [fungsiObjek("tampilin", TIPEDATA_VOID, [varibelObjek(False,"p_inputCout", TIPEDATA_ANY)], node.nodeClass(-1, -1))]

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
                    newVrblObj : varibelObjek = varibelObjek(False, param.nama, param.tipedata)
                    newScope.mappingVariabel.setdefault(param.nama, newVrblObj)
                
                for nodeKode in p_node.isiFungsi:
                    self.cekScope(nodeKode, newScope)
            
            case node.nodeBikinVariabel():
                # print(p_node.namaVariabel,p_node.nilaiVariabel, p_node.nilaiVariabel.tipe)
                newVariabelObj : varibelObjek
                if(p_node.nilaiVariabel.tipe!=TIPEDATA_NULL):
                    newVariabelObj = varibelObjek(True, p_node.namaVariabel, p_node.tipedataVariabel, p_node.baris)
                else:
                    newVariabelObj = varibelObjek(False, p_node.namaVariabel, p_node.tipedataVariabel, p_node.baris)
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
                    
                    tipedataParameterInput : datatypes | None = None
                    tipedataParameterFungsi : datatypes | None = None
                    
                    #mastiin klo input paramnya sesuai
                    if(len(p_node.parameterInput)<=len(getFungsi.parameters)):
                        for paramIndeks in range(0,len(getFungsi.parameters)):
                            tipedataParameterFungsi = getFungsi.parameters[paramIndeks].type
                            
                            if(paramIndeks<len(p_node.parameterInput)):
                                paramSkrg : node.nodeEkspresi = p_node.parameterInput[paramIndeks]
                                # print("paramSkrg:",paramSkrg.getDatas())
                                if(isinstance(paramSkrg, node.nodeIdentifier)):
                                    #ketemu parameter variabel
                                    if(p_scope.cekVariabel(paramSkrg.identifierToken)):
                                        #ketemu variabelnya
                                        tipedataParameterInput = p_scope.getVariabel(paramSkrg.identifierToken).type
                                        
                                    else:
                                        # print("GK KETEMU VARIABELNYA")
                                        self.errorHandlerObjek.tambahinError(__name__, 1, paramSkrg.baris, paramSkrg.kolom, paramSkrg.identifierToken)
                                
                                elif(type(paramSkrg) in [node.nodeString, node.nodeNomor, node.nodeBoolean]):
                                    #ketemu parameter primitive
                                    tipedataParameterInput = paramSkrg.tipe
                                
                                elif(isinstance(paramSkrg, node.nodePanggilFungsi)):
                                    # self.cekScope(paramSkrg, p_scope)
                                    # continue
                                    #ketemu panggilan fungsi
                                    if(p_scope.cekFungsi(paramSkrg.namaFungsi.nilai)):
                                        tipedataParameterInput = p_scope.getFungsi(paramSkrg.namaFungsi.nilai).type
                                        self.cekScope(paramSkrg, p_scope)
                                    else:
                                        self.errorHandlerObjek.tambahinError(__name__, 6, paramSkrg.baris, paramSkrg.kolom, paramSkrg.namaFungsi.nilai)
                                        # print("FUNGSI GA NEMU")
                                    pass
                                else:
                                    #ketemu parameter node lain
                                    raise Exception(f"ada input yg ga diinginkan : {paramSkrg}")
                            else:
                                #kondisi parameter opsional yg blm diisi
                                if(getFungsi.parameters[paramIndeks].bernilai):
                                    #ada kekosongan input di parameter opsional
                                    pass
                                else:
                                    #ada kekosongan input di parameter wajib
                                    self.errorHandlerObjek.tambahinError(__name__, 9, p_node.baris, p_node.kolom, p_bagian=p_node.namaFungsi.nilai)

                            # print(tipedataParameterFungsi, "==", tipedataParameterInput)
                            if(paramIndeks<len(p_node.parameterInput)):
                                if(not tipedataParameterFungsi is None and not tipedataParameterInput is None):
                                    # print(tipedataParameterFungsi,"=",tipedataParameterInput)
                                    # print(getFungsi.parameters[paramIndeks].nama,"=",p_node.parameterInput[paramIndeks].getDatas())
                                    # print(getFungsi.parameters[paramIndeks].nama, ":", tipedataParameterFungsi, "=", p_node.parameterInput[paramIndeks].getDatas(), ":", tipedataParameterInput)
                                    if(tipedataParameterInput!=tipedataParameterFungsi and not (tipedataParameterInput==TIPEDATA_ANY or tipedataParameterFungsi==TIPEDATA_ANY)):
                                        # print("GK SAMA",tipedataParameterFungsi,tipedataParameterInput)
                                        if(tipedataParameterInput==TIPEDATA_VOID):
                                            self.errorHandlerObjek.tambahinError(__name__, 12, p_node.baris, -1, paramSkrg.namaFungsi.nilai)
                                        else:
                                            if(isinstance(paramSkrg, node.nodeIdentifier)):
                                                self.errorHandlerObjek.tambahinError(__name__, 5, p_node.baris, -1, f"{p_node.namaFungsi.nilai}({getFungsi.parameters[paramIndeks].nama} = {paramSkrg.identifierToken})")
                                                # self.errorHandlerObjek.tambahinError(__name__, 5, p_node.baris, -1, str(p_node.namaFungsi.nilai+"."+getFungsi.parameters[paramIndeks].nama)+" = "+str(paramSkrg.identifierToken))
                                            elif(type(paramSkrg) in [node.nodeString, node.nodeNomor, node.nodeBoolean]):
                                                self.errorHandlerObjek.tambahinError(__name__, 10, p_node.baris, -1, f"{p_node.namaFungsi.nilai}({getFungsi.parameters[paramIndeks].nama} = '{paramSkrg.nilai}')")
                                                
                                            elif(isinstance(paramSkrg, node.nodePanggilFungsi)):
                                                self.errorHandlerObjek.tambahinError(__name__, 11, p_node.baris, -1, f"{p_node.namaFungsi.nilai}({getFungsi.parameters[paramIndeks].nama} = '{paramSkrg.namaFungsi.nilai}')")
                                                
                                            # print("gk sama =",getFungsi.nama,":",getFungsi.parameters[paramIndeks].nama, ":", tipedataParameterFungsi, "=", p_node.parameterInput[paramIndeks].getDatas(), ":", tipedataParameterInput)
                                    else:
                                        # print("sama =",getFungsi.nama,":",getFungsi.parameters[paramIndeks].nama, ":", tipedataParameterFungsi, "=", p_node.parameterInput[paramIndeks].getDatas(), ":", tipedataParameterInput)
                                        pass
                                
                    else:
                        print("DEBUG3")
                        self.errorHandlerObjek.tambahinError(__name__, 4, p_node.baris, -1, p_node.namaFungsi.nilai)
                else:
                    print("DEBUG4")
                    # print(p_node.namaFungsi,"gaada")
                    self.errorHandlerObjek.tambahinError(__name__, 6, p_node.baris, -1, p_node.namaFungsi.nilai)
                    
                
            case _:
                pass
        pass

    def registerFungsi(self, p_node : node.nodeBikinFungsi, p_rootScope: scopeContainer)->None:
        listParams : list[varibelObjek] = []
        bagianParameterWajib : bool = True
        for params in p_node.parameterFungsi:
            newVariabelObj : varibelObjek
            if(params.nilaiDefault is None):
                newVariabelObj = varibelObjek(False, params.nama, params.tipedata)
                if(not bagianParameterWajib):
                    # print("INVALID",params.nama)
                    newVariabelObj.invalid = True
                    self.errorHandlerObjek.tambahinError(__name__, 8, params.baris, p_bagian=params.nama)
                else:
                    bagianParameterWajib=True
                listParams.append(newVariabelObj)

            else:
                # if(bagianParameterWajib)
                bagianParameterWajib=False
                if(type(params.nilaiDefault) in [node.nodeString, node.nodeNomor, node.nodeBoolean]):
                    if(params.tipedata==params.nilaiDefault.tipe):
                        # print(params.nama,params.tipedata,params.nilaiDefault.tipe)
                        newVariabelObj : varibelObjek = varibelObjek(True, params.nama, params.tipedata)
                        listParams.append(newVariabelObj)
                    else:
                        self.errorHandlerObjek.tambahinError(__name__, 2, params.baris, p_bagian=params.nama)
                        
                else:
                    self.errorHandlerObjek.tambahinError(__name__, 7, params.baris, p_bagian=params.nama)

                
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