#include <iostream>

template<typename T>
void ngeprint(T p_nilai){
    std::cout<<p_nilai<<std::endl;
}

extern "C" {
    void fosfor_tampilin_int(int x)        { ngeprint(x); }
    void fosfor_tampilin_str(const char* s){ ngeprint(s); }
    void fosfor_tampilin_flt(float f)     { ngeprint(f); }
    void fosfor_tampilin_bool(bool b)      { ngeprint(b ? "benar" : "salah"); }
}