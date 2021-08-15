#include "module_b.hpp"
#include "module_d/module_d.hpp"
#include "module_e/module_e.hpp"

#define MY_NUMBER 7

int module_b::get_number(){
    return MY_NUMBER * module_d::get_number() * module_e::get_number();
}

#undef MY_NUMBER