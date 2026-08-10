from __future__ import annotations
from llvmlite import ir
from typing import Optional, Union
from typing import cast
from typing import Any, Callable, Dict
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

mappingOpsInt : dict[str, str] = {
    "+" : "add",
    "-" : "sub",
    "*" : "mul",
    "/" : "sdiv",
    "%" : "srem",
}

mappingOpsFlt : dict[str, str] = {
    "+" : "fadd",
    "-" : "fsub",
    "*" : "fmul",
    "/" : "fdiv",
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
        
        if(namaBuiltin in self.fungsiExtern):
            return self.modul.globals[namaBuiltin]
        
        if(not p_namaFungsi in self.fungsiExtern.keys()):
            parameterBuiltin : list[ir.Type] = cast(list[ir.Type], fungsiBuiltin[p_namaFungsi]["parameter"])
            tipeReturnBuiltin : ir.Type = cast(ir.Type, fungsiBuiltin[p_namaFungsi]["tipeReturn"])
            
            llvm_tipeFungsi : ir.FunctionType = ir.FunctionType(tipeReturnBuiltin, parameterBuiltin)
            llvm_fungsi : ir.Function = ir.Function(self.modul, llvm_tipeFungsi, namaBuiltin)
            
            self.fungsiExtern[namaBuiltin] = llvm_fungsi
        
        return self.fungsiExtern[namaBuiltin]
    
    def llvm_addBlok(self, p_namaBlok : str, p_statement : list[node.nodeClass]|list[node.nodeKalau], p_scope : scopeClass)->ir.Block:
        if(not self.builder is None):
            tempBlok : ir.Block = self.builder.append_basic_block(p_namaBlok)
            self.builder.position_at_start(tempBlok)
            
            for statemen in p_statement:
                self.visit(statemen, p_scope)
            
            return tempBlok
    
    def visit(self, p_node : node.nodeClass, p_scope : scopeClass)->ir.Value | None:
        namaFungsi : str =f"baca_{type(p_node).__name__}"
        fungsiTujuan : Callable[[Any, Any], Any] = getattr(self, namaFungsi)
        return fungsiTujuan(p_node, p_scope)
    
    def baca_nodeBikinVariabel(self, p_nodeBikinVariabel : node.nodeBikinVariabel, p_scope : scopeClass)->None:
        if(not self.builder is None):
            konversiTipedataVariabel : ir.Type = konvertClass.konversiTipedata(p_nodeBikinVariabel.tipedataVariabel)

            nilaiVariabel : ir.Value | None = self.visit(p_nodeBikinVariabel.nilaiVariabel, p_scope) 
            
            llvm_alokasi : ir.AllocaInstr = cast(ir.AllocaInstr, self.builder.alloca(konversiTipedataVariabel, name=p_nodeBikinVariabel.namaVariabel)) #type:ignore
            
            self.builder.store(nilaiVariabel, llvm_alokasi) #type:ignore

            p_scope.addVariabel(p_nodeBikinVariabel.namaVariabel, llvm_alokasi)
        pass
    
    def baca_nodeBikinFungsi(self, p_nodeBikinFungsi : node.nodeBikinFungsi, p_scope : scopeClass)->None:
        if(p_nodeBikinFungsi.namaFungsi=="main"):
            newScope : scopeClass = scopeClass(p_scope)
            
            llvm_tipeFungsi : ir.FunctionType = ir.FunctionType(ir.IntType(32), [])
            llvm_fungsiBaru : ir.Function = ir.Function(self.modul, llvm_tipeFungsi, p_nodeBikinFungsi.namaFungsi)
            
            llvm_entryBlock : ir.Block = llvm_fungsiBaru.append_basic_block(name="entry") #type:ignore
            
            self.builder = ir.IRBuilder(llvm_entryBlock)
            
            zeroExitCode : ir.Constant = ir.Constant(ir.IntType(32), 0)
            
            for nodeKode in p_nodeBikinFungsi.isiFungsi:
                self.visit(nodeKode, newScope)
                pass
            # pass
            self.builder.ret(zeroExitCode) #type:ignore
        else:
            newScope : scopeClass = scopeClass(p_scope)
            
            llvm_parameters : list[ir.Type] = []
            llvm_tipedataFungsi : ir.Type = konvertClass.konversiTipedata(p_nodeBikinFungsi.tipedataFungsi)
            
            #ngeiterasi tipedata paramnbya dulu
            for param in p_nodeBikinFungsi.parameterFungsi:
                llvm_parameters.append(konvertClass.konversiTipedata(param.tipedata))
            
            llvm_tipeFungsi : ir.FunctionType = ir.FunctionType(llvm_tipedataFungsi, llvm_parameters)
            llvm_fungsiBaru : ir.Function = ir.Function(self.modul, llvm_tipeFungsi, p_nodeBikinFungsi.namaFungsi)
            
            llvm_entryBlock : ir.Block = llvm_fungsiBaru.append_basic_block(name="entry") #type:ignore
            self.builder = ir.IRBuilder(llvm_entryBlock)
            
            zeroExitCode : ir.Constant = ir.Constant(ir.IntType(32), 0)
            
            returnanFungsi : Any
            
            #ngisiin nama utk paramnya
            for paramIdx in range(0, len(p_nodeBikinFungsi.parameterFungsi)):
                namaParam : str = p_nodeBikinFungsi.parameterFungsi[paramIdx].nama
                llvm_fungsiBaru.args[paramIdx].name = namaParam
                
                llvm_atomikParam : ir.AllocaInstr = self.builder.alloca(llvm_fungsiBaru.args[paramIdx].type, name=namaParam)
                self.builder.store(llvm_fungsiBaru.args[paramIdx], llvm_atomikParam)
                p_scope.addVariabel(namaParam, llvm_atomikParam)
            
            for nodeKode in p_nodeBikinFungsi.isiFungsi:
                if(isinstance(nodeKode, node.nodeBalikin)):
                    returnanFungsi = self.visit(nodeKode, newScope)
                else:
                    self.visit(nodeKode, newScope)
                pass
            # pass
            self.builder.ret(returnanFungsi) #type:ignore

    def baca_nodePanggilFungsi(self, p_nodePanggilFungsi : node.nodePanggilFungsi, p_scope : scopeClass)->ir.Value:
        if(p_nodePanggilFungsi.namaFungsi.nilai in fungsiBuiltin.keys()):
            llvm_fungsi : ir.Function = self.setupBuiltin(p_nodePanggilFungsi.namaFungsi.nilai)
            getVariabel : ir.Value | None = self.visit(p_nodePanggilFungsi.parameterInput[0], p_scope)
            
            if(getVariabel is None):raise Exception("VARIABEL GAK KETEMU, SAFEGUARD JEBOL")
            else:
                llvm_parameterInput : ir.Value = getVariabel
                return self.builder.call(llvm_fungsi, [llvm_parameterInput]) #type:ignore
            
        elif(p_nodePanggilFungsi.namaFungsi.nilai in self.modul.globals):
            llvm_fungsi : ir.Function = self.modul.globals[p_nodePanggilFungsi.namaFungsi.nilai]
            llvm_params : list[ir.Value] = []
            
            for paramIdx in range(0, len(p_nodePanggilFungsi.parameterInput)):
                paramInput : ir.Value = self.visit(p_nodePanggilFungsi.parameterInput[paramIdx], p_scope)
                llvm_params.append(paramInput)
                
            return self.builder.call(llvm_fungsi, llvm_params) #type:ignore 
        # raise Exception("STOPPER")
    
    def baca_nodeIdentifier(self, p_nodeIdentifier : node.nodeIdentifier, p_scope : scopeClass)-> ir.Value:
        if(p_scope.cekVariabel(p_nodeIdentifier.identifierToken)):
            getVar : ir.AllocaInstr = p_scope.getVariabel(p_nodeIdentifier.identifierToken)
            return cast(ir.Value, self.builder.load(getVar, f"load_{p_nodeIdentifier.identifierToken}")) #type: ignore
        else:
            raise Exception("variable gak ketemu, semantik kebobolan / blm didaftarin discope table")
            # self.errorHandlerObjek.tambahinError(__name__, 1, p_nodeIdentifier.baris, p_bagian=p_nodeIdentifier.identifierToken)
            # return ir.Constant(ir.IntType(32), 67)
    
    def baca_nodeNomor(self, p_nodeNomor : node.nodeNomor, p_scope : scopeClass)->ir.Value:
        if(p_nodeNomor.tipe==TIPEDATA_INTEGER):return ir.Constant(ir.IntType(32), int(p_nodeNomor.nilai))
        else:return ir.Constant(ir.FloatType(), float(p_nodeNomor.nilai))
    
    def baca_nodeBiner(self, p_nodeBiner : node.nodeBiner, p_scope : scopeClass)->ir.Value:
        kiri : ir.Value | None = self.visit(p_nodeBiner.operand1, p_scope)
        kanan : ir.Value | None = self.visit(p_nodeBiner.operand2, p_scope)
        
        if(isinstance(kiri.type, ir.IntType)):
            if(p_nodeBiner.operator in mappingOpsInt):
                instruksi = getattr(self.builder, mappingOpsInt[p_nodeBiner.operator])
                # instruksi = self.mappingOpsInt[p_nodeBiner.operator](kiri, kanan, name="operasi_biner_int")
                return instruksi(kiri, kanan, name="operasi_biner_int")
            else:raise Exception("operator gk tersedia")
        
        elif(isinstance(kiri.type, ir.FloatType)):
            if(p_nodeBiner.operator in mappingOpsFlt):
                instruksi = getattr(self.builder, mappingOpsFlt[p_nodeBiner.operator])
                # instruksi = self.mappingOpsInt[p_nodeBiner.operator](kiri, kanan, name="operasi_biner_int")
                return instruksi(kiri, kanan, name="operasi_biner_flt")
            else:raise Exception("operator gk tersedia")
        
        else:
            raise Exception("operasi invalid")
        
        # raise Exception("STOPPER")
    
    def baca_nodeBanding(self, p_nodeBanding : node.nodeBanding, p_scope : scopeClass)->ir.Value:
        kiri = self.visit(p_nodeBanding.operand1, p_scope)
        kanan = self.visit(p_nodeBanding.operand2, p_scope)
        pass
        return self.builder.icmp_signed(p_nodeBanding.operator.nilai, kiri, kanan, "opr_perbandingan")
    
    def baca_nodeBalikin(self, p_nodeBalikin : node.nodeBalikin, p_scope : scopeClass)->ir.Value | None:
        # print(self.visit(p_nodeBalikin.returnEkspresi, p_scope))
        # raise Exception("[baca_nodeBalikin] STOPPER")
        return self.visit(p_nodeBalikin.returnEkspresi, p_scope)
    
    def baca_nodePenugasan(self, p_nodePenugasan : node.nodePenugasan, p_scope : scopeClass)->None:
        llvm_nilai : ir.Instruction = self.visit(p_nodePenugasan.ekspresi, p_scope)
        
        if(isinstance(p_nodePenugasan.referensi, node.nodeIdentifier)):
            namaIdtf : str = p_nodePenugasan.referensi.identifierToken
            if(p_scope.cekVariabel(namaIdtf)):
                llvm_alokaMem : ir.AllocaInstr = p_scope.getVariabel(namaIdtf)
                self.builder.store(llvm_nilai, llvm_alokaMem)
            else:
                raise Exception("SAFEGUARD JEBOL, IDENTIFIER GK KETEMU")
        else:
            raise Exception("UNEXPECTED RESULT")
    
    def baca_nodePerulanganSelama(self, p_nodePerulanganSelama : node.nodePerulanganSelama, p_scope : scopeClass)->ir.Value | None:
        if (not self.builder is None):
            # 1. Bikin label basic block
            cond_bb = self.builder.function.append_basic_block("loop.kondisi")
            body_bb = self.builder.function.append_basic_block("loop.badan")
            end_bb = self.builder.function.append_basic_block("loop.akhir")

            # 2. Dari lokasi sekarang, langsung lompat ke pengecekan kondisi
            self.builder.branch(cond_bb)

            # --- BLOCK KONDISI ---
            # 🔴 UBAH 1: Pake position_at_end biar instruksi cond di-append dari atas ke bawah
            self.builder.position_at_end(cond_bb)
            cond_val = self.visit(p_nodePerulanganSelama.kondisi, p_scope)
            # Jika True ke body_bb, Jika False ke end_bb
            self.builder.cbranch(cond_val, body_bb, end_bb)

            # --- BLOCK BODY (ISI LOOP) ---
            # 🔴 UBAH 2: Pake position_at_end biar stmt (termasuk i++) masuk ke body_bb secara urut
            self.builder.position_at_end(body_bb)
            for stmt in p_nodePerulanganSelama.isiLoop:
                self.visit(stmt, p_scope)

            # Jika di akhir body belum di-terminate, paksain branch balik ke cond_bb!
            if not self.builder.block.is_terminated:
                self.builder.branch(cond_bb)

            # --- PENTING: KUNCI BUILDER DI END_BB UNTUK STATEMENT SELANJUTNYA ---
            # 🔴 UBAH 3: Pake position_at_end biar statement di luar loop (kayak tampilin) masuk ke end_bb
            self.builder.position_at_end(end_bb)
    
    def baca_nodeKalau(self, p_nodeKalau : node.nodeKalau, p_scope : scopeClass)->None:
        
        getterKondisi : ir.Value | None = self.visit(p_nodeKalau.kondisi, p_scope)
        llvm_kondisi : ir.Value
        if(not getterKondisi is None):
            llvm_kondisi = getterKondisi
        else:
            raise Exception("STOPPER")
        
        llvm_merge_blok : ir.Block = self.builder.function.append_basic_block("if.end")
        # llvm_isiElif_blok : ir.Block  = self.builder.function.append_basic_block("if.elif")
        llvm_isiKalau_blok : ir.Block = self.builder.function.append_basic_block("if.then")
        llvm_else_blok : ir.Block = self.builder.function.append_basic_block("if.else")
        # llvm_isiKalau_blok : ir.Block = self.llvm_addBlok("if.then", p_nodeKalau.isiKalau, p_scope)
        # llvm_else_blok : ir.Block = self.llvm_addBlok("if.else", p_nodeKalau.isiElse, p_scope)
        
        self.builder.cbranch(llvm_kondisi, llvm_isiKalau_blok, llvm_else_blok)
        
        self.builder.position_at_start(llvm_isiKalau_blok)
        for nodeKode in p_nodeKalau.isiKalau:
            self.visit(nodeKode, p_scope)
        
        if not self.builder.block.is_terminated:
            self.builder.branch(llvm_merge_blok)
            
        self.builder.position_at_start(llvm_else_blok)
        
        listElif : list[node.nodeKalau] = p_nodeKalau.listElif
        isiElse : list[node.nodeClass] = p_nodeKalau.isiElse
        
        if(len(listElif)>0):
            for nodeKode in p_nodeKalau.listElif:
                if not len(nodeKode.isiElse)>0 and len(isiElse)>0:
                    nodeKode.isiElse = isiElse
                
                self.visit(nodeKode, p_scope)
                
            if not self.builder.block.is_terminated:
                self.builder.branch(llvm_merge_blok)
            
        elif len(isiElse)>0:
            self.builder.position_at_start(llvm_else_blok)
            for nodeKode in p_nodeKalau.isiElse:
                self.visit(nodeKode, p_scope)
                
            if not self.builder.block.is_terminated:
                self.builder.branch(llvm_merge_blok)
        
        else:
            if not self.builder.block.is_terminated:
                self.builder.branch(llvm_merge_blok)
                
        self.builder.position_at_start(llvm_merge_blok)
        
        # if(len(p_nodeKalau.listElif)):
        #     llvm_isiElif_blok : ir.Block  = self.builder.function.append_basic_block("if.elif")
        #     self.builder.position_at_start(llvm_isiElif_blok)
            
        #     for nodeElif in p_nodeKalau.listElif:
        #         self.baca_nodeKalau(nodeElif, p_scope)
                
        #     if not self.builder.block.is_terminated:
        #         self.builder.branch(llvm_blok_merge)
        
        # else:
        #     llvm_else_blok  = self.llvm_addBlok("if.else", p_nodeKalau.isiElse, p_scope)
        #     if not self.builder.block.is_terminated:
        #         self.builder.branch(llvm_blok_merge)
        
        
        # self.builder.position_at_start(llvm_blok_merge)
            
                
        pass
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