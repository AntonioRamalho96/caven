#include <iostream>
#include <assert.h>

#include "module_e.hpp"

int main(){
    std::cout << "Starting test..." << std::endl;
    assert(module_e::get_number()==2);
    std::cout << "Test was a success" << std::endl;
}