from llvmlite import ir

# 1. Inisialisasi Module & Function main()
module = ir.Module(name="fosfor_module")
main_type = ir.FunctionType(ir.IntType(32), [])
main_func = ir.Function(module, main_type, name="main")
block = main_func.append_basic_block(name="entry")
builder = ir.IRBuilder(block)

# 2. DEKLARASI PROTOTYPE FUNGSI BUILTIN (Biar LLVM tau 'tampilin_int' itu ada)
# void tampilin_int(int32)
void_type = ir.VoidType()
tampilin_type = ir.FunctionType(void_type, [ir.IntType(32)])
tampilin_func = ir.Function(module, tampilin_type, name="tampilin_int")

# =========================================================
# 3. PROSES AST DARI .FOS:
# =========================================================

# (A) Nemu: bikin variabel namanya umur tipenya integer nilainya 20;
umur_ptr = builder.alloca(ir.IntType(32), name="umur")             # Minta alokasi memori
builder.store(ir.Constant(ir.IntType(32), 20), umur_ptr)          # Isi variabel umur = 20

# (B) Nemu: tampilin(umur);
nilai_umur = builder.load(umur_ptr, name="val_umur")               # Ambil nilai dari variabel umur
builder.call(tampilin_func, [nilai_umur])                         # Panggil fungsi C++ tampilin_int(20)

# (C) Selesai main() -> return 0
builder.ret(ir.Constant(ir.IntType(32), 0))

# 4. Simpan ke file main.ll
with open("main.ll", "w") as f:
    f.write(str(module))