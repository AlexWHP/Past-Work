#pragma once
#include <vector>
#include <string>
#include <sstream>

#include "rapidcsv.h"
#include "Province.h"
#include "Region.h"
#include "Territory.h"
#include "Country.h"

class Country
{
public:
	Country(std::string s, double g);
public:
	std::string name;
	int net_pop = 0;
	int manpower = 0; // 0.4 of population
	double gold;
	double tax_rate = 0.1;
	double admin_efficiency = 0.05;
	double trade_tax_rate = 0.0;
	// Dependencies
	std::vector<Province*> provinces;
	std::vector<Region*> regions;
	std::vector<Territory*> territories;
public:
	void init_dependencies(std::vector<Province*> p_ptrs, std::vector<Region*> r_ptrs, std::vector<Territory*> t_ptrs);
	void tick(); //Tick, and then update income and
};