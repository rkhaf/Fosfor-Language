// runtime.cpp
#include <iostream>

extern "C" {
    void fosfor_tampilin_int(int val) {
        std::cout << val << std::endl;
    }
    
    void fosfor_tampilin_str(const char* val) {
        std::cout << val << std::endl;
    }
}