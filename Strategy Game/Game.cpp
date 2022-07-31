#include "Game.h"

Game::Game() { State = GAME_MENU; }
void Game::build(std::string filename)
{
	loadgame = filename;
	init_constants(); // Builds Provinces and neighbour pointers
	if (loadgame == "YTI")
	{
		init_saves();
	}
	else
	{
		init_initial();
	}
}
void Game::init_constants()
{
	std::vector<std::string> children;
	std::vector<std::string> neighbours;
	std::vector<int> indices_n;
	std::vector<int> indices_c;
	std::vector<Province*> pro_ptrs;
	std::vector<Region*> reg_ptrs;
	std::vector<Territory*> ter_ptrs;
	// Get num provs, regions, territories
	rapidcsv::Document constants("data/Constants/constants.csv");
	std::vector<std::string> row = constants.GetRow<std::string>(0);
	num_provinces = std::stoi(row[0]);
	num_regions = std::stoi(row[1]);
	num_territories = std::stoi(row[2]);
	// Province (For all 3, initialises name-ID-colour and then does neighbours)
	rapidcsv::Document pro("Data/Constants/provinces.csv");
	for (int i = 0; i < num_provinces; i++)
	{
		std::vector<std::string> row = pro.GetRow<std::string>(i);
		// Initialise Province and save neighbours for pointers to be created
		provinces.push_back(Province(row[1], std::stoi(row[0]), string_converter(row[2])));
		neighbours.push_back(row[3]);
	}
	for (int i = 0; i < num_provinces; i++)
	{
		indices_n = string_converter(neighbours[i]);
		for (int j = 0; j < indices_n.size(); j++)
		{
			pro_ptrs.push_back(&provinces[indices_n[j]-1]);
		}
		provinces[i].init_neighbours(pro_ptrs);
		pro_ptrs.clear();
	}
	neighbours.clear();
	// Region
	rapidcsv::Document reg("Data/Constants/regions.csv");
	for (int i = 0; i < num_regions; i++)
	{
		std::vector<std::string> row = reg.GetRow<std::string>(i);
		regions.push_back(Region(row[1], std::stoi(row[0]), string_converter(row[2])));
		neighbours.push_back(row[3]);
		children.push_back(row[4]);
	}
	for (int i = 0; i < num_regions; i++)
	{
		// Converting neighbours and children to vector<int> to find the pointers of IDs
		indices_n = string_converter(neighbours[i]);
		for (int j = 0; j < indices_n.size(); j++)
		{
			reg_ptrs.push_back(&regions[indices_n[j] - 1]);
		}
		indices_c = string_converter(children[i]);
		for (int j = 0; j < indices_c.size(); j++)
		{
			pro_ptrs.push_back(&provinces[indices_c[j] - 1]);
		}
		regions[i].init_n_c(reg_ptrs, pro_ptrs);
		pro_ptrs.clear();
		reg_ptrs.clear();
	}
	neighbours.clear();
	children.clear();
	// Territory
	rapidcsv::Document ter("Data/Constants/territories.csv");
	for (int i = 0; i < num_territories; i++)
	{
		std::vector<std::string> row = ter.GetRow<std::string>(i);
		territories.push_back(Territory(row[1], std::stoi(row[0]), string_converter(row[2])));
		neighbours.push_back(row[3]);
		children.push_back(row[4]);
	}
	for (int i = 0; i < num_territories; i++)
	{
		// Converting neighbours and children to vector<int> to find the pointers of IDs
		indices_n = string_converter(neighbours[i]);
		for (int j = 0; j < indices_n.size(); j++)
		{
			ter_ptrs.push_back(&territories[indices_n[j] - 1]);
		}
		indices_c = string_converter(children[i]);
		for (int j = 0; j < indices_c.size(); j++)
		{
			reg_ptrs.push_back(&regions[indices_c[j] - 1]);
		}
		territories[i].init_n_c(ter_ptrs, reg_ptrs);
		reg_ptrs.clear();
		ter_ptrs.clear();
	}
}
void Game::init_saves()
{

}
void Game::init_initial()
{
	// Province Data (YTI region and territory for larger and saves)
	rapidcsv::Document prod("Data/Initial/province_data.csv");
	for (int i = 0; i < num_provinces; i++)
	{
		std::vector<std::string> row = prod.GetRow<std::string>(i);
		provinces[std::stoi(row[0])-1].init_variables(std::stoi(row[1]), std::stod(row[2]), std::stod(row[3]), std::stoi(row[4]));
	}
	// People Data
	std::vector<std::vector<People>> people(num_provinces);
	rapidcsv::Document peo("Data/Initial/people.csv");
	for (int i = 0; i < num_provinces; i++)
	{
		std::vector<std::string> row = peo.GetRow<std::string>(i);
		people[i].push_back(People(row[1], row[2], std::stod(row[3])));
	}
	// Product Data
	std::vector<std::vector<Product>> product(num_provinces);
	rapidcsv::Document pro("Data/Initial/production.csv");
	for (int i = 0; i < num_provinces; i++)
	{
		std::vector<std::string> row = pro.GetRow<std::string>(i);
		product[i].push_back(Product("Iron", 1.0, std::stod(row[1])));
		product[i].push_back(Product("Horses", 4.0, std::stod(row[2])));
	}
	// Terrain Data
	std::vector<std::vector<Terrain>> terrain(num_provinces);
	rapidcsv::Document ter("Data/Initial/terrain.csv");
	for (int i = 0; i < num_provinces; i++)
	{
		std::vector<std::string> row = ter.GetRow<std::string>(i);
		terrain[i].push_back(Terrain("Plains", 1.0, std::stod(row[1])));
		terrain[i].push_back(Terrain("Forests", 0.8, std::stod(row[2])));
		terrain[i].push_back(Terrain("Hills", 0.8, std::stod(row[3])));
		terrain[i].push_back(Terrain("Mountains", 0.5, std::stod(row[4])));
	}
	// Country Data
	rapidcsv::Document cou("Data/Initial/countries.csv");
	std::vector<Province*> p_ptrs;
	std::vector<Region*> r_ptrs;
	std::vector<Territory*> t_ptrs;
	std::vector<int> indices;
	rapidcsv::Document constants("Data/Initial/variables.csv");
	std::vector<std::string> row = constants.GetRow<std::string>(0);
	num_countries = std::stoi(row[0]);
	for (int i = 0; i < num_countries; i++)
	{
		std::vector<std::string> row = cou.GetRow<std::string>(i);
		countries.push_back(Country(row[0], std::stod(row[1])));
		// Province
		indices = string_converter(row[2]);
		for (int j = 0; j < indices.size(); j++)
		{
			if (indices[j] != 0)
			{
				p_ptrs.push_back(&provinces[indices[j] - 1]);
			}
		}
		// Region
		indices = string_converter(row[3]);
		for (int j = 0; j < indices.size(); j++)
		{
			if (indices[j] != 0)
			{
				r_ptrs.push_back(&regions[indices[j] - 1]);
			}
		}
		// Territory
		indices = string_converter(row[4]);
		for (int j = 0; j < indices.size(); j++)
		{
			if (indices[j] != 0)
			{
				t_ptrs.push_back(&territories[indices[j] - 1]);
			}
		}
		countries[i].init_dependencies(p_ptrs, r_ptrs, t_ptrs);
	}
}

void Game::tick()
{
	tick_count();
	tick_world();
	// std::cout << countries[0].gold << std::endl;
}
void Game::tick_count()
{
	for (int i = 0; i < countries.size(); i++)
	{
		countries[i].tick();
	}
}
void Game::tick_world()
{
	// Tick down from territories and evaluate from their (Food, Weather and disease (Regions)
	for (int i = 0; i < territories.size(); i++)
	{
		if (territories[i].owner == "")
		{
			for (int j = 0; j < territories[i].children.size(); j++)
			{
				Region* region = territories[i].children[j];
				if (region->owner == "")
				{
					for (int k = 0; k < territories[i].children.size(); k++)
					{
						// Evaluate Province
						Province* province = region->children[k];
						province->update_food();
					}
				}
				else
				{
					// Evaluate Region
					region->update_food();
				}
			}
		}
		else
		{
			// Evaluate Territory
			territories[i].update_food();
		}
		// Tick weather and diseases at this level
		
	}
}

std::vector<int> Game::string_converter(std::string s)
{
	char delimiter = ',';
	std::vector<int> nums;
	std::stringstream sstream(s);
	std::string num;
	while (std::getline(sstream, num, delimiter)) {
		nums.push_back(std::stoi(num));
	}
	return nums;
}