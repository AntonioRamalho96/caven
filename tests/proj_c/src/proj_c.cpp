#include <iostream>

#include "proj_c.hpp"
#include "proj_e.hpp"

void proj_c::print(){
	std::cout << "In C" << std::endl;
	proj_e::print();
}
