#include <iostream>
#include <assert.h>

#include "module_b.hpp"

int main(){
    std::cout << "Starting test..." << std::endl;
    assert(module_b::get_number()==(42));
    std::cout << "Test was a success" << std::endl;
}