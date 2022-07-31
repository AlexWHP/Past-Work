#include "Territory.h"



Territory::Territory(std::string s, int i, std::vector<int> c) : Land(s, i, c) {}
void Territory::init_n_c(std::vector<Territory*> t_ptrs, std::vector<Region*> r_ptrs)
{
	neighbours = t_ptrs;
	children = r_ptrs;
}