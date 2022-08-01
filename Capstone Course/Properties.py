from SimulationObject import SimulationObject

class Property(SimulationObject):
    """ Products of animals that cannot be interacted with but give information to other animals about the animal """
    def __init__(self, data, animal):
        super().__init__(data)
        self.animal = animal

    def get_animal(self):
        """ Returns what animal is connected with the property """
        return self.animal

    def destroy(self):
        """ Deletes all references to the property """
        self.get_animal().remove_track(self)
        self.get_tile().remove_sim_object(self)
        del self

class Tracks(Property):
    """ Animals produce Tracks that give a strength in the tile and direction it has moved to. """
    def __init__(self, data, animal, direction, strength):
        super().__init__(data, animal)
        self.direction = direction
        self.start_strength = strength
        self.strength = strength

    def __str__(self) -> str:
        """ Returns Tracks and it's animals name and information """
        return "{} of {}".format(self.get_name(), self.get_animal())

    def get_start_strength(self) -> int:
        """ Returns the starting strength of the Tracks """
        return self.start_strength
     
    def get_direction(self) -> int:
        """ Returns the direction the Tracks are facing """
        return self.direction

    def get_strength(self) -> int:
        """ Returns the strength of the Tracks """
        return self.strength

    def get_max_tracks(self) -> int:
        """ Returns the max amount of Tracks that can be in the environment at one time which is used for the observation space """
        max_tracks =  (self.start_strength + 1) * self.get_animal_total()   # + 1 included because properties are ticked after animals
        return max_tracks

    def tick(self) -> None:
        """ Decreases the strength and detectability as time passes until the Tracks reach zero strength which is when it is destroyed """
        self.strength -= 1
        self.detectable -= 10
        if self.strength == 0:
            self.destroy()

    def get_info(self) -> list:
        """ Returns all of the info of the Tracks """
        obj_id = int(self.get_obj_id())   
        tree_id = self.get_id()
        detectability = self.get_detectability()
        direction = self.get_direction()
        strength = self.get_strength()
        animal = self.get_animal().get_name()
        if animal == "Agent":
            animal_type = 0
        elif animal == "StationaryPredator": 
            animal_type = 1
        elif animal == "RandomPredator":
            animal_type = 2
        elif animal == "PatrolPredator":
            animal_type = 3

        return [obj_id, tree_id, detectability, direction, strength, animal_type]
