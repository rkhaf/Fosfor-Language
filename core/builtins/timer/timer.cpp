#include <chrono>
#include <iomanip>
#include <iostream>

static std::chrono::high_resolution_clock::time_point g_start_time;

extern "C" {
    void fosfor_mulai_timer(){
        g_start_time = std::chrono::high_resolution_clock::now();
    }

    void fosfor_stop_timer(){
        auto end_time = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> duration = end_time - g_start_time;

        // std::cout << std::fixed << std::setprecision(4);
        std::cout << "\n[Fosfor] Waktu eksekusi: " << duration.count() << " detik" << std::endl;
    }
}