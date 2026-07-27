import os
import llvmlite.binding as llvm

# 1. WAJIB: Inisialisasi Target Native CPU Komputer Lu!
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

# 2. Kunci lokasi file
BASE_DIR = os.path.dirname(__file__)
LL_FILE = os.path.join(BASE_DIR, "main.ll")
OBJ_FILE = os.path.join(BASE_DIR, "main.o")

# 3. Baca main.ll
with open(LL_FILE, "r", encoding="utf-8") as f:
    llvm_ir = f.read()

# 4. Parse & Verify
mod = llvm.parse_assembly(llvm_ir)
mod.verify()

# 5. Convert ke main.o Native
target = llvm.Target.from_default_triple()
target_machine = target.create_target_machine()
obj_bytes = target_machine.emit_object(mod)

# 6. Tulis file
with open(OBJ_FILE, "wb") as f:
    f.write(obj_bytes)

print("✅ SUCCESS: main.ll -> main.o")