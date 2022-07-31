#pragma once
#include <string>
#include <vector>

class Tile
{
public:
	Tile(std::string s, int i, std::vector<int> c);
public:
	std::string name;
	int id;
	std::vector<int> colour; // 3 array for color values
};

