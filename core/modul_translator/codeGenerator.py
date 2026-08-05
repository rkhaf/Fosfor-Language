from __future__ import annotations
from llvmlite import ir
from typing import Optional, Union
from typing import cast
from errorHandler import errorHandlerClass
from modul_parsing.AST import ASTClass
from pohon import node
from llvmFolder.konverter import LLVMLITEConverterClass as konvertClass
from metadata.datatypeClass import TIPEDATA_BOOLEAN
from metadata.datatypeClass import TIPEDATA_INTEGER
from metadata.datatypeClass import TIPEDATA_STRING
from metadata.datatypeClass import TIPEDATA_FLOAT
from metadata.datatypeClass import TIPEDATA_NULL

class scopeClass:
    def __init__(self, p_parent : scopeClass | None = None) -> None:
        self.scopeParent : scopeClass | None = p_parent
        self.mappingVariabel : dict[str, ir.AllocaInstr] = {}
    
    def addVariabel(self, p_nama : str, p_ptr : ir.AllocaInstr)->None:
        self.mappingVariabel[p_nama] = p_ptr
    
    def cekVariabel(self, p_nama:str)->bool:
        if(self.scopeParent is None):
            return p_nama in self.mappingVariabel.keys()
        else:
            percobaanCari : bool = p_nama in self.mappingVariabel.keys()
            if(percobaanCari):
                return True
            else:
                return self.scopeParent.cekVariabel(p_nama)

    def getVariabel(self, p_nama : str)->ir.AllocaInstr:
        if(self.cekVariabel(p_nama)):
            if(self.scopeParent is None):
                getter : ir.AllocaInstr | None = self.mappingVariabel.get(p_nama, None)
                if(not getter is None):
                    return getter
                else:raise Exception("gk ketemu")
            
            else:
                percobaanCari : bool = p_nama in self.mappingVariabel.keys()
                if(percobaanCari):
                    getter : ir.AllocaInstr | None = self.mappingVariabel.get(p_nama, None)
                    if(not getter is None):
                        return getter
                    else:raise Exception("gk ketemu")
                else:
                    return self.scopeParent.getVariabel(p_nama)
        else:
            raise Exception("ERROR")

class codeGeneratorClass:
    def __init__(self, p_errorHandlerRef : errorHandlerClass) -> None:
        self.modul : ir.Module = ir.Module(name="FOSFOR CODEGEN")
        self.simbolTable : scopeClass = scopeClass()
        self.errorHandlerObjek = p_errorHandlerRef
        self.rootScope : scopeClass = scopeClass()
        self.builder : ir.IRBuilder | None = None
        pass
    
    def visit(self, p_node : node.nodeClass, p_scope : scopeClass)->ir.Value | None:
        match p_node:
            case node.nodeBikinVariabel():
                self.bacaVariabel(p_node, p_scope)
            
            case node.nodeBikinFungsi():
                self.bacaFungsi(p_node)
                    
            case _:
                pass
        pass
    
    def bacaVariabel(self, p_nodeBikinVariabel : node.nodeBikinVariabel, p_scope : scopeClass)->None:
        if(not self.builder is None):
            # if(p_nodeBikinVariabel.tipedataVariabel in [TIPEDATA_BOOLEAN, TIPEDATA_FLOAT, TIPEDATA_INTEGER, TIPEDATA_STRING])
            konversiTipedataVariabel : ir.Type = konvertClass.konversiTipedata(p_nodeBikinVariabel.tipedataVariabel)
            llvm_varRef = cast(ir.AllocaInstr, self.builder.alloca(konversiTipedataVariabel, name=p_nodeBikinVariabel.namaVariabel))
            # if(type(p_nodeBikinVariabel.nilaiVariabel) in [node.nodeNomor, node.nodeString, node.nodeBoolean]):
            if(isinstance(p_nodeBikinVariabel.nilaiVariabel, node.nodeNomor)):
                if(p_nodeBikinVariabel.tipedataVariabel==TIPEDATA_INTEGER):
                    self.builder.store(ir.Constant(konversiTipedataVariabel, int(p_nodeBikinVariabel.nilaiVariabel.nilai)), llvm_varRef)
                else:
                    self.builder.store(ir.Constant(konversiTipedataVariabel, float(p_nodeBikinVariabel.nilaiVariabel.nilai)), llvm_varRef)
            else:raise Exception("TIPEDATA BLM DISUPPORT")
            # print("nilai variabel: ",p_nodeBikinVariabel.nilaiVariabel)
            p_scope.addVariabel(p_nodeBikinVariabel.namaVariabel, llvm_varRef)
        pass
    
    def bacaFungsi(self, p_nodeBikinFungsi : node.nodeBikinFungsi)->None:
        if(p_nodeBikinFungsi.namaFungsi=="main"):
            newScope : scopeClass = scopeClass(self.rootScope)
            
            llvm_tipeFungsi : ir.FunctionType = ir.FunctionType(ir.IntType(32), [])
            llvm_fungsiBaru : ir.Function = ir.Function(self.modul, llvm_tipeFungsi, p_nodeBikinFungsi.namaFungsi)
            
            llvm_entryBlock : ir.Block = llvm_fungsiBaru.append_basic_block(name="entry")
            
            self.builder = ir.IRBuilder(llvm_entryBlock)
            
            zeroExitCode : ir.Constant = ir.Constant(ir.IntType(32), 0)
            # a = ir.Constant(ir.IntType(32), 6)
            # b = ir.Constant(ir.IntType(32), 7)
            # hasil = cast(ir.Value, self.builder.add(a, b, name="hasilTambah"))
            
            for nodeKode in p_nodeBikinFungsi.isiFungsi:
                self.visit(nodeKode, newScope)
                pass
            # pass
            self.builder.ret(zeroExitCode)
                
    # def bacaFungsi(self, p_nodeBikinFungsi : node.nodeBikinFungsi)->None:
    #     if(p_nodeBikinFungsi.namaFungsi=="main"):
    #         # llvm_tipedataFungsi : ir.Type = konvertClass.konversiTipedata(p_nodeBikinFungsi.tipedataFungsi)
    #         # llvm_parameterFungsi : list[ir.Type] = []
    #         # llvm_tipeFungsi : ir.FunctionType = ir.FunctionType(llvm_tipedataFungsi, llvm_parameterFungsi)
    #         # llvm_fungsiBaru : ir.Function = ir.Function(self.modul, llvm_tipeFungsi, p_nodeBikinFungsi.namaFungsi)
            
    #         llvm_tipeFungsi : ir.FunctionType = ir.FunctionType(ir.IntType(32), [])
    #         llvm_fungsiBaru : ir.Function = ir.Function(self.modul, llvm_tipeFungsi, p_nodeBikinFungsi.namaFungsi)
            
    #         # #ngeappend parameter ke fungsi
    #         # for paramFungsi in p_nodeBikinFungsi.parameterFungsi:
    #         #     llvm_parameterFungsi.append(konvertClass.konversiTipedata(paramFungsi.tipedata))
            
    #         # #ngasi nama ke param fungsi llvm
    #         # for indeks in range(0, len(p_nodeBikinFungsi.parameterFungsi)):
    #         #     llvm_fungsiBaru.args[indeks].name = p_nodeBikinFungsi.parameterFungsi[indeks].nama
            
    #         llvm_entryBlock : ir.Block = ir.Block(llvm_fungsiBaru.append_basic_block(name="entry"))
            
    #         llvm_builder : ir.IRBuilder = ir.IRBuilder(llvm_entryBlock)
            
    #         zeroExitCode : ir.Constant = ir.Constant(ir.IntType(32), 0)
    #         llvm_builder.ret(zeroExitCode)
            
    #         for nodeKode in p_nodeBikinFungsi.isiFungsi:
    #             self.bacaApapun(nodeKode)
    #             pass
    #         # pass
    
    def proses(self, p_astReferensi : ASTClass)->None:
        nodeList : list[node.nodeClass] = p_astReferensi.getTree()
        for fungsiNode in nodeList:
            if(isinstance(fungsiNode, node.nodeBikinFungsi)):
                self.bacaFungsi(fungsiNode)
            else:
                raise Exception("ADA CODE DILUAR SCOPE")
        print("FINAL:\n",str(self.modul))