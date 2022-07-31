#include "Region.h"

Region::Region(std::string s, int i, std::vector<int> c) : Land(s, i, c) {}
void Region::init_n_c(std::vector<Region*> r_ptrs, std::vector<Province*> p_ptrs)
{
	neighbours = r_ptrs;
	children = p_ptrs;
}
void Region::tick()
{
	
}