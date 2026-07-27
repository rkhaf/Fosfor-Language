// runtime.cpp
#include <iostream>

extern "C" {
    void tampilin_int(int val) {
        std::cout << "Output Fosfor: " << val << std::endl;
    }
    
    void tampilin_str(const char* val) {
        std::cout << "Output Fosfor: " << val << std::endl;
    }
}