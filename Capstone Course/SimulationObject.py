class SimulationObject:
    """ All creatures and items are SimulationObjects. All SimObj possess an associated
        Tile object, id and detectability alongside appropriate accesors and mutators.
        Also has a pointer to the environment RNG stored within for variability"""
    def __init__(self, data):
        """ object_id, id, tile, random, detectable are core attributes of
            every object and are contained within data """
        self.obj_category = data[0]
        self.obj_id = data[1]
        self.id = data[2]
        self.tile = data[3]
        self.random = data[4]
        self.logging = data[5]
        self.detectable = data[6]
        self.default_detectable = data[6]

    def __str__(self) -> str:
        """ Returns the name of a SimObj and it's obj_id and id """
        return "{} ({}, {})".format(self.get_name(), self.get_obj_id(), self.get_id())

    def get_name(self) -> str:
        """ Returns the Class name as a string """
        return type(self).__name__

    def get_obj_category(self) -> int: 
        """ Returns the objects category value (animal, resource or property) """
        return self.obj_category

    def get_obj_id(self) -> int: 
        """ Returns the object id (Unique for subclass types) """
        return self.obj_id

    def get_id(self) -> int:
        """ Returns the objects id (Unique between the same subclass) """
        return self.id

    def get_tile(self):
        """ Returns the Tile object the SimObj is on """
        return self.tile

    def get_detectability(self) -> int:
        """ Returns the detectability of the SimObj """
        return self.detectable

    def get_default_detectability(self) -> int:
        """ Returns the immutable base detectability of the SimObj """
        return self.default_detectable

    def set_tile(self, tile) -> None:
        """ Re-assigns the Tile a SimObj is currently on """
        self.tile = tile

    def set_detectability(self, detectable) -> None:
        """ Changes a SimObj detectability to a given value """
        self.detectable = detectable
    
    def rng(self, i, j) -> int:
        """ Returns a random value between two given values (i<=x<j) """
        num = self.random.integers(i, j)
        return num

    def log(self, to_log) -> None:
        """ Writes a string to the log file of the environment """
        self.logging.write_to_file(to_log)

    def is_detected(self) -> bool:
        """ Returns if a SimObj is detected and can be interacted with """
        detect_chance = self.rng(0, 101)
        if detect_chance <= self.get_detectability():
            return True
        return False

    def tick(self) -> None:
        """ Alters a SimObj upon the environment ticking """
        raise NotImplementedError

    def get_info(self) -> list:
        """ Subclass will return a list of info usable in generating state/observation """
        raise NotImplementedError