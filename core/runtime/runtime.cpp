// runtime.cpp
#include <iostream>
#include <chrono>
#include <iomanip>

static std::chrono::high_resolution_clock::time_point g_start_time;

template<typename T>
void ngeprint(T p_nilai){
    std::cout<<p_nilai<<std::endl;
}

extern "C" {
    void fosfor_mulai_timer(){
        g_start_time = std::chrono::high_resolution_clock::now();
    }

    void fosfor_stop_timer(){
        auto end_time = std::chrono::high_resolution_clock::now();
        // auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time-g_start_time).count();

        // double detik = duration / 1000000.0;

        std::chrono::duration<double> duration = end_time - g_start_time;

        // std::cout << std::fixed << std::setprecision(4);
        std::cout << "\n[Fosfor] Waktu eksekusi: " << duration.count() << " detik" << std::endl;
    }

    void fosfor_tampilin_int(int x)        { ngeprint(x); }
    void fosfor_tampilin_str(const char* s){ ngeprint(s); }
    void fosfor_tampilin_flt(float f)     { ngeprint(f); }
    void fosfor_tampilin_bool(bool b)      { ngeprint(b ? "benar" : "salah"); }
}