import os
import subprocess
import tempfile
import llvmlite.binding as llvm
from llvmlite import ir
from pathlib import Path
import config



# Inisialisasi LLVM backend
# llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()


class LLVMMergerClass:

    def proses(
        self,
        eksekusi : bool,
        namaFile : str,
        ir_str: ir.Module,
        output_exe_path: str,
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

        # print("TEST KONFIG", config.path_runtimeCPP)

        targetPathEXE : Path
        if(len(output_exe_path)==0):
            targetPathEXE = Path.cwd()
        else:
            targetPathEXE = Path(output_exe_path)

        try:
            # 1. Pastikan target_exe berupa Absolute Path & ber-ekstensi .exe
            target_exe = (targetPathEXE / f"{namaFile}.exe").resolve()

            cmd = [
                compiler,
                temp_obj_path,
                str(config.path_runtimeCPP),
                "-o",
                str(target_exe), # Kirim FULL ABSOLUTE PATH ke G++
                "-fno-pic",
                "-fno-pie",
                "-Wl,--gc-sections"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                # 2. VALIDASI FISIK FILE: Cek apakah filenya BENERAN ada di harddisk!
                if target_exe.exists():
                    # print(f"✅ Linking Berhasil! Binary terbuat di: {target_exe}")
                    
                    # Baru deh auto-execute
                    if eksekusi:
                        subprocess.run([str(target_exe)], check=True)
                        
                else:
                    print(f"❌ ANEH: G++ bilang sukses (returncode 0), tapi file ga ada di {target_exe}!")
                    print("💡 Kemungkinan besar: Di-quarantine Antivirus atau tersimpan di folder lain.")

            else:
                print(f"❌ G++ Linking Failed:\n{result.stderr}")
        
        finally:
            # 5. BERSIH-BERSIH: Hapus file .o temporary biar gak nyampah di disk
            if os.path.exists(temp_obj_path):
                os.remove(temp_obj_path)
        pass