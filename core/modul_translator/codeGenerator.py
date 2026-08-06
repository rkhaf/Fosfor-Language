from __future__ import annotations
from llvmlite import ir
from typing import Optional, Union
from typing import cast
from typing import Any, Callable
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

fungsiBuiltin : dict[str, dict[str, list[ir.Type] | str | ir.Type]] = {
    "tampilin" : {
        "namaDiCPP" : "fosfor_tampilin_int",
        "parameter" : [ir.IntType(32)],
        "tipeReturn" : ir.VoidType()
    }
}

class codeGeneratorClass:
    def __init__(self, p_errorHandlerRef : errorHandlerClass) -> None:
        self.modul : ir.Module = ir.Module(name="FOSFOR CODEGEN")
        self.simbolTable : scopeClass = scopeClass()
        self.errorHandlerObjek = p_errorHandlerRef
        self.rootScope : scopeClass = scopeClass()
        self.builder : ir.IRBuilder | None = None
        self.fungsiExtern : dict[str, ir.Function] = {}
        pass
    
    def setupBuiltin(self, p_namaFungsi : str)->ir.Function:
        namaBuiltin : str = cast(str, fungsiBuiltin[p_namaFungsi]["namaDiCPP"])
        
        if(not p_namaFungsi in self.fungsiExtern.keys()):
            parameterBuiltin : list[ir.Type] = cast(list[ir.Type], fungsiBuiltin[p_namaFungsi]["parameter"])
            tipeReturnBuiltin : ir.Type = cast(ir.Type, fungsiBuiltin[p_namaFungsi]["tipeReturn"])
            
            llvm_tipeFungsi : ir.FunctionType = ir.FunctionType(tipeReturnBuiltin, parameterBuiltin)
            llvm_fungsi : ir.Function = ir.Function(self.modul, llvm_tipeFungsi, namaBuiltin)
            
            self.fungsiExtern[namaBuiltin] = llvm_fungsi
        
        return self.fungsiExtern[namaBuiltin]
    
    def visit(self, p_node : node.nodeClass, p_scope : scopeClass)->ir.Value | None:
        namaFungsi : str =f"baca_{type(p_node).__name__}"
        fungsiTujuan : Callable[[Any, Any], Any] = getattr(self, namaFungsi)
        return fungsiTujuan(p_node, p_scope)
    
    def baca_nodeBikinVariabel(self, p_nodeBikinVariabel : node.nodeBikinVariabel, p_scope : scopeClass)->None:
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
    
    def baca_nodeBikinFungsi(self, p_nodeBikinFungsi : node.nodeBikinFungsi, p_scope : scopeClass)->None:
        if(p_nodeBikinFungsi.namaFungsi=="main"):
            newScope : scopeClass = scopeClass(p_scope)
            
            llvm_tipeFungsi : ir.FunctionType = ir.FunctionType(ir.IntType(32), [])
            llvm_fungsiBaru : ir.Function = ir.Function(self.modul, llvm_tipeFungsi, p_nodeBikinFungsi.namaFungsi)
            
            llvm_entryBlock : ir.Block = llvm_fungsiBaru.append_basic_block(name="entry")
            
            self.builder = ir.IRBuilder(llvm_entryBlock)
            
            zeroExitCode : ir.Constant = ir.Constant(ir.IntType(32), 0)
            
            for nodeKode in p_nodeBikinFungsi.isiFungsi:
                self.visit(nodeKode, newScope)
                pass
            # pass
            self.builder.ret(zeroExitCode)

    def baca_nodePanggilFungsi(self, p_nodePanggilFungsi : node.nodePanggilFungsi, p_scope : scopeClass)->None | ir.Value:
        if(p_nodePanggilFungsi.namaFungsi.nilai in fungsiBuiltin.keys()):
            llvm_fungsi : ir.Function = self.setupBuiltin(p_nodePanggilFungsi.namaFungsi.nilai)
            # self.builder.
            # print("param input:", self.visit(p_nodePanggilFungsi.parameterInput[0], p_scope))
            getVariabel : ir.Value | None = self.visit(p_nodePanggilFungsi.parameterInput[0], p_scope)
            if(getVariabel is None):raise Exception("VARIABEL GAK KETEMU, SAFEGUARD JEBOL")
            else:
                llvm_parameterInput : ir.Value = getVariabel
                
                return self.builder.call(llvm_fungsi, [self.builder.load(llvm_parameterInput)])
    
    def baca_nodeIdentifier(self, p_nodeIdentifier : node.nodeIdentifier, p_scope : scopeClass)-> ir.Value:
        # print("valuenya:",p_nodeIdentifier.identifierToken)
        # print("ada di scope", p_scope.getVariabel(p_nodeIdentifier.identifierToken))
        return p_scope.getVariabel(p_nodeIdentifier.identifierToken)
    
    def proses(self, p_astReferensi : ASTClass)->None:
        nodeList : list[node.nodeClass] = p_astReferensi.getTree()
        for fungsiNode in nodeList:
            if(isinstance(fungsiNode, node.nodeBikinFungsi)):
                # self.bacaFungsi(fungsiNode)
                self.visit(fungsiNode, self.rootScope)
            else:
                raise Exception("ADA CODE DILUAR SCOPE")
        # print("FINAL:\n",str(self.modul))
    
    def getModul(self)->ir.Module:
        return self.modul