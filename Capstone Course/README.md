# Poly-Hex
Test environment for artificial consciousness. Template hex-grid world compatible with OpenAI gym. Created by Mystery Machine (Team 9).

#### Project Management Tool
[GitHub](https://github.com)

## Description
This program provides a simulated environment that can be used for experiments with artificial consciousness. The simulated environment reflects conditions from human evolutionary history by simulating survival, i.e., gathering food and avoiding predators. Multiple artificially intelligent agents at once can be used in the environment.

## Getting Started

### Dependencies
* A requirements.txt file is provided in the files:
  * cloudpickle 2.0.0
  * gym 0.23.1
  * gym-notices 0.0.6
  * numpy 1.22.3
  * pygame 2.1.2
* The program was developed on Windows
* Python language is used.

### Installing
* Download this program from the releases section
* or Download the files individually from GitHub
* or Download the .zip file if provided

### Executing program
1. Open the Main.py file.
2. Follow the instructions at the top of the Main.py file or those here
   1. Provide WorldEnv or WorldEnvRender with values.
   ```
   env_parameters = {
        "width":                30,
        "height":               30,
        "seed":                 1,
        "max_turns":            80,
        "non_trav_chance":      40
    }
   ```
   2. Provide obj_counts with values.
   ```
   # AGENT, SPREDATOR, RPREDATOR, PPREDATOR, BBUSH, WATER, TREE
   obj_counts = [20, 5, 5, 5, 30, 30, 30]
   ``` 
   3. Customise SimObj parameters
   ```
   obj_parameters = {
        "agent": {
            "detectability":    80,
            "health":           10,
            "attack":           1,
            "hunger":           20,
            "thirst":           20
        },
   ...
   ``` 
   4. Input these values into the rendering or regular environments
   ```
   env = WorldEnvRender(screen_width, screen_height, delay, env_parameters, obj_counts, obj_parameters, log)
   env = WorldEnv(env_parameters, obj_counts, obj_parameters, log)
   ```
### Usage examples
Example values for ```obj_counts```, ```obj_counts = [20, 1, 7, 1, 30, 30, 30]```.
The values are (from left to right):
* Agents
* Stationary Predators
* Random Predators
* Patrol Predators
* Berry Bushes
* Water
* Trees

Example values for ```env``` are set in env_parameters and are passed into ```env = WorldEnvRender(screen_width, screen_height, delay, env_parameters, obj_counts, obj_parameters, log)``` where the values are used in the WorldEnvRender function. Each of the parameters functionality is highlighted by the key to each of the values.

Parameters for Simulation Objects are also provided and passed to the envrionment through Main.py with adjustable values for all. Their functionality is stated within the keys of the dictionary with their values represented as values.

## Authors
Contributor names and GitHub links
* Alex Phillips ([@AlexWHP](https://github.com/AlexWHP))
* Barbora Sharrock ([@BSha259](https://github.com/BSha259))
* Darryn He ([@dhe077](https://github.com/dhe077))
* Kris Gemmell ([@KrisGemmell](https://github.com/KrisGemmell))
* Kyle Saifiti ([@ksaifiti](https://github.com/ksaifiti))
* Riley Irwin ([@RonkLonk](https://github.com/RonkLonk))

## Future Plans
* Letting artificial intelligence control the agents to test for artificial consciousness
* Visualiser could be extended to be interactable (Select tiles and output information)
* Tools
* Huts
* Any features that could add complexity to the environment for better testing of AI

## Acknowledgement
Inspiration, code snippets, etc.
* Dr Josh Ljubo Bensemann.
* Credit to [rbaltrusch](https://github.com/rbaltrusch/pygame_examples/blob/master/code/hexagonal_tiles/main.py) for the drawing functions for the visualiser. 
* [Building a Custom Environment for Deep Reinforcement Learning with OpenAI Gym and Python](https://youtu.be/bD6V3rcr_54)

