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
from metadata.datatypeClass import TIPEDATA_EROR
# from typing import Any
import json

fungsi_builtin : list[fungsiObjek] = [fungsiObjek("tampilin", TIPEDATA_VOID, [varibelObjek(False,"p_inputCout", TIPEDATA_ANY)], node.nodeClass(-1, -1))]

class semantikClass:
    def __init__(self, p_errorHandlerRef : errorHandlerClass) -> None:
        self.errorHandlerObjek = p_errorHandlerRef
        self.scopes : list[scopeContainer] = []
    
    # def cekGetVariabel

    def cekScope(self, p_node: node.nodeClass, p_scope: scopeContainer)->None:
        match p_node:
            case node.nodeBikinFungsi():
                newScope : scopeContainer = scopeContainer()
                newScope.scopeParent=p_scope
                returnValueTipedata : datatypes = TIPEDATA_VOID
                fungsiTipedata : datatypes = TIPEDATA_VOID
                
                self.scopes.append(newScope)
                
                #ngeinsert tipedata fungsi
                if(p_node.tipedataFungsi!=TIPEDATA_VOID):
                    fungsiTipedata = p_node.tipedataFungsi
                
                #nambahin data parameter
                for param in p_node.parameterFungsi:
                    newVrblObj : varibelObjek = varibelObjek(False, param.nama, param.tipedata)
                    newScope.mappingVariabel.setdefault(param.nama, newVrblObj)
                
                #scanning isi fungsi
                for nodeKode in p_node.isiFungsi:
                    
                    #ngecek returnan dri fungsi
                    if(isinstance(nodeKode, node.nodeBalikin)):
                        
                        #ngecek biar fungsi void gak ngereturn apapun
                        if(fungsiTipedata!=TIPEDATA_VOID):
                            if(nodeKode.returnEkspresi.tipe==TIPEDATA_NULL):
                                if(isinstance(nodeKode.returnEkspresi, node.nodeIdentifier)):
                                    # print("idtf",nodeKode.returnEkspresi.identifierToken)
                                    if(newScope.cekVariabel(nodeKode.returnEkspresi.identifierToken)):
                                        # print("variabelnya ada")
                                        returnValueTipedata = newScope.getVariabel(nodeKode.returnEkspresi.identifierToken).type

                                    else:
                                        # print("variabelnya gaada")
                                        self.errorHandlerObjek.tambahinError(__name__, 1, nodeKode.baris, nodeKode.kolom, nodeKode.returnEkspresi.identifierToken)
                                        pass
                                        
                                    # print(nodeKode.returnEkspresi.identifierToken)
                            else:
                                returnValueTipedata = nodeKode.returnEkspresi.tipe
                        else:
                            # print("VOID HRUSNYA GK NGERETURN APAPUN")
                            self.errorHandlerObjek.tambahinError(__name__, 16, nodeKode.baris, nodeKode.kolom, p_node.namaFungsi)
                    else:
                        self.cekScope(nodeKode, newScope)
                
                if(fungsiTipedata!=TIPEDATA_VOID):
                    if(returnValueTipedata==TIPEDATA_VOID):
                        # print("FUNGSINYA GA NGERETURN APAPUN")
                        self.errorHandlerObjek.tambahinError(__name__, 17, p_node.baris, p_node.kolom, p_node.namaFungsi)
                    else:
                        if(fungsiTipedata!=returnValueTipedata):
                            # print("RETURNNYA GA SESUAI SMA TIPEDATA FUNGSINYA")
                            self.errorHandlerObjek.tambahinError(__name__, 18, p_node.baris, p_node.kolom, p_node.namaFungsi)
                        
            
            case node.nodeBikinVariabel():
                if(p_scope.cekVariabel(p_node.namaVariabel)):
                    self.errorHandlerObjek.tambahinError(__name__, 14, p_node.baris, p_bagian=p_node.namaVariabel)
                    
                else:
                    newVariabelObj : varibelObjek
                    
                    tipedataValue : datatypes | None = None
                    tipedataVariabel : datatypes = TIPEDATA_VOID
                    
                    if(p_node.nilaiVariabel.tipe!=TIPEDATA_NULL):
                        newVariabelObj = varibelObjek(True, p_node.namaVariabel, p_node.tipedataVariabel, p_node.baris)
                    else:
                        newVariabelObj = varibelObjek(False, p_node.namaVariabel, p_node.tipedataVariabel, p_node.baris)

                    if(p_node.tipedataVariabel==TIPEDATA_EROR):
                        newVariabelObj.invalid = True
                        self.errorHandlerObjek.tambahinError(__name__, 13, p_node.baris, p_bagian=p_node.namaVariabel)
                    else:
                        tipedataVariabel = p_node.tipedataVariabel
                        
                    if(isinstance(p_node.nilaiVariabel, node.nodeIdentifier)):
                        
                        #ngecek apkh variabelnya ada discope
                        if(p_scope.cekVariabel(p_node.nilaiVariabel.identifierToken)):
                            
                            getVariabel : varibelObjek = p_scope.getVariabel(p_node.nilaiVariabel.identifierToken)
                            tipedataValue = getVariabel.type
                            
                        else:
                            newVariabelObj.invalid = True
                            self.errorHandlerObjek.tambahinErrorMultibaris(p_kelas= __name__, p_kodeError=1, p_baris=p_node.nilaiVariabel.baris, p_bagian=p_node.nilaiVariabel.identifierToken)
                        
                    elif(type(p_node.nilaiVariabel) in [node.nodeNomor, node.nodeString, node.nodeBoolean]):
                        nilaiVar : node.nodeNomor | node.nodeString | node.nodeBoolean = p_node.nilaiVariabel
                        tipedataValue = nilaiVar.tipe
                        
                    if(not tipedataValue is None):
                        if(tipedataVariabel!=tipedataValue):
                            self.errorHandlerObjek.tambahinError(__name__, 2, p_node.baris, p_bagian=p_node.namaVariabel)
                        p_scope.mappingVariabel.setdefault(p_node.namaVariabel, newVariabelObj)

            case node.nodeBalikin():
                self.cekScope(p_node.returnEkspresi, p_scope)
                pass
            
            case node.nodeBiner():
                
                kiriTipe : datatypes | None = None
                kananTipe : datatypes | None = None
                
                kiriNilai : str | None = None
                kananNilai : str | None = None
                
                if(isinstance(p_node.operand1, node.nodeIdentifier)):
                    if(p_scope.cekVariabel(p_node.operand1.identifierToken)):
                        kiriTipe = p_scope.getVariabel(p_node.operand1.identifierToken).type
                        kiriNilai = p_scope.getVariabel(p_node.operand1.identifierToken).nama
                    else:
                        self.errorHandlerObjek.tambahinError(__name__, 1, p_node.baris, -1, p_node.operand1.identifierToken)
                else:
                    kiriTipe = p_node.operand1.tipe
                    kiriNilai = p_node.operand1.getDatas().get("nilai")
                    # print(p_node.operand1.getDatas())
                    
                if(isinstance(p_node.operand2, node.nodeIdentifier)):
                    if(p_scope.cekVariabel(p_node.operand2.identifierToken)):
                        kananTipe = p_scope.getVariabel(p_node.operand2.identifierToken).type
                        kananNilai = p_scope.getVariabel(p_node.operand2.identifierToken).nama
                    else:
                        self.errorHandlerObjek.tambahinError(__name__, 1, p_node.baris, -1, p_node.operand2.identifierToken)
                else:
                    kananTipe = p_node.operand2.tipe
                    kananNilai = p_node.operand2.getDatas().get("nilai")

                if(not kiriTipe is None and not kananTipe is None):
                    if(kiriTipe!=kananTipe):
                        self.errorHandlerObjek.tambahinError(__name__, 3, p_node.baris, -1, f"{kiriNilai}{p_node.operator}{kananNilai}")

            case node.nodePanggilFungsi():
                if(p_scope.cekFungsi(p_node.namaFungsi.nilai)):
                    getFungsi : fungsiObjek = p_scope.getFungsi(p_node.namaFungsi.nilai)
                    
                    tipedataParameterInput : datatypes | None = None
                    tipedataParameterFungsi : datatypes | None = None
                    
                    #mastiin klo input paramnya sesuai
                    if(len(p_node.parameterInput)<=len(getFungsi.parameters)):
                        for paramIndeks in range(0,len(getFungsi.parameters)):
                            tipedataParameterFungsi = getFungsi.parameters[paramIndeks].type
                            paramSkrg : node.nodeEkspresi | None = None
                            if(paramIndeks<len(p_node.parameterInput)):
                                paramSkrg = p_node.parameterInput[paramIndeks]
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
                                    self.cekScope(paramSkrg, p_scope)
                                    # raise Exception(f"ada input yg ga diinginkan : {paramSkrg}")
                            else:
                                #kondisi parameter opsional yg blm diisi
                                if(getFungsi.parameters[paramIndeks].bernilai):
                                    #ada kekosongan input di parameter opsional
                                    pass
                                else:
                                    #ada kekosongan input di parameter wajib
                                    self.errorHandlerObjek.tambahinError(__name__, 9, p_node.baris, p_node.kolom, p_bagian=p_node.namaFungsi.nilai)

                            if(paramIndeks<len(p_node.parameterInput)):
                                if(not tipedataParameterFungsi is None and not tipedataParameterInput is None):
                                    if(tipedataParameterInput!=tipedataParameterFungsi and not (tipedataParameterInput==TIPEDATA_ANY or tipedataParameterFungsi==TIPEDATA_ANY)):
                                        if(tipedataParameterInput==TIPEDATA_VOID):
                                            self.errorHandlerObjek.tambahinError(__name__, 12, p_node.baris, -1, paramSkrg.namaFungsi.nilai)
                                        else:
                                            if(isinstance(paramSkrg, node.nodeIdentifier)):
                                                self.errorHandlerObjek.tambahinError(__name__, 5, p_node.baris, -1, f"{p_node.namaFungsi.nilai}({getFungsi.parameters[paramIndeks].nama} = {paramSkrg.identifierToken})")

                                            elif(type(paramSkrg) in [node.nodeString, node.nodeNomor, node.nodeBoolean]):
                                                self.errorHandlerObjek.tambahinError(__name__, 10, p_node.baris, -1, f"{p_node.namaFungsi.nilai}({getFungsi.parameters[paramIndeks].nama} = '{paramSkrg.nilai}')")
                                                
                                            elif(isinstance(paramSkrg, node.nodePanggilFungsi)):
                                                self.errorHandlerObjek.tambahinError(__name__, 11, p_node.baris, -1, f"{p_node.namaFungsi.nilai}({getFungsi.parameters[paramIndeks].nama} = '{paramSkrg.namaFungsi.nilai}')")
                                                
                                            
                                    else:
                                        
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
        if(p_rootScope.cekFungsi(p_node.namaFungsi)):
            self.errorHandlerObjek.tambahinError(__name__, 14, p_node.baris, p_bagian=p_node.namaFungsi)
        else:
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