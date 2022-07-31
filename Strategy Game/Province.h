#pragma once
#include "Land.h"
#include <string>
#include <vector>

class Province : public Land
{
public:
    Province(std::string s, int i, std::vector<int> c);
public:
    std::vector<Province*> neighbours;
public:
    void init_neighbours(std::vector<Province*> p_ptrs);
    void tick();
};
