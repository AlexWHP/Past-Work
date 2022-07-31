#include "Country.h"

Country::Country(std::string s, double g)
{
	std::string name;
	gold = g;
}
void Country::init_dependencies(std::vector<Province*> p_ptrs, std::vector<Region*> r_ptrs, std::vector<Territory*> t_ptrs)
{
	// Dependency pointers
	provinces = p_ptrs;
	regions = r_ptrs;
	territories = t_ptrs;
}
void Country::tick() 
{
	double income = 0.0;
	double trade = 0.0;
	// Province tick (YTI Famine ect.)
	for (int i = 0; i < provinces.size(); i++)
	{
		income += provinces[i]->population * tax_rate * admin_efficiency;
		if (trade_tax_rate != 0.0)
		{
			for (int j = 0; j < provinces[i]->products.size(); j++)
			{
				Product p = provinces[i]->products[j];
				trade += (p.value * (1 / p.difficulty)) * provinces[i]->urbanization * provinces[i]->development;
			}
		}
	}
	// Region tick
	for (int i = 0; i < regions.size(); i++)
	{
		income += regions[i]->population * tax_rate * admin_efficiency;
		if (trade_tax_rate != 0.0)
		{
			for (int j = 0; j < regions[i]->products.size(); j++)
			{
				Product p = regions[i]->products[j];
				trade += (p.value * (1 / p.difficulty)) * regions[i]->urbanization * regions[i]->development;
			}
		}
	}
	// Territory tick
	for (int i = 0; i < territories.size(); i++)
	{
		income += territories[i]->population * tax_rate * admin_efficiency;
		if (trade_tax_rate != 0.0)
		{
			for (int j = 0; j < territories[i]->products.size(); j++)
			{
				Product p = territories[i]->products[j];
				trade += (p.value * (1 / p.difficulty)) * territories[i]->urbanization * territories[i]->development;
			}
		}
	}
	// Updating Country
	gold += income + trade;
}