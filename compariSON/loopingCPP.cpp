#include <iostream>
#include <chrono>

int main() {
    auto start = std::chrono::high_resolution_clock::now();

    // Pake long long biar gak integer overflow pas nampung total 100 juta
    long long i = 0;
    long long total = 0;

    // Loop 100 Juta Kali
    while (i < 100000000) {
        total = total + i;
        i = i + 1;
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;

    std::cout << "Hasil Total : " << total << std::endl;
    std::cout << "Waktu C++   : " << duration.count() << " detik" << std::endl;

    return 0;
}