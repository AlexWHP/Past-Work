#pragma once
#include "Land.h"
#include "Region.h"
#include <string>
#include <vector>

class Territory : public Land
{
public:
    Territory(std::string s, int i, std::vector<int> c); // Founded on initialization
public:
    std::vector<Territory*> neighbours;
    std::vector<Region*> children;
public:
    void init_n_c(std::vector<Territory*> t_ptrs, std::vector<Region*> r_ptrs);
};