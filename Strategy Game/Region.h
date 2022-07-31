#pragma once
#include "Land.h"
#include "Province.h"
#include <string>
#include <vector>

class Region : public Land
{
public:
    Region(std::string s, int i, std::vector<int> c); // Founded on initialization
public:
    bool diseased = false;
    bool badweather = false;
    std::vector<Region*> neighbours;
    std::vector<Province*> children;
public:
    void init_n_c(std::vector<Region*> r_ptrs, std::vector<Province*> p_ptrs);
    void tick();
};