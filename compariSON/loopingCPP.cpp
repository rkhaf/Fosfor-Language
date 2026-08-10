#include <iostream>
#include <chrono>
#include <iomanip>

int main() {
    int total = 0;
    int i = 1;

    std::cout << "Mulai perulangan 100 juta..." << std::endl;

    auto start = std::chrono::high_resolution_clock::now();

    while (i <= 100000000) {
        total++;

        if (i % 20000000 == 0) {
            std::cout << "iterasi ke: " << i << "\n";
        }

        i++;
    }

    auto end = std::chrono::high_resolution_clock::now();
    double duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() / 1000000.0;

    std::cout << "\n[C++] Waktu eksekusi: " << std::fixed << std::setprecision(6) << duration << " detik" << std::endl;
    std::cout << "Hasil total: " << total << std::endl;

    return 0;
}