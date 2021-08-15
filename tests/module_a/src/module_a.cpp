#include "module_a.hpp"
#include "module_b/module_b.hpp"
#include "module_c/module_c.hpp"

#define MY_NUMBER 11

int module_a::get_number(){
    return MY_NUMBER * module_b::get_number() * module_c::get_number();
}

#undef MY_NUMBER