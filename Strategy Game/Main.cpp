#include "Main.h"
#define STB_IMAGE_IMPLEMENTATION
#include <stb_image.h>

// Declaring identifiers
void framebuffer_size_callback(GLFWwindow* window, int width, int height);
float* coordinateTransform(float vertices[]);
Main::Main()
{
    main_loop();
}
int Main::main_loop()
{
    game.build("a");
    // glfw: initialize and configure
    // ------------------------------
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

#ifdef __APPLE__
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
#endif

    //GLFWwindow* window = glfwCreateWindow(scr_width, scr_height, "LearnOpenGL", glfwGetPrimaryMonitor(), NULL); // Fullscreen
    GLFWwindow* window = glfwCreateWindow(scr_width, scr_height, "LearnOpenGL", NULL, NULL);
    if (window == NULL)
    {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);

    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

    // glad: load all OpenGL function pointers
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
    {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }
    glfwSetInputMode(window, GLFW_STICKY_KEYS, GLFW_TRUE);
    glfwSetInputMode(window, GLFW_STICKY_MOUSE_BUTTONS, GLFW_TRUE);

    //glfwGetWindowContentScale(window, &xscale, &yscale);

    // Load tiles
    load_tile_images();

    // Load textures and height map
    load_render_images();
    // Shaders etc.
    Shader ourShader("VertexShader.vert", "FragmentShader.frag"); // you can name your shader files however you like

    // Textures and frames
    unsigned int VBO_map_mode, VAO_map_mode, EBO_map_mode;
    // Creation of texture (Bitmap for now)
    {
        // set up vertex data (and buffer(s)) and configure vertex attributes
        // ------------------------------------------------------------------
        float vertices[] = {
            // positions          // colors           // texture coords
             1.0f, 1.0f, 0.0f,    1.0f, 0.0f, 0.0f,   1.0f, 1.0f, // top right
             1.0f,-1.0f, 0.0f,    0.0f, 1.0f, 0.0f,   1.0f, 0.0f, // bottom right
            -1.0f,-1.0f, 0.0f,    0.0f, 0.0f, 1.0f,   0.0f, 0.0f, // bottom left
            -1.0f, 1.0f, 0.0f,    1.0f, 1.0f, 0.0f,   0.0f, 1.0f  // top left 
        };
        unsigned int indices[] = {
            0, 1, 3, // first triangle
            1, 2, 3  // second triangle
        };
        glGenVertexArrays(1, &VAO_map_mode);
        glGenBuffers(1, &VBO_map_mode);
        glGenBuffers(1, &EBO_map_mode);

        glBindVertexArray(VAO_map_mode);

        glBindBuffer(GL_ARRAY_BUFFER, VBO_map_mode);
        glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO_map_mode);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

        // position attribute
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)0);
        glEnableVertexAttribArray(0);
        // color attribute
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(3 * sizeof(float)));
        glEnableVertexAttribArray(1);
        // texture coord attribute
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(6 * sizeof(float)));
        glEnableVertexAttribArray(2);
    }
    // Creates panels associated with frames (Main menu, in-game etc.)
    unsigned int VBO, VAO, EBO;
    {
        // set up vertex data (and buffer(s)) and configure vertex attributes
        // ------------------------------------------------------------------
        float vertices[] = {
            // positions          // colors           // texture coords
             0.2f, 0.5f, 0.0f,    1.0f, 0.0f, 0.0f,   1.0f, 1.0f, // top right
             0.2f,-0.5f, 0.0f,    0.0f, 1.0f, 0.0f,   1.0f, 0.0f, // bottom right
            -0.2f,-0.5f, 0.0f,    0.0f, 0.0f, 1.0f,   0.0f, 0.0f, // bottom left
            -0.2f, 0.5f, 0.0f,    1.0f, 1.0f, 0.0f,   0.0f, 1.0f  // top left 
        };
        unsigned int indices[] = {
            0, 1, 3, // first triangle
            1, 2, 3  // second triangle
        };
        glGenVertexArrays(1, &VBO);
        glGenBuffers(1, &VAO);
        glGenBuffers(1, &EBO);

        glBindVertexArray(VAO);

        glBindBuffer(GL_ARRAY_BUFFER, VBO);
        glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

        // position attribute
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)0);
        glEnableVertexAttribArray(3);
        // color attribute
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(3 * sizeof(float)));
        glEnableVertexAttribArray(4);
        // texture coord attribute
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(6 * sizeof(float)));
        glEnableVertexAttribArray(5);
    }
    create_frames();
    map_mode = texture_prov;

    //glEnableVertexAttribArray(0);
    // Clear buffer
    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
    glBindVertexArray(0);
    // render loop
    float vertices[] = {
        // positions          // colors           // texture coords
         1.0f, 1.0f, 0.0f,    1.0f, 0.0f, 0.0f,   1.0f, 1.0f, // top right
         1.0f,-1.0f, 0.0f,    0.0f, 1.0f, 0.0f,   1.0f, 0.0f, // bottom right
        -1.0f,-1.0f, 0.0f,    0.0f, 0.0f, 1.0f,   0.0f, 0.0f, // bottom left
        -1.0f, 1.0f, 0.0f,    1.0f, 1.0f, 0.0f,   0.0f, 1.0f  // top left 
    };

    glBindBuffer(GL_ARRAY_BUFFER, VBO_map_mode);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO_map_mode);
    while (!glfwWindowShouldClose(window))
    {
        /*
        // input
        process_input(window);
        // Menu Render
        if (game.State == GAME_MENU)
        {
            glBindBuffer(GL_ARRAY_BUFFER, VBO);
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
            glClearColor(0.8f, 0.8f, 0.8f, 1.0f);
            glClear(GL_COLOR_BUFFER_BIT);
        }
        // Game Render
        else if (game.State == GAME_ACTIVE)
        {
            //glBindBuffer(GL_ARRAY_BUFFER, VBO_map_mode);
            //glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO_map_mode);
            // render
            // ------
            glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
            glClear(GL_COLOR_BUFFER_BIT);

            //glBindBuffer(GL_ARRAY_BUFFER, VBO_map_mode);
            //glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO_map_mode);
            // bind Texture
            glActiveTexture(GL_TEXTURE0);
            glBindTexture(GL_TEXTURE_2D, map_mode);
            // render container
            ourShader.use();
            glBindVertexArray(VAO_map_mode);
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
        }
        // Unbinding buffer - Not necassary
        //glBindBuffer(GL_ARRAY_BUFFER, 0);
        //glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
        //glBindVertexArray(0);
        
        // glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
        // render window
        */
        // input
        process_input(window);
        // Menu Render
        if (game.State == GAME_MENU)
        {
            glClearColor(0.8f, 0.8f, 0.8f, 1.0f);
            glClear(GL_COLOR_BUFFER_BIT);
        }
        // Game Render
        else if (game.State == GAME_ACTIVE)
        {
            // render
            // ------
            glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
            glClear(GL_COLOR_BUFFER_BIT);
            // bind Texture
            glActiveTexture(GL_TEXTURE0);
            glBindTexture(GL_TEXTURE_2D, map_mode);
            // render container
            ourShader.use();
            glBindVertexArray(VAO_map_mode);
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
        }
        glfwSwapBuffers(window);
        glfwPollEvents();
    }
    // Shader etc.
    glDeleteVertexArrays(1, &VAO_map_mode);
    glDeleteBuffers(1, &VBO_map_mode);
    glDeleteBuffers(1, &EBO_map_mode);
    // glfw: terminate, clearing all previously allocated GLFW resources.
    glfwTerminate();
    return 0;
}
void Main::load_tile_images()
{
    // Check if all values (width, height, channels) is the same.
    stbi_set_flip_vertically_on_load(false); // tell stb_image.h to flip loaded texture's on the y-axis.
    province_pixels = stbi_load("ireland_prov.bmp", &tile_width, &tile_height, &tile_channels, 3);
    region_pixels = stbi_load("ireland_regi.bmp", &tile_width, &tile_height, &tile_channels, 3);
    territory_pixels = stbi_load("ireland_terr.bmp", &tile_width, &tile_height, &tile_channels, 3);
    // Should check if correctly loaded
}
void Main::load_render_images()
{
    stbi_set_flip_vertically_on_load(true);
    // Province map mode
    {
        // Texture
        glGenTextures(1, &texture_prov);
        glBindTexture(GL_TEXTURE_2D, texture_prov);
        // set the texture wrapping/filtering options (on the currently bound texture object)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        // load and generate the texture
        int width, height, nrChannels;
        unsigned char* data = stbi_load("ireland_prov.bmp", &width, &height, &nrChannels, 0);
        if (data)
        {
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
            glGenerateMipmap(GL_TEXTURE_2D);
        }
        else
        {
            std::cout << "Failed to load texture" << std::endl;
        }
        stbi_image_free(data);
    }
    // Region map mode
    {
        // Texture
        glGenTextures(1, &texture_regi);
        glBindTexture(GL_TEXTURE_2D, texture_regi);
        // set the texture wrapping/filtering options (on the currently bound texture object)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        // load and generate the texture
        int width, height, nrChannels;
        unsigned char* data = stbi_load("ireland_regi.bmp", &width, &height, &nrChannels, 0);
        if (data)
        {
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
            glGenerateMipmap(GL_TEXTURE_2D);
        }
        else
        {
            std::cout << "Failed to load texture" << std::endl;
        }
        stbi_image_free(data);
    }
    // Territory map mode
    {
        // Texture
        glGenTextures(1, &texture_terr);
        glBindTexture(GL_TEXTURE_2D, texture_terr);
        // set the texture wrapping/filtering options (on the currently bound texture object)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        // load and generate the texture
        int width, height, nrChannels;
        unsigned char* data = stbi_load("ireland_terr.bmp", &width, &height, &nrChannels, 0);
        if (data)
        {
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
            glGenerateMipmap(GL_TEXTURE_2D);
        }
        else
        {
            std::cout << "Failed to load texture" << std::endl;
        }
        stbi_image_free(data);
    }
    // Height Map
    {
        glGenTextures(2, &texture_hm);
        glBindTexture(GL_TEXTURE_2D, texture_hm);
        // set the texture wrapping/filtering options (on the currently bound texture object)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        // load and generate the texture
        int width, height, nrChannels;
        unsigned char* data = stbi_load("ireland_heightmap.bmp", &width, &height, &nrChannels, 0);
        if (data)
        {
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
            glGenerateMipmap(GL_TEXTURE_2D);
        }
        else
        {
            std::cout << "Failed to load texture" << std::endl;
        }
        stbi_image_free(data);
        // Greyscale height map (Becomes 3D value for a pixel)
        // z = height_map[x] / 255
        // Geomipmapping
    }
}
void Main::create_frames()
{
    // Main Menu
    {
        // Add a function to stop all the {} for left bottom width height etc.
        unsigned int indices[] = {
                0, 1, 3, // first triangle
                1, 2, 3  // second triangle
        };
        // Main Panel
        {
            float vertices[] = {
                // positions          // colors           // texture coords
                 0.2f, 0.5f, 0.0f,    0.0f, 0.0f, 0.0f,   1.0f, 1.0f, // top right
                 0.2f,-0.5f, 0.0f,    0.0f, 0.0f, 0.0f,   1.0f, 0.0f, // bottom right
                -0.2f,-0.5f, 0.0f,    0.0f, 0.0f, 0.0f,   0.0f, 0.0f, // bottom left
                -0.2f, 0.5f, 0.0f,    0.0f, 1.0f, 0.0f,   0.0f, 1.0f  // top left 
            };
            // left, bottom, width (right - left), height (top - bottom)
            float left, bottom, width, height;
            left = (vertices[16] + 1) / 2;
            bottom = (vertices[17] + 1) / 2;
            width = (vertices[0] + 1) / 2 - left;
            height = (vertices[1] + 1) / 2 - bottom;
            float v[4] = { left, bottom, width, height };
            Panel main("Main Menu", v);
            // Setting Render values
            unsigned int* b = Main::buffer(vertices, indices);
            unsigned int b2[3] = {b[0], b[1], b[2]};
            main.setBuffers(b2);
            frame_main_menu.panels.push_back(main);
        }
        // Start Game Button
        {
            float vertices[] = {
                // positions          // colors           // texture coords
                 0.5f, 0.5f, 0.0f,    0.0f, 0.0f, 0.0f,   1.0f, 1.0f, // top right
                 0.5f,-0.5f, 0.0f,    0.0f, 0.0f, 0.0f,   1.0f, 0.0f, // bottom right
                -0.5f,-0.5f, 0.0f,    0.0f, 0.0f, 0.0f,   0.0f, 0.0f, // bottom left
                -0.5f, 0.5f, 0.0f,    0.0f, 1.0f, 0.0f,   0.0f, 1.0f  // top left 
            };
            float left, bottom, width, height;
            left = (vertices[16] + 1) / 2;
            bottom = (vertices[17] + 1) / 2;
            width = (vertices[0] + 1) / 2 - left;
            height = (vertices[1] + 1) / 2 - bottom;
            float v[4] = { left, bottom, width, height };
            Button button("Start Game", v);
            button.setBuffers(Main::buffer(vertices, indices));
            frame_main_menu.panels[0].buttons.push_back(button);
        }
    }
}
unsigned int* Main::buffer(float vertices[32], unsigned int indices[6])
{
    unsigned int VBO, VAO, EBO;
    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glGenBuffers(1, &EBO);

    glBindVertexArray(VAO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
    unsigned int b[3] = { VBO, VAO, EBO };
    return b;
}
void Main::process_input(GLFWwindow* window)
{
    if (game.State == GAME_MENU)
    {
        // Keys
        {
            if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS && glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_RELEASE)
                glfwSetWindowShouldClose(window, true);
        }
        // Mouse
        {
            if (glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_LEFT) == GLFW_PRESS && glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_LEFT) == GLFW_RELEASE)
            {
                int width, height, x_pix, y_pix, index;
                double xpos, ypos;
                std::string action;
                glfwGetWindowSize(window, &width, &height);
                glfwGetCursorPos(window, &xpos, &ypos);
                // Evaluate other objects at position (YTI)
                for (int i = 0; i < frame_main_menu.panels.size(); i++)
                {
                    // Check sub panels (YTI)
                    action = frame_main_menu.panels[i].pressed(xpos / width, ypos / height);
                    if (action == "Start Game")
                    {
                        game.State = GAME_ACTIVE;
                    }
                }
            }
        }
    }
    else if (game.State == GAME_ACTIVE)
    {
        // Keys
        {
            if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS && glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_RELEASE)
                game.State = GAME_MENU;
                // Delete game
                //glfwSetWindowShouldClose(window, true);
            if (glfwGetKey(window, GLFW_KEY_SPACE) == GLFW_PRESS && glfwGetKey(window, GLFW_KEY_SPACE) == GLFW_RELEASE)
                game.tick();
            // Camera
            // Camera movement
            if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS && glfwGetKey(window, GLFW_KEY_W) == GLFW_RELEASE)
                game.tick();
            if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS && glfwGetKey(window, GLFW_KEY_A) == GLFW_RELEASE)
                map_mode = texture_prov;
            if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS && glfwGetKey(window, GLFW_KEY_S) == GLFW_RELEASE)
                map_mode = texture_regi;
            if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS && glfwGetKey(window, GLFW_KEY_D) == GLFW_RELEASE)
                map_mode = texture_terr;
            if (glfwGetKey(window, GLFW_KEY_F) == GLFW_PRESS && glfwGetKey(window, GLFW_KEY_F) == GLFW_RELEASE)
                map_mode = texture_hm;
            // Zoom
            if (glfwGetKey(window, GLFW_KEY_EQUAL) == GLFW_PRESS && glfwGetKey(window, GLFW_KEY_EQUAL) == GLFW_RELEASE)
                game.tick();
            if (glfwGetKey(window, GLFW_KEY_MINUS) == GLFW_PRESS && glfwGetKey(window, GLFW_KEY_MINUS) == GLFW_RELEASE)
                game.tick();
        }
        // Mouse
        {
            // Left Click
            if (glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_LEFT) == GLFW_PRESS && glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_LEFT) == GLFW_RELEASE)
            {
                // Scale cursor from window to image
                int width, height, x_pix, y_pix, index;
                std::vector<int> col = { 0,0,0 };
                std::vector<int> col_t = { 0,0,0 }, col_r = { 0,0,0 }, col_p = { 0,0,0 };
                double xpos, ypos;
                glfwGetWindowSize(window, &width, &height);
                glfwGetCursorPos(window, &xpos, &ypos);
                // Evaluate other objects at position (YTI)
                x_pix = (int)(xpos * tile_width / width);
                y_pix = (int)(ypos * tile_height / height);
                index = (x_pix + tile_width * y_pix) * tile_channels; // Calculates pixel position in array

                // BMP territory -> region -> province
                col[0] = (int)territory_pixels[index]; col[1] = (int)territory_pixels[index + 1]; col[2] = (int)territory_pixels[index + 2];
                if (col[0] == 0 and col[1] == 0 and col[2] == 255) { return; } // Exit if sea tile is selected (Other options YTI)
                // Find territory and search children if necassary
                for (int i = 0; i < game.territories.size(); i++)
                {
                    Territory territory = game.territories[i];
                    col_t = territory.colour; // Gets colour of territory
                    if (col[0] == col_t[0] and col[1] == col_t[1] and col[2] == col_t[2])
                    {
                        col[0] = (int)region_pixels[index]; col[1] = (int)region_pixels[index + 1]; col[2] = (int)region_pixels[index + 2];
                        std::cout << "Territory = " << territory.name << std::endl;
                        for (int j = 0; j < territory.children.size(); j++)
                        {
                            Region* region = territory.children[j];
                            col_r = region->colour; // Gets colour of the matching territories child region
                            if (col[0] == col_r[0] and col[1] == col_r[1] and col[2] == col_r[2])
                            {
                                col[0] = (int)province_pixels[index]; col[1] = (int)province_pixels[index + 1]; col[2] = (int)province_pixels[index + 2];
                                std::cout << "Region = " << region->name << std::endl;
                                for (int k = 0; k < region->children.size(); k++)
                                {
                                    Province* province = region->children[k];
                                    col_p = province->colour; // Gets colour of the matching regions child province
                                    if (col[0] == col_p[0] and col[1] == col_p[1] and col[2] == col_p[2])
                                    {
                                        std::cout << "Province = " << province->name << std::endl;
                                    }
                                }
                            }
                        }
                    }
                }
                // Check panels
                /*
                bool fired = false;
                for (int i = 0; i < panels.size(); i++)
                {
                    std::cout << "Search" << std::endl;
                    if (fired)
                    {
                        break;
                    }
                    fired = panels[i].pressed(xpos, ypos);
                }
                if (fired)
                {
                    std::cout << "Hit Panel" << std::endl;
                    std::cout << "Scale (" << xscale << " : " << yscale << std::endl;
                }
                else
                {
                    // Check armies

                    // Other
                }
                // Seperate for loop for armies
                */
            }

        }
    }
}

void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
    // make sure the viewport matches the new window dimensions; note that width and 
    // height will be significantly larger than specified on retina displays.
    glViewport(0, 0, width, height);
    // Update panels with new window dimensions
}
float* coordinateTransform(float vertices[])
{
    // -1.0f - 1.0f to 0.0f - 1.0f
    float left, bottom, width, height;
    left = (vertices[16] + 1) / 2;
    bottom = (vertices[17] + 1) / 2;
    width = (vertices[0] + 1) / 2 - left;
    height = (vertices[1] + 1) / 2 - bottom;
    float v[4] = { left, bottom, width, height };
    return v;
}