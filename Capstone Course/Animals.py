import numpy as np
import uuid

from SimulationObject import SimulationObject
from Resources import Corpse
from Properties import Tracks

class Animal(SimulationObject):
    """ An Animal is a SimObject that has health and is able to move from one Tile to another """
    def __init__(self, data, health, attack, diet, hunger, thirst, corpse_info, tracks_info):
        super().__init__(data)
        self.alive = True
        self.max_health, self.health = health, health
        self.attack = attack
        self.diet = diet
        self.max_hunger, self.hunger = hunger, hunger
        self.max_thirst, self.thirst = thirst, thirst
        self.turn, self.kills = 0, 0
        # Dependent object information
        self.corpse, self.tracks = None, []
        self.corpse_info, self.tracks_info = corpse_info, tracks_info

    def get_alive(self) -> bool:
        """ Returns if the Animal is alive """
        return self.alive
    
    def get_max_health(self) -> int:
        """ Returns the maximum health of the Animal """
        return self.max_health

    def get_health(self) -> int:
        """ Returns the current health of the Animal """
        return self.health
    
    def get_attack(self) -> int:
        """ Returns the attack of the Animal """
        return self.attack
    
    def get_diet(self) -> list[str]:
        """ Returns a list of the food the Animal can consume """
        return self.diet

    def get_max_hunger(self) -> int:
        """ Returns the maximum hunger the Animal can have """
        return self.max_hunger

    def get_hunger(self) -> int:
        """ Returns the current hunger of the Animal """
        return self.hunger
    
    def get_max_thirst(self) -> int:
        """ Returns the maximum thirst the Animal can have """
        return self.max_thirst

    def get_thirst(self) -> int:
        """ Returns the current thirst of the Animal """
        return self.thirst

    def get_turn(self) -> int:
        """ Returns the last turn the Animal acted """
        return self.turn

    def get_kills(self) -> int:
        """ Returns the current kills of the Animal """
        return self.kills

    def get_corpse(self) -> Corpse:
        """ Returns the corpse of the animal """
        return self.corpse

    def get_tracks(self) -> list[Tracks]:
        """ Returns the tracks of the animal """
        return self.tracks

    def get_corpse_info(self) -> list:
        """ Returns the obj_id and parameters of the Corpse SimObj """
        return self.corpse_info

    def get_tracks_info(self) -> list:
        """ Returns the obj_id and parameters of the Tracks SimObj """
        return self.tracks_info

    def create_track(self, direction) -> None:
        """ Creates a track on the animals tile """
        obj_id, t_param = self.get_tracks_info()[0], self.get_tracks_info()[1]
        track = Tracks([3, obj_id, uuid.uuid4(), self.get_tile(), self.random, self.logging, t_param["detectability"]], self, direction, t_param["strength"])
        self.get_tile().add_sim_object(track)
        self.tracks.append(track)

    def remove_track(self, track):
        """ Removes the animals Track from its knowledge """
        self.tracks.remove(track)

    def set_tile(self, tile):
        """ Changes the tile an animal is on """
        self.tile.remove_sim_object(self)
        self.tile = tile
        if tile != None:
            self.tile.add_sim_object(self)
    
    def alter_health(self, change) -> None:
        """ Alters the health of the Animal by the given value """
        if self.health + change < 1:
            self.health = 0
            self.die()
        elif self.health + change > self.get_max_health():
            self.health = self.get_max_health()
        else:
            self.health += change

    def alter_hunger(self, change) -> None:
        """ Alters the hunger of the Animal by the given value """
        if self.hunger + change < 1:
            self.hunger = 0
            self.alter_health(-1)
        # An animal has eaten and is full
        elif self.hunger + change > self.get_max_hunger():
            self.hunger = self.get_max_hunger()
        else:
            self.hunger += change

    def alter_thirst(self, change) -> None:
        """ Alters the thirst of the Animal by the given value """
        if self.thirst + change < 1:
            self.thirst = 0
            self.alter_health(-1)
        elif self.thirst + change > self.get_max_thirst():
            self.thirst = self.get_max_thirst()
        else:
            self.thirst += change

    def had_turn(self) -> None:
        """ Increment the turn the animal last acted on """
        self.turn += 1

    def killed(self) -> None:
        """ Increment the kill count of the animal """
        self.kills += 1

    def find_tracks(self) -> list:
        """ Returns a list of tracks detected within an animal's tile """
        tracks = []
        for property in self.get_tile().get_properties():
            if str(property.get_name()) == "Tracks" and property.is_detected():
                tracks.append(property)
        return tracks

    def move(self, direction) -> None:
        """ Alters the Animals current Tile to another based on the given direction """
        if not self.get_alive() or direction == 0:
            return
        next_tile = self.tile.get_neighbours()[direction-1]
        if (next_tile != None) and (next_tile.get_traverse() == True):
            self.create_track(direction)
            self.set_tile(next_tile)

    def act(self, action, target_obj_id, target_id) -> None:
        """ The Animal tries to perform an action (Nothing, consume, hide, or attack) on a specific SimObj """
        if action == 0: 
            return
        tile = self.get_tile()
        obj = tile.get_sim_object(target_obj_id, target_id)
        if obj != None:
            if action == 1:
                self.consume(obj)
            elif action == 2:
                obj.hide(self)
            elif action == 3:
                self.attack_animal(obj)
        else:
            self.log("Invalid target of {} at {}".format((target_obj_id, target_id), tile.get_position()))
            
    def consume(self, food) -> None:
        """ The Animal consumes a portion of the given food restoring itself """
        if food.get_group() in self.get_diet():
            self.log("{} consumed {} for {} nutrition".format(self, food, food.get_nutrition()))
            if food.get_group() == "Water":
                self.alter_thirst(food.consumed())
            else:
                self.alter_hunger(food.consumed())

    def attack_animal(self, target) -> None:
        """ Attacks the target Animal for variable damage """
        damage = self.get_attack() + self.rng(0, 3)
        self.log("{} attacks {}, dealing {} points of damage".format(self, target, damage))
        target.alter_health(-damage)
        if target.get_alive() == False:
            self.killed()
                
    def die(self) -> None:
        """ Sets the Animal as dead and replaces itself on it's Tile with a Corpse """
        if self.get_alive():
            self.alive = False
            tile = self.get_tile()
            corpse_obj_id, c_param = self.get_corpse_info()[0], self.get_corpse_info()[1]
            self.corpse = Corpse([2, corpse_obj_id, uuid.uuid4(), self.get_tile(), self.random, self.logging, 
                                  c_param["detectability"]], c_param["quantity"], c_param["nutrition"], c_param["decay"], self)
            tile.remove_sim_object(self)
            tile.add_sim_object(self.get_corpse())
            self.log("{} died on {} with {} hunger and {} thirst".format(self, self.get_tile().get_position(), self.get_hunger(), self.get_thirst()))
        

class Predator(Animal):
    """ A Predator is an Animal that hunts down Agents """
    def __init__(self, data, health, attack, corpse_info, tracks_info):
        super().__init__(data, health, attack, ["Meat", "Water"], 0, 0, corpse_info, tracks_info)

    def find_weakest_agent(self):
        """ Returns the weakest detected agent in the surrounding tiles, and which direction it is in """
        weakest, direction = None, None
        reachable = [self.get_tile()] + self.get_tile().get_neighbours()
        for i in range(len(reachable)):
            tile = reachable[i]
            if tile != None:
                for animal in tile.get_animals():
                    if animal.get_name() == "Agent" and animal.get_alive() and animal.is_detected():
                        self.log("{} at {} has spotted {} at {}".format(self, self.get_tile().get_position(), animal, tile.get_position()))
                        if weakest == None or animal.get_health() < weakest.get_health():
                            weakest = animal
                            direction = i
                    elif animal.get_name() == "Agent" and animal.get_alive():
                        self.log("{} at {} didn't detect {} at {}".format(self, self.get_tile().get_position(), animal, tile.get_position()))
        return weakest, direction

    def movement(self) -> None:
        """ The Predator will undergo implemented subclass movement """
        raise NotImplementedError

    def grief(self) -> None:
        """ Predators will consume a Corpse if it is present in the same Tile with no detected Agents """
        eligible_food = []
        for resource in self.get_tile().get_resources():
            if resource.get_name() == "Corpse" and resource.is_detected():
                if resource.get_group() == "Meat":
                    eligible_food.append(resource)
        if len(eligible_food) > 0:
            index = self.rng(0, len(eligible_food))
            self.act(1, eligible_food[index].get_obj_id(), eligible_food[index].get_id())

    def tick(self) -> None:
        """ Searches the nearby Tiles for the weakest Agent to attack, or undergoes subclass movement and attempts to grief present Corpses"""
        if not self.get_alive():
            return
        weakest, move = self.find_weakest_agent()
        if move != None:
            self.move(move)
            self.act(3, weakest.get_obj_id(), weakest.get_id())
        else:
            self.movement()
            self.grief()
        self.had_turn()

    def get_info(self) -> list:
        """ Returns all of the info the Predators has """
        obj_id = self.get_obj_id()   
        predator_id = self.get_id()
        detectability = self.get_detectability()
        alive = int(self.get_alive())
        health = self.get_health()
        attack = self.get_attack()

        if isinstance(self, StationaryPredator): 
            predator_type = 0
        elif isinstance(self, RandomPredator):
            predator_type = 1
        elif isinstance(self, PatrolPredator):
            predator_type = 2

        return [obj_id, predator_id, detectability, alive, health, attack, predator_type]

class StationaryPredator(Predator):
    """ A StationaryPredator is a Predator that doesn't move unless it notices an Agent """
    def __init__(self, data, health, attack, corpse_info, tracks_info):
        super().__init__(data, health, attack, corpse_info, tracks_info)
    
    def movement(self) -> None:
        """ Stationary Predators do not move without stimulus """
        self.move(0)

class RandomPredator(Predator):
    """ A RandomPredator is a Predator that moves randomly unless it detects an Agent's Tracks, which it then follows """
    def __init__(self, data, health, attack, corpse_info, tracks_info):
        super().__init__(data, health, attack, corpse_info, tracks_info)

    def movement(self) -> None:
        """ Random Predators randomly move unless it detects an Agents Tracks """
        tracks = self.find_tracks()
        for track in tracks:
            if str(track.get_animal().get_name()) == "Agent":
                self.log("{} followed {} ({}, {})".format(self, track.get_animal().get_name(), track.get_animal().get_obj_id(), track.get_animal().get_id()))
                self.move(track.get_direction())
                return            
        action = self.rng(0, 7)
        self.move(action)

class PatrolPredator(Predator):
    """ A PatrolPredator is a Predator that Takes a tile object as it's origin (starting position)
        and a tile object as it's destination (final position) and moves between them """
    def __init__(self, data, health, attack, destination, corpse_info, tracks_info):
        super().__init__(data, health, attack, corpse_info, tracks_info)
        self.origin = self.get_tile()
        self.destination = destination
        #self.log("Patrol Pred route:" + str(self.origin.get_position()) + "to" + str(self.destination.get_position()))

    def axial_distance(self, start_x, start_y, dest_x, dest_y):
        """ Calculates distance between 2 hextiles (More accurate than manhatten distance with hexes) """
        return ((abs(start_x - dest_x) + abs(start_x + start_y - dest_x - dest_y)+ abs(start_y - dest_y)) / 2)

    def movement(self) -> None:
        """ The PatrolPredator looks at which of its neighbours are closest to the destination and moves there """
        tile = self.get_tile()
        # If predator made it to it's destination, swap its origin with its destination (to move back and forth)
        if (tile == self.destination):
            self.destination, self.origin = self.origin, self.destination
            
        neighbours = tile.get_neighbours()
        dest_position = self.destination.get_position()
        dest_x, dest_y = dest_position[0], dest_position[1]
        
        # Neighbour score calculated like manhatten distance (x offset + y offset)
        neighbour_scores = []  # each index corresponds to a neighbour tile. Each score is a distance heuristic (lower value = closer to destination)
        for neighbour in neighbours:  # calculates and appends scores in order up_left, up_right, left, right, down_left, down_right

            # If this neighbour doesn't exist or is non-traversable, its score defaults to None
            if (neighbour is None) or (neighbour.get_traverse() == False):
                neighbour_scores.append(None)

            else: 
                neighbour_position = neighbour.get_position()
                neighbour_x, neighbour_y = neighbour_position[0], neighbour_position[1]
                score = self.axial_distance(neighbour_x, neighbour_y, dest_x, dest_y)
                neighbour_scores.append(score)

        best_score = min(score for score in neighbour_scores if score is not None)
        best_neighbours = []
        for i in range(len(neighbour_scores)):
            if neighbour_scores[i] == best_score:
                # Collects all tiles with the best score. Usually there are ties for best score.
                best_neighbours.append(neighbours[i])

        # Randomly pick from among the best scoring neighbours
        chosen_neighbour = best_neighbours[self.rng(0, len(best_neighbours))]

        # The index (+1 to offset 0, as direction 0 means stay) of each neighbour, corresponds with the direction to the neighbour. None scores are not considered.
        direction = neighbours.index(chosen_neighbour) + 1 
        self.move(direction)  # i.e up_left = neighbour_scores[0] = direction 1     &     up_right = neighbour_scores[1] = direction 2
        #self.log(f"Patrol Pred moved from ({tile.get_position()[0]}, {tile.get_position()[1]}) to ({self.get_tile().get_position()[0]}, {self.get_tile().get_position()[1]})")


class Agent(Animal):
    """ An Agent is an Animal which is controlled externally and has a main goal of surviving for as long as possible """
    def __init__(self, data, health, attack, hunger, thirst, corpse_info, tracks_info):
        super().__init__(data, health, attack, ["Fruit", "Meat", "Water"], hunger, thirst, corpse_info, tracks_info)
        self.score = 0
        self.in_tree = False

    def get_score(self) -> int:
        """ Returns the Agents current score """
        return self.score
      
    def add_score(self, score) -> None:
        """ Adds the score to the Agents current score """
        self.score += score

    def is_in_tree(self) -> bool:
        """ Returns True if the agent is currently in a Tree for the state space"""
        return self.in_tree

    def set_tree(self, bool) -> None:
        """ Sets whether or not an agent is in a Tree for the state space"""
        self.in_tree = bool

    def tick(self) -> None:
        """ Alters the Agent if it is alive by changing its hunger/thirst as well as regenerating """
        if self.get_alive(): 
            self.alter_hunger(-1)
            self.alter_thirst(-1)
            if self.get_hunger() != 0 and self.get_thirst() != 0:
                self.alter_health(1)
            self.had_turn()

    def get_info(self) -> list:
        """ Returns all of the info the Agent has """
        obj_id = self.get_obj_id()   
        agent_id = self.get_id()
        detectability = self.get_detectability()
        alive = int(self.get_alive())
        health = self.get_health()
        attack = self.get_attack()
        hunger = self.get_hunger()
        thirst = self.get_thirst()
        in_tree = int(self.is_in_tree())

        return [obj_id, agent_id, detectability, alive, health, attack, hunger, thirst, in_tree]