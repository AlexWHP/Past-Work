#pragma once
#include <vector>
#include <string>
#include <sstream>

#include "rapidcsv.h"
#include "Province.h"
#include "Region.h"
#include "Territory.h"
#include "Country.h"

enum GameState { GAME_MENU, GAME_MENU_OPTIONS, GAME_ACTIVE, GAME_ACTIVE_MENU };

class Game
{
public:
    Game();
public:
    // What the game wants to render
    GameState State;
    //bool paused;
    int num_provinces = 0;
    int num_regions = 0;
    int num_territories = 0;
    int num_countries = 0;
    // Game constants
    //std::vector<Product> product_types;
    //std::vector<Terrain> terrain_types;

    std::string loadgame;
    std::vector<Province> provinces;
    std::vector<Region> regions;
    std::vector<Territory> territories;
    std::vector<Country> countries;

    // Initialize game state
    void build(std::string filename);
    void init_constants();
    void init_initial();
    void init_saves();
    // Tick
    void tick();
    void tick_count(); // Iterates through countries and ticks
    void tick_world(); // Iterates through 'world' and ticks
    // Helper Functions
    std::vector<int> string_converter(std::string s);
};