#include <iostream>

#include "proj_a.hpp"
#include "proj_b.hpp"
#include "proj_c.hpp"

void proj_a::print(){
	std::cout << "In A" << std::endl;
	proj_b::print();
	proj_c::print();
}
