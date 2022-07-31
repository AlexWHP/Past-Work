#include "Province.h"

Province::Province(std::string s, int i, std::vector<int> c) : Land(s, i, c) {}

void Province::init_neighbours(std::vector<Province*> p_ptrs)
{
	neighbours = p_ptrs;
}

void Province::tick()
{
	// Adjust food
}