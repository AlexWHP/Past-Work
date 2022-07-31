#pragma once
#include "Tile.h"
#include "Land.h"

// Defined in this as it is encapsulated by land
class People
{
public:
	People(std::string c, std::string r, double pr);
public:
	std::string culture;
	std::string religion;
	int opinion;
	double pop_ratio;
};
class Product
{
public:
	Product(std::string s, double v, double d);
public:
	std::string name;
	double value;
	double difficulty; // How hard to make
};
class Terrain
{
public:
	Terrain(std::string s, double a, double r);
public:
	std::string type;
	double arability;
	double ter_ratio; 
};
// Implemented at his level (YTI)
class Disease
{
public:

};
class Weather
{
public:

};

class Land : public Tile
{
public:
	Land(std::string s, int i, std::vector<int> c);
public:
	std::string owner = ""; // Initializing country needs to change this
	// Population (Groups)
	int population = 0;
	std::vector<People> pop_groups;
	// Development and urbanization
	double development = 0.0;
	double urbanization = 0.0;
	// Production
	std::vector<Product> products;
	// Food
	int food = 0; // Growth from urbanization (Lack thereof)
	// Food cap (calculated)
	double arability = 0.0; // Net from terrain (Calculated)
	// Geography
	std::vector<Terrain> terrain;
public:
	void init_dependents(std::vector<People> pg, std::vector<Product> prod, std::vector<Terrain> terr);
	void init_variables(int p, double dev, double urb, int f);
	void update_food();
};