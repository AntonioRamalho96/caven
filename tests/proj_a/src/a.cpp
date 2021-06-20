#include <iostream>

#include "a.hpp"
#include "b.hpp"

void a::test(){
    b::print();
    std::cout << "Proj A!" << std::endl;
}