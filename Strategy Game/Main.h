#pragma once

#include <glad/glad.h>
#include <GLFW/glfw3.h>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include "Shader.h"
#include <vector>
#include <iostream>
#include "Game.h"
#include "Frame.h"

class Main
{
public:
    Main();
public:
    // Window
    int scr_width = 1920;
    int scr_height = 1080;
    float width_scale = 1.0;
    float height_scale = 1.0;
    float ui_scale = 1.0;

    // Display
    int offset_width = 0;
    int offset_height = 0;
    float zoom = 1.0;

    // Objects
    Game game;

    // Frames
    Frame frame_main_menu;
    Frame frame_game;
    Frame frame_game_menu;

    // Tile data
    int tile_width;
    int tile_height;
    int tile_channels;
    unsigned char* province_pixels;
    unsigned char* region_pixels;
    unsigned char* territory_pixels;
    // Textures - Main Menu (YTI)
    
    // Textures - Game
    unsigned int map_mode;
    unsigned int texture_prov;
    unsigned int texture_regi;
    unsigned int texture_terr;
    unsigned int texture_hm;
public:
    void create_frames();

    void process_input(GLFWwindow* window);

    void load_tile_images();
    void load_render_images();
    unsigned int* buffer(float vertices[32], unsigned int indices[6]);
    int main_loop();
};

