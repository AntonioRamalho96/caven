#include "module_c.hpp"
#include "module_e/module_e.hpp"

#define MY_NUMBER 5

int module_c::get_number(){
    return MY_NUMBER * module_e::get_number();
}

#undef MY_NUMBER