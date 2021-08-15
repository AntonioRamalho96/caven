#include <iostream>
#include <assert.h>

#include "module_a.hpp"

int main(){
    std::cout << "Starting test..." << std::endl;
    assert(module_a::get_number()==(11*10*42));
    std::cout << "Test was a success" << std::endl;
}