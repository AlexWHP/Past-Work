import gym
from gym import spaces, utils
import numpy as np

from Tile import Tile
from Animals import Agent, Tracks, PatrolPredator, RandomPredator, StationaryPredator
from Resources import BerryBush, Tree, Water, Corpse

class WorldEnv(gym.Env):
    """ Hexgrid OpenAI gym environment """
    def __init__(self, env_parameters, obj_counts, obj_parameters, log=None):
        # Actions that can be taken - stay, up left, up right, left, right, down left, down right
        self.action_space = spaces.Discrete(7)

        # Defining environment parameters and RNG
        self.grid_width = env_parameters["width"]
        self.grid_height = env_parameters["height"]
        self.seed = env_parameters["seed"]
        self.random, x = utils.seeding.np_random(env_parameters["seed"])
        self.max_turn = env_parameters["max_turns"]
        self.non_trav_chance = env_parameters["non_trav_chance"]

        # Defining the number of Simulation Objects and parameters
        self.obj_counts = obj_counts
        self.obj_parameters = obj_parameters

        # Stores the logging object within the environment
        self.logging = log

    def step(self, agent_turn) -> dict:
        """ Performs an agents action, progresses the environment if all agents have moved, and returns the new state """
        agent_id, movement = agent_turn[0], agent_turn[1]
        action, target_obj_id, target_id = agent_turn[2], agent_turn[3], agent_turn[4]
        agent = self.get_agent(agent_id)

        # Perform agent actions and track which have acted
        if agent_id not in self.get_acted_agents():
            if agent.get_alive():
                agent.move(movement)
                agent.act(action, target_obj_id, target_id)
                agent.tick()
            self.agent_acted(agent_id)

        # Reward calculation (Survival time)
        reward = 0
        if agent.get_alive():
            reward += 1

        # Progresses the environment, once all agents have acted, and checks if done
        done = False
        if len(self.get_acted_agents()) == len(self.get_agents()):
            self.tick()
            if self.get_turn() > self.get_max_turn() or not any([agent.get_alive() for agent in self.get_agents()]):
                done = True

        # Retrieves information and state to be returned
        info = {}
        state = self.get_state()
        return state, reward, done, info

    def render(self):
        """ To be implemented by subclasses to visualise the environment """
        raise NotImplementedError

    def reset(self) -> dict:
        """ Initialises a new episode and returns the new state of the environment """
        self.acted_agents = []
        self.turn = 1
        self.create_hex_grid()
        self.add_tile_neighbours()
        self.traversability()
        self.populate_hex_grid()

        return self.get_state()

    def create_hex_grid(self) -> None:
        """ Creates the hex-grid of grid_width and grid_height with traversability """
        self.tiles = []
        # Checks if all tiles are traversable
        trav = (self.get_non_trav_chance() == 0)
        for y in range(self.get_grid_height()):
            self.tiles.append([])
            for x in range(self.get_grid_width()):
                tile_num = y * self.get_grid_height() + x
                new_tile = Tile(x, y, tile_num, trav)
                self.tiles[y].append(new_tile)

    def coords_real(self, x, y) -> bool:
        """ Returns True if the coordinates are within the environments bounds """
        if (x < 0) or (y < 0) or (x >= self.get_grid_width()) or (y >= self.get_grid_height()):
            return False
        else:
            return True
     
    def add_tile_neighbours(self):
        """ Iterates through all tiles and add their neighbours to them """
        for y in range(self.get_grid_height()):
            for x in range(self.get_grid_width()):
                # Getting and defining necessary values
                main_tile = self.get_tile(x, y)
                main_x, main_y = main_tile.get_position()
                ul_tile, ur_tile, l_tile, r_tile, dl_tile, dr_tile = None, None, None, None, None, None

                # coords of up_left neighbour
                if main_tile.y % 2 == 0:
                    up_left_x, up_left_y = main_x - 1, main_y - 1
                else:
                    up_left_x, up_left_y = main_x, main_y - 1
                if self.coords_real(up_left_x, up_left_y):
                    ul_tile = self.get_tile(up_left_x, up_left_y)

                # coords of up_right neighbour
                if main_tile.y % 2 == 0:
                    up_right_x, up_right_y = main_x, main_y - 1
                else:
                    up_right_x, up_right_y = main_x + 1, main_y - 1
                if self.coords_real(up_right_x, up_right_y):
                    ur_tile = self.get_tile(up_right_x, up_right_y)

                # coordinates of left neighbour
                left_x, left_y = main_x - 1, main_y
                if self.coords_real(left_x, left_y):
                    l_tile = self.get_tile(left_x, left_y)

                # coords of right neighbour
                right_x, right_y = main_x + 1, main_y
                if self.coords_real(right_x, right_y):
                    r_tile = self.get_tile(right_x, right_y)

                # coords of down_left neighbour
                if main_tile.y % 2 == 0:
                    down_left_x, down_left_y = main_x - 1, main_y + 1
                else:
                    down_left_x, down_left_y = main_x, main_y + 1
                if self.coords_real(down_left_x, down_left_y):
                    dl_tile = self.get_tile(down_left_x, down_left_y)

                # coords of down_right neighbour
                if main_tile.y % 2 == 0:
                    down_right_x, down_right_y = main_x, main_y + 1
                else:
                    down_right_x, down_right_y = main_x + 1, main_y + 1
                if self.coords_real(down_right_x, down_right_y):
                    dr_tile = self.get_tile(down_right_x, down_right_y)

                main_tile.set_neighbours([ul_tile, ur_tile, l_tile, r_tile, dl_tile, dr_tile])

    def traversability(self) -> None:
        """ Algorithm for creating connected traversable tiles by randomly selecting unique adjacent Tiles that are non-traversable """
        if self.get_non_trav_chance() != 0:
            visited = [[False] * self.get_grid_width() for i in range(self.get_grid_height())]
            trav_count = 0
            eligible = []
            x, y = self.get_grid_width() // 2, self.get_grid_height() // 2
            tile = self.get_tile(x, y)
            visited[y][x] = True
            trav_max = self.get_grid_height() * self.get_grid_width() * (100-self.get_non_trav_chance()) / 100
            
            while trav_count < trav_max:
                tile.set_traverse(True)
                trav_count += 1
                # Finds all valid and not traversable neighbouring tiles
                neighbours = tile.get_neighbours()
                for neighbour in neighbours:
                    if neighbour != None and neighbour.get_traverse() == False:
                        x, y = neighbour.get_position()
                        if not visited[y][x]:
                            visited[y][x] = True
                            eligible.append(neighbour)

                # Selects a random Tile from eligible
                if len(eligible) > 0:
                    num = self.rng(0, len(eligible))
                    tile = eligible.pop(num)
                else:
                    break

    def populate_hex_grid(self) -> None:
        """ Generates the Simulation Objects in the environment """
        self.agents, self.predators = [], []
        self.berry_bushes, self.water_sources, self.trees = [], [], []

        # Agent, StationaryPredator, RandomPredator, PatrolPredator, BerryBush, Water, Tree
        obj_counts = self.get_obj_counts()
        obj_paramteters = self.get_obj_parameters()
        # Obj_id and parameters to be used for Corpse and Tracks within Animals
        corpse_info = [len(obj_counts), obj_paramteters["corpse"]]
        tracks_info = [len(obj_counts) + 1, obj_paramteters["tracks"]]

        # Generates all animals within the environment (Category = 1)
        # Agents
        obj_id, id = 0, 0
        agent_p = obj_paramteters["agent"]
        while id < obj_counts[obj_id]:
            x, y = self.random_pos()
            tile = self.get_tile(x, y)
            if tile.get_traverse() == True:
                agent = Agent([1, obj_id, id, tile, self.random, self.logging, agent_p["detectability"]], agent_p["health"],
                             agent_p["attack"], agent_p["hunger"], agent_p["thirst"], corpse_info, tracks_info)
                self.agents.append(agent)
                tile.add_sim_object(agent)
                id += 1
        # Stationary Predators
        obj_id, id = obj_id + 1, 0
        spred_p = obj_paramteters["spredator"]
        while id < obj_counts[obj_id]:
            x, y = self.random_pos()
            tile = self.get_tile(x, y)
            if tile.get_traverse() == True:
                pred = StationaryPredator([1, obj_id, id, tile, self.random, self.logging, spred_p["detectability"]],
                                          spred_p["health"], spred_p["attack"], corpse_info, tracks_info)
                self.predators.append(pred)
                tile.add_sim_object(pred)
                id += 1
        # Random Predators
        obj_id, id = obj_id + 1, 0
        rpred_p = obj_paramteters["rpredator"]
        while id < obj_counts[obj_id]:
            x, y = self.random_pos()
            tile = self.get_tile(x, y)
            if tile.get_traverse() == True:
                pred = RandomPredator([1, obj_id, id, tile, self.random, self.logging, rpred_p["detectability"]],
                                      rpred_p["health"], rpred_p["attack"], corpse_info, tracks_info)
                self.predators.append(pred)
                tile.add_sim_object(pred)
                id += 1
        # Patrol Predators
        obj_id, id = obj_id + 1, 0
        ppred_p = obj_paramteters["ppredator"]
        while id < obj_counts[obj_id]:
            x, y = self.random_pos()
            tile = self.get_tile(x, y)
            x, y = self.random_pos()
            destination = self.get_tile(x, y)
            if tile.get_traverse() == True and destination.get_traverse() == True and tile != destination:
                pred = PatrolPredator([1, obj_id, id, tile, self.random, self.logging, ppred_p["detectability"]],
                                      ppred_p["health"], ppred_p["attack"], destination, corpse_info, tracks_info)
                self.predators.append(pred)
                tile.add_sim_object(pred)
                id += 1

        # Generates all resources within the environment (Category = 2)
        # Berry Bushes
        obj_id, id = obj_id + 1, 0
        bberry_p = obj_paramteters["bbush"]
        while id < obj_counts[obj_id]:
            x, y = self.random_pos()
            tile = self.get_tile(x, y)
            if tile.get_traverse() == True:
                berry = BerryBush([2, obj_id, id, tile, self.random, self.logging, bberry_p["detectability"]],
                                  bberry_p["quantity"], bberry_p["nutrition"], bberry_p["regen"])
                self.berry_bushes.append(berry)
                tile.add_sim_object(berry)
                id += 1
        # Water
        obj_id, id = obj_id + 1, 0
        water_p = obj_paramteters["water"]
        while id < obj_counts[obj_id]:
            x, y = self.random_pos()
            tile = self.get_tile(x, y)
            if tile.get_traverse() is True:
                water = Water([2, obj_id, id, tile, self.random, self.logging, water_p["detectability"]], water_p["quantity"],
                              water_p["nutrition"])
                self.water_sources.append(water)
                tile.add_sim_object(water)
                id += 1
        # Trees
        obj_id, id = obj_id + 1, 0
        tree_p = obj_paramteters["tree"]
        while id < obj_counts[obj_id]:
            x, y = self.random_pos()
            tile = self.get_tile(x, y)
            if tile.get_traverse() == True:
                tree = Tree([2, obj_id, id, tile, self.random, self.logging, tree_p["detectability"]], tree_p["camouflage"], tree_p["limit"])
                self.trees.append(tree)
                tile.add_sim_object(tree)
                id += 1

    def get_state(self) -> dict:
        """ Returns information on every SimObject and Tile in the environment """
        state = {}

        # Adding agent info
        for agent in self.get_agents():
            agent_info = agent.get_info()
            tile_num = agent.get_tile().get_tile_num()
            agent_info.insert(2, tile_num)

            if agent.get_id() in self.get_acted_agents():
                had_turn = 0
            else:
                had_turn = 1
            agent_info.insert(-1, had_turn)
            state[agent.get_name() + str(agent.get_id())] = agent_info

        # Adding predator info
        for predator in self.get_predators():
            pred_info = predator.get_info()
            tile_num = predator.get_tile().get_tile_num()
            pred_info.insert(2, tile_num)

            state[predator.get_name() + str(predator.get_id())] = pred_info
        
        # Adding bush info
        for bush in self.get_berry_bushes():
            bush_info = bush.get_info()
            tile_num = bush.get_tile().get_tile_num()
            bush_info.insert(2, tile_num)

            state[bush.get_name() + str(bush.get_id())] = bush_info
        
        # Adding water info
        for water in self.get_water_sources():
            water_info = water.get_info()
            tile_num = water.get_tile().get_tile_num()
            water_info.insert(2, tile_num)

            state[water.get_name() + str(water.get_id())] = water_info
        
        # Adding tree info
        for tree in self.get_trees():
            tree_info = tree.get_info()
            tile_num = tree.get_tile().get_tile_num()
            tree_info.insert(2, tile_num)

            state[tree.get_name() + str(tree.get_id())] = tree_info
        
        # Adding corpse info
        corpses = self.get_corpses()
        for i in range(self.get_animal_total()):
            if i < len(corpses):
                corpse = corpses[i]
                corpse_info = corpse.get_info()
                tile_num = corpse.get_tile().get_tile_num()
                corpse_info.insert(2, tile_num)

                state[corpse.get_name() + str(i)] = corpse_info
            else:
                # Acts as a placeholder for later corpse objects, so that the state_space doesn't change size mid simulation
                state["Corpse" + str(i)] = [0, 0, 0, 0, 0, 0, 0]

        # Adding track info
        tracks_data = self.get_obj_parameters()["tracks"]
        start_strength = tracks_data["strength"]
        max_tracks = (start_strength + 1) * self.get_animal_total()
        tracks = self.get_tracks()
        for i in range(max_tracks):
            if i < len(tracks):
                track = tracks[i]
                track_info = track.get_info()
                tile_num = track.get_tile().get_tile_num()
                track_info.insert(2, tile_num)

                state[track.get_name() + str(i)] = track_info
            else:
                # Acts as a placeholder for later track objects, so that the state_space doesn't change size mid simulation
                state["Tracks" + str(i)] = [0, 0, 0, 0, 0, 0]

        # Adding tile info
        tile_num = 0
        for x in range(self.get_grid_width()):
            for y in range(self.get_grid_height()):
                tile = self.get_tile(x, y)
                traversable = int(tile.get_traverse())
                state["tile" + str(tile_num)] = [tile_num, traversable]
                tile_num += 1

        return state

    def generate_state_space(self) -> dict:
        """ Creates a state space dependent on the initialisation parameters """
        state_space = spaces.Dict({})  # represents all possible states that can be returned by step() method
        total_tiles = self.get_grid_height() * self.get_grid_width()

        # Adding agents to state_space dict
        for agent in self.get_agents():
            state_space[agent.get_name() + str(agent.get_id())] = spaces.MultiDiscrete(
                [9, len(self.get_agents()), total_tiles, 100, 2, agent.get_max_health(), agent.get_attack(),
                 agent.get_max_hunger(), agent.get_max_thirst(), 2, 2])
            # obj_id, id, tile number, detectability %, alive, health, attack, hunger, thirst, had turn, in tree

        # Adding predators to state_space dict
        for predator in self.get_predators():
            state_space[predator.get_name() + str(predator.get_id())] = spaces.MultiDiscrete(
                [9, len(self.get_predators()), total_tiles, 100, 2, predator.get_max_health(), predator.get_attack(),
                 3])
            # obj_id, id, tile number, detectability %, alive, health, attack, predator type (stationary or random or patrol)

        # Adding bushes to state_space dict
        for bush in self.get_berry_bushes():
            state_space[bush.get_name() + str(bush.get_id())] = spaces.MultiDiscrete(
                [9, len(self.get_berry_bushes()), total_tiles, 100, bush.get_quantity(), bush.get_nutrition(), 3,
                 bush.get_regen()])
            # obj_id, id, tile number, detectability, quantity, nutrition, food type (fruit or meat or water), regen chance %

        # Adding corpses to state_space dict  
        # Added slightly differently, as no corpses exist upon world creation
        corpse_data = self.get_obj_parameters()["corpse"]
        max_quantity = corpse_data["quantity"]
        max_nutrition = corpse_data["nutrition"]
        decay = corpse_data["decay"]
        max_corpses = self.get_animal_total()
        for i in range(max_corpses):

            state_space["Corpse" + str(i)] = spaces.MultiDiscrete(
                [9, max_corpses, total_tiles, 100, max_quantity, max_nutrition, decay, 3])
            # obj_id, id, tile number, detectability, quantity, nutrition, food type (fruit or meat or water), decay chance %

        # Adding water to state_space dict
        for water in self.get_water_sources():
            state_space[water.get_name() + str(water.get_id())] = spaces.MultiDiscrete(
                [9, len(self.get_water_sources()), total_tiles, 100, water.get_quantity(), water.get_nutrition(), 3])
            # obj_id, id, tile number, detectability, quantity, nutrition, food type (fruit or meat or water)

        # Adding tree to state_space dict
        for tree in self.get_trees():
            state_space[tree.get_name() + str(tree.get_id())] = spaces.MultiDiscrete(
                [9, len(self.get_trees()), total_tiles, 100, tree.get_limit(), tree.get_limit()])
            # obj_id, id, tile number, detectability, agent limit, current agents

        # Adding tracks to state_space dict
        # Added slightly differently, as no tracks exist upon world creation
        tracks_data = self.get_obj_parameters()["tracks"]
        start_strength = tracks_data["strength"]
        max_tracks = (start_strength + 1) * self.get_animal_total()
        for i in range(max_tracks):
            state_space["Tracks" + str(i)] = spaces.MultiDiscrete(
                [9, max_tracks, total_tiles, 100, 6, start_strength + 1, 4])
            # obj_id, id, tile number, detectability, direction, strength, animal type (agent, st_pred, ra_pred, pa_pred)

        # Tiles allocated numbers column by column, top to bottom
        tile_num = 0
        for x in range(self.get_grid_width()):
            for y in range(self.get_grid_height()):
                state_space["tile" + str(tile_num)] = spaces.MultiDiscrete(
                    [total_tiles, 2])  # tile number, traversability
                tile_num += 1
        return state_space

    def get_max_turn(self) -> int:
        """ Returns the maximum number of turns an episode will run for """
        return self.max_turn
    
    def get_turn(self) -> int:
        """ Returns the current turn an episode the environment is in """
        return self.turn

    def get_grid_width(self) -> int:
        """ Returns the width of the hex-grid """
        return self.grid_width

    def get_grid_height(self) -> int:
        """ Returns the height of the hex-grid """
        return self.grid_height

    def get_seed(self) -> int:
        """ Returns the seed used on initialisation of the environment """
        return self.seed

    def get_non_trav_chance(self) -> int:
        """ Returns the chance a Tile will not be traversable """
        return self.non_trav_chance
      
    def get_obj_counts(self) -> list[int, ...]: 
        """ Returns the list of Simulation Objects initially in the environment """
        return self.obj_counts

    def get_obj_parameters(self) -> dict:
        """ Returns the parameter info of all Simulation Objects """
        return self.obj_parameters

    def get_tile(self, *args) -> Tile:
        """ Overloaded funtion that returns a tile at either its coordinates in the array or out of the number of tiles """
        if len(args) == 1:
            tile_num = args[0]
            y = tile_num % self.get_grid_height()
            x = tile_num // self.get_grid_height()
            return self.tiles[y][x]
        elif len(args) == 2:
            x, y = args[0], args[1]
            return self.tiles[y][x]
    
    def get_tiles(self) -> list[[Tile, ...], ...]:
        """ Returns a 2D array of Tiles that the hexgrid is comprised of """
        return self.tiles

    def get_agent(self, id) -> Agent:
        """ Returns an agent based on its specific id """
        return self.agents[id]

    def get_agents(self) -> list[Agent]:
        """ Returns a list of all agents in the environment """
        return self.agents

    def get_predators(self)-> list[StationaryPredator, RandomPredator, PatrolPredator, ...]:
        """ Returns a list of all predators in the environment """
        return self.predators
      
    def get_berry_bushes(self) -> list[BerryBush]:
        """ Returns a list of all berry bushes in the environment """
        return  self.berry_bushes

    def get_corpses(self) -> list[Corpse]:
        """ Returns a list of all corpses in the environment """
        corpses = []
        for animal in self.get_predators() + self.get_agents():
            if not animal.get_alive():
                corpse = animal.get_corpse()
                if corpse.get_tile() != None:
                    corpses.append(corpse)
        return corpses

    def get_tracks(self) -> list[Tracks]:
        """ Returns a list of all tracks in the environment """
        tracks = []
        for animal in self.get_predators() + self.get_agents():
            tracks = tracks + animal.get_tracks()
        return tracks

    def get_trees(self) -> list[Tree]:
        """ Returns a list of all trees in the environment """
        return self.trees

    def get_water_sources(self) -> list[Water]:
        """ Returns a list of all water sources in the environment """
        return self.water_sources

    def get_acted_agents(self) -> list[int]:
        """ Returns a list of all agents that have already acted on the turn """
        return self.acted_agents

    def agent_acted(self, agent_id) -> None:
        """ Adds an agent to the list who have acted this turn """
        self.acted_agents.append(agent_id)
      
    def get_animal_total(self) -> int:
        """ Returns the total number of animals on initialisation """
        total = self.get_obj_counts()[0] + self.get_obj_counts()[1] + self.get_obj_counts()[2] + self.get_obj_counts()[3]
        return total

    def add_tracks(self, tracks) -> None:
        """ Appends a tracks elemobjectent to the environment """
        self.tracks.append(tracks)

    def remove_tracks(self, tracks) -> None:
        """ Removes a tracks object from the environment """
        self.tracks.remove(tracks)

    def add_corpse(self, corpse) -> None:
        """ Appends a corpse object to the environment """
        self.corpse.append(corpse)

    def remove_corpse(self, corpse) -> None:
        """ Removes a corpse object from the environment """
        self.corpses.remove(corpse)

    def rng(self, i, j) -> int:
        """ Returns a random value between two given values (i<=x<j) """
        if abs(i-j) <= 1:
            return i
        return self.random.integers(i, j)

    def random_pos(self):
        """ Returns a random coordinate (x, y) within the environments bounds """
        return self.rng(0, self.get_grid_width()), self.rng(0, self.get_grid_height())

    def log(self, to_log) -> None:
        """ Writes a string to the log file of the environment """
        self.logging.write_to_file(to_log)
                
    def tick(self):
        """ Steps the environment by ticking remaining animals and tiles """
        for predator in self.get_predators():
            predator.tick()
        for tile_row in self.get_tiles():
            for tile in tile_row:
                tile.tick()
        self.turn += 1
        self.acted_agents = []
