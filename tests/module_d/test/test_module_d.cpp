#include <iostream>
#include <assert.h>

#include "module_d.hpp"

int main(){
    std::cout << "Starting test..." << std::endl;
    assert(module_d::get_number()==(3));
    std::cout << "Test was a success" << std::endl;
}