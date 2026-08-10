import os
import subprocess
import tempfile
import llvmlite.binding as llvm
from llvmlite import ir

# Inisialisasi LLVM backend
# llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()


class LLVMMergerClass:

    def proses(
        self,
        namaFile : str,
        ir_str: ir.Module,
        output_exe_path: str,
        runtime_obj_path: str = "core/runtime/runtime.o",
        compiler: str = "g++",
    ) -> None:
        
        
        # 1. Parse IR String ke LLVM ModuleRef di RAM
        mod: llvm.ModuleRef = llvm.parse_assembly(str(ir_str))
        mod.verify()

        # 2. Setup Target Machine
        target : llvm.Target = llvm.Target.from_triple("x86_64-pc-windows-gnu")
        target_machine : llvm.TargetMachine = target.create_target_machine("", "", 2, "default", "default")

        mod.triple = "x86_64-pc-windows-gnu"
        mod.data_layout = str(target_machine.target_data)

        # 3. Convert IR RAM -> Byte Object File (.o)
        obj_bytes: bytes = target_machine.emit_object(mod)

        # 4. Tulis obj_bytes ke Temp File & Link bareng runtime.o
        # delete=False biar filenya gak langsung hilang pas file handler-nya ditutup
        with tempfile.NamedTemporaryFile(
            suffix=".o", delete=False
        ) as temp_obj_file:
            temp_obj_file.write(obj_bytes)
            temp_obj_path: str = temp_obj_file.name

        try:
            # Command: g++ <temp_main.o> <runtime.o> -o <main.exe>
            if(len(output_exe_path)==0):
                cmd: list[str] = [
                    compiler,
                    temp_obj_path,
                    runtime_obj_path,
                    "-o",
                    namaFile,
                    "-fno-pic",
                    "-fno-pie"
                ]
            else:
                cmd: list[str] = [
                    compiler,
                    temp_obj_path,
                    runtime_obj_path,
                    "-o",
                    output_exe_path,
                    "-fno-pic",
                    "-fno-pie"
                ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print("=== G++ ERROR LOG ===")
                print(result.stderr)
                raise RuntimeError(f"G++ Linking Failed:\n{result.stderr}")
            
            # Eksekusi linker
            subprocess.run(cmd, check=True)
        finally:
            # 5. BERSIH-BERSIH: Hapus file .o temporary biar gak nyampah di disk
            if os.path.exists(temp_obj_path):
                os.remove(temp_obj_path)