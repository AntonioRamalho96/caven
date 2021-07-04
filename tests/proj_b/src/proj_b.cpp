#include <iostream>

#include "proj_b.hpp"
#include "proj_d.hpp"
#include "proj_e.hpp"

void proj_b::print(){
	std::cout << "In B" << std::endl;
	proj_e::print();
	proj_d::print();
}
