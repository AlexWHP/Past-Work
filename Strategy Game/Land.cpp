#include "Land.h"

People::People(std::string c, std::string r, double pr)
{
	culture = c;
	religion = r;
	pop_ratio = pr;
}
Product::Product(std::string s, double v, double d)
{
	name = s;
	value = v;
	difficulty = d;
}
Terrain::Terrain(std::string s, double a, double r)
{
	type = s;
	arability = a;
	ter_ratio = r;
}

Land::Land(std::string s, int i, std::vector<int> c) : Tile(s, i, c) {}
void Land::init_dependents(std::vector<People> pg, std::vector<Product> prod, std::vector<Terrain> terr) 
{
	pop_groups = pg;
	products = prod;
	terrain = terr;
}
void Land::init_variables(int p, double dev, double urb, int f)
{
	population = p;
	// Development and urbanization
	development = dev;
	urbanization = urb;
	// Food
	food = f;
	for (int i = 0; i < terrain.size(); i++)
	{
		arability += terrain[i].arability;
	}
	arability = arability / terrain.size();
}

void Land::update_food()
{
	food += arability * (1 - urbanization) * population;
	food += arability * urbanization * (1 - development) * population;
}