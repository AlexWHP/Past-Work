from SimulationObject import SimulationObject

class Resource(SimulationObject):
    """ A resource is a Simulation Object that is fixed to a specific tile and can be interacted with by animals """
    def __init__(self, data):
        super().__init__(data)

    def destroy(self) -> None:
        """ Removes a Resources from its Tile class, excluding it from the simulation """
        self.get_tile().remove_sim_object(self)
        self.set_tile(None)
        self.log("{} has been destroyed".format(self))

class Tree(Resource):
    """ Object that allows agents to hide from hunting or chasing predators """
    def __init__(self, data, camouflage, limit):
        super().__init__(data)
        self.agents = []
        self.camouflage = camouflage
        self.limit = limit

    def get_camouflage(self):
        """ Returns the detectability of agents who are hiding in the tree """
        return self.camouflage

    def get_limit(self) -> int:
        """ Returns the max amount of agents that can hide in the tree """
        return self.limit

    def get_agents(self) -> list: 
        """ Returns the agents stored within the Tree """
        return self.agents

    def add_agent(self, agent) -> None:
        """ Adds an agent within the tree """
        self.agents.append(agent)
        agent.set_detectability(self.get_camouflage())
        agent.set_tree(True)

    def reset_agents(self) -> None:
        """ Defines the stored agents in the Tree to be empty """
        self.agents = []

    def hide(self, agent) -> None:
        """ Reduces an animals detectability and stores them within the Tree """
        if len(self.get_agents()) < self.limit:
            self.add_agent(agent)
            self.log("{} hid in {} at {}".format(agent, self, self.get_tile().get_position()))
            if len(self.get_agents()) >= self.limit:
                self.log("{} ({}) at {} has reached full capacity".format(self.get_name(), self.get_id(), self.get_tile().get_position()))

    def tick(self) -> None:
        """ Removes stored agents and resets their detectability as well as it's own """
        for agent in self.get_agents():
            agent.set_detectability(agent.get_default_detectability())
            agent.set_tree(False)
        self.reset_agents()

    def get_info(self) -> list:
        """ Returns all of the info the Tree has """
        obj_id = self.get_obj_id()   
        tree_id = self.get_id()
        detectability = self.get_detectability()
        agent_limit = self.get_limit()
        current_agents = len(self.get_agents())

        return [obj_id, tree_id, detectability, agent_limit, current_agents]


class Food(Resource):
    """ Food is necassary for an agents survival and can be a measure of its fitness based on how much it is able to consume.
        - Quantity determines how many times the food can be consumed
        - Nutrition determines how much hunger it restores upon consumption """
    def __init__(self, data, quantity, nutrition, group):
        super().__init__(data)
        self.quantity = quantity
        self.nutrition = nutrition
        self.group = group

    def get_quantity(self) -> int:
        """ Returns the amount of portions left in the food """
        return self.quantity

    def get_nutrition(self) -> int:
        """ Returns the nutritional value of portions within the food """
        return self.nutrition

    def get_group(self) -> str:
        """ Returns the food group ("Fruit", "Meat", "Water") """
        return self.group

    def consumed(self) -> None:
        """ Alters the Food upon consumption"""
        raise NotImplementedError

class BerryBush(Food):
    """ A replenshing source of food in the environment """
    def __init__(self, data, quantity, nutrition, regen):
        super().__init__(data, quantity, nutrition, "Fruit")
        self.regen_percent = regen

    def get_regen(self) -> int:
        """ Returns the regeneration chance of the BerryBush """
        return self.regen_percent
    
    def regen(self) -> None:
        """ Regenerates the BerryBush by incrementing the quantity available """
        if self.rng(1, 100) < self.get_regen():
            self.quantity += 1
            # self.log("{} ({}) at {} has replenished itself".format(self.get_name(), self.get_id(), self.get_tile().get_position()))

    def consumed(self) -> int:
        """ Returns the nutrition gained by consuming the BerryBush """
        if self.get_quantity() > 0:
            self.quantity -= 1
            return(self.get_nutrition())
        return 0

    def tick(self) -> None:
        """ Regenerates the BerryBush based on its defined chance """
        self.regen()

    def get_info(self) -> list:
        """ Returns all of the info the BerryBush has """
        obj_id = self.get_obj_id()   
        bush_id = self.get_id()
        detectability = self.get_detectability()
        quantity = self.get_quantity()
        nutrition = self.get_nutrition()
        food_group = 0  # "Fruit" group value is 0, "Meat" = 1, "Water" = 2 
        regen_chance = self.get_regen()

        return [obj_id, bush_id, detectability, quantity, nutrition, food_group, regen_chance]

class Corpse(Food):
    """ A decaying source of food produced by the death of an animal """
    def __init__(self, data, quantity, nutrition, decay, animal):
        super().__init__(data, quantity, nutrition, "Meat")
        self.decay_percent = decay
        self.source = animal

    def __str__(self) -> str:
        """ Returns Corpse and it's sources name and information """
        return "{} of {}".format(self.get_name(), self.get_source())

    def get_source(self) -> int:
        """ Returns the Animal that produced the Corpse """
        return self.source

    def get_decay(self) -> int:
        """ Returns the decay chance of the Corpse """
        return self.decay_percent

    def decay(self) -> None:
        """ Chance to decay the Corpse by decrementing its nutritional value """
        if self.rng(1, 100) < self.get_decay():
            self.nutrition -= 1
            # self.log("{} ({}) at {} has decayed".format(self.get_name(), self.get_id(), self.get_tile().get_position()))
            if self.get_nutrition() < 1:
                self.destroy()

    def consumed(self) -> int:
        """ Returns the nutrition gained by consuming the Corpse and destroys if it runs out """
        if self.get_quantity() > 0:
            self.quantity -= 1
            if self.get_quantity() < 1:
                self.destroy()
            return(self.get_nutrition())
        return 0

    def tick(self) -> None:
        """ Decays the Corpse based on its defined chance """
        self.decay()

    def get_info(self) -> list:
        """ Returns all of the info the Corpse has """
        obj_id = int(self.get_obj_id())   
        corpse_id = self.get_id()
        detectability = self.get_detectability()
        quantity = self.get_quantity()
        nutrition = self.get_nutrition()
        food_group = 1  # "Fruit" group value is 0, "Meat" = 1, "Water" = 2 
        decay_chance = self.get_decay()

        return [obj_id, corpse_id, detectability, quantity, nutrition, food_group, decay_chance]


class Water(Food):
    """ A food object that replenishes thirst instead of hunger """
    def __init__(self, data, quantity, nutrition):
        super().__init__(data, quantity, nutrition, "Water")

    def consumed(self) -> int:
        """ Returns the nutrition gained by consuming the Water """
        return self.get_nutrition()

    def tick(self) -> None:
        """ Water is unchanged as the environment ticks """
        pass

    def get_info(self) -> list:
        """ Returns all of the info the Water has """
        obj_id = self.get_obj_id()   
        water_id = self.get_id()
        detectability = self.get_detectability()
        quantity = self.get_quantity()
        nutrition = self.get_nutrition()
        food_group = 2  # "Fruit" group value is 0, "Meat" = 1, "Water" = 2 

        return [obj_id, water_id, detectability, quantity, nutrition, food_group]
