class Tile:
    """ A Tile is a node in the environment which can contain an infinite number of SimObjects and Properties.
        Each Tile has six neighbouring tiles, unless they are on the edge of the environment, and animals can move
        from one Tile to another unless they are specified non-traversable """
    def __init__(self, x, y, num, trav):
        self.x = x
        self.y = y
        self.tile_num = num
        # Could potentially use a better, more accessible way for of storing and returning the properties
        self.animals = []  # agents or predators or living moving things
        self.properties = []  # properties of a tile like smell
        self.resources = []  # resources in the tile
        # List of searchable property names
        self.names = []

        self.traversable = trav

    def __str__(self) -> str:
        return F"Tile: x, y = ({self.x}, {self.y}), traversable = {self.traversable}"

    def get_position(self) -> tuple[int, int]:
        """ Returns the Tile's position in the environment """
        return self.x, self.y

    def get_tile_num(self) -> int:
        """ Returns the tiles number based on its x and y coordinates """
        return self.tile_num

    def get_traverse(self) -> bool:
        """ Returns the traversability of the Tile """
        return self.traversable

    def get_animals(self) -> list:
        """" Returns a list of the Animals in the Tile """
        return self.animals

    def get_properties(self) -> list:
        """ Returns a list of the Properties in the Tile """
        return self.properties

    def get_resources(self) -> list:
        """ Returns a list of the Resources in the Tile """
        return self.resources

    def get_sim_object(self, obj_id, id):
        """ Search a Tile for a specifc object using the identifiying values of obj_id and id
            Properties are intialised with unique ID's as they are dynamically produced """
        for obj in self.get_animals() + self.get_resources() + self.get_properties():
            if obj.get_obj_id() == obj_id and obj.get_id() == id:
                return obj
        return None

    def add_sim_object(self, sim_object):
        """ Adds a SimObject to a list depending on its type """
        if sim_object.get_obj_category() == 1:
            self.animals.append(sim_object)
        elif sim_object.get_obj_category() == 2:
            self.resources.append(sim_object)
        elif sim_object.get_obj_category() == 3:
            self.properties.append(sim_object)

    def remove_sim_object(self, sim_object):
        """ Removes a SimObject from the list it is in """
        if sim_object.get_obj_category() == 1:
            self.animals.remove(sim_object)
        elif sim_object.get_obj_category() == 2:
            self.resources.remove(sim_object)
        elif sim_object.get_obj_category() == 3:
            self.properties.remove(sim_object)

    def set_traverse(self, boolean) -> None:
        """ Sets if the Tile is traversable or not """
        self.traversable = boolean

    def get_actions(self, animal) -> list[list[int]]:
        """ Using pre-defined values for actions we can return the valid actions for each of the Tiles in
            the environment with respect to detected simulation objects """
        # Default is for an animal to take no action
        actions = [[0,0,0]]
        for obj in self.get_animals() + self.get_resources():
            if obj != animal and obj.is_detected():
                name = obj.get_name()
                # The object can be consumed by an animal
                if name == "Water" or name == "BerryBush" or name == "Corpse":
                    actions.append([1, obj.get_obj_id(), obj.get_id()])
                # The object can hide an animal
                elif name == "Tree":
                    actions.append([2, obj.get_obj_id(), obj.get_id()])
                # The object can be attacked by an animal
                else:
                    actions.append([3, obj.get_obj_id(), obj.get_id()])
        return actions

    def get_neighbours(self) -> list["Tile"]:
        """ Returns all of the neighbouring Tiles """
        return self.neighbours

    def set_neighbours(self, neighbours) -> None:
        """ Sets all of the neighbouring Tiles, None is used for neighbours that do not exist """
        self.neighbours = neighbours

    def neighbours_full(self) -> bool:
        """ Only returns true if the tile has a neighbour on every side """
        if None in self.get_neighbours():
            return False
        return True

    def non_trav_count(self, prev_tile) -> int:
        """ Returns the amount of neighbouring Tiles that are non-traversable """
        counter = 0
        for neighbour in self.get_neighbours():
            if neighbour is not None and neighbour.get_traverse() is False and neighbour is not prev_tile:
                counter += 1
        return counter

    def get_next_non_trav(self, prev_tiles) -> "Tile":
        """ Return the next neighbour as long as it is not the previous neighbour """
        for neighbour in self.get_neighbours():
            if neighbour is not None and neighbour.get_traverse() is False and neighbour not in prev_tiles:
                return neighbour
        return None
      
    def tick(self) -> None:
        """ Ticks through all of the objects in the Property and Resource lists """
        for property in self.get_properties():
            property.tick()
        for resource in self.get_resources():
            resource.tick()
