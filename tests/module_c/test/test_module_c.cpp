#include <iostream>
#include <assert.h>

#include "module_c.hpp"

int main(){
    std::cout << "Starting test..." << std::endl;
    assert(module_c::get_number()==10);
    std::cout << "Test was a success" << std::endl;
}