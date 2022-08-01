import numpy as np
import pygame

from Environment import WorldEnv
from Tile import Tile

class HexagonTile:
    """ Hexagon class """
    def __init__(self, position, tile, radius=20):
        self.position = position
        self.tile = tile
        self.radius = radius
        self.vertices = self.compute_vertices()

    def compute_vertices(self) -> list[tuple[float, float]]:
        """ Returns a list of the hexagon's vertices as x, y tuples """
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        return [
            (x, y),
            (x - minimal_radius, y + half_radius),
            (x - minimal_radius, y + 3 * half_radius),
            (x, y + 2 * self.radius),
            (x + minimal_radius, y + 3 * half_radius),
            (x + minimal_radius, y + half_radius),
        ]

    def collide_with_point(self, point: tuple[float, float]) -> bool:
        """ Returns True if distance from centre to point is less than horizontal_length """
        return np.linalg.norm(np.subtract(point, self.centre)) < self.minimal_radius

    def render(self, screen) -> None:
        """ Renders the hexagon on the screen """
        pygame.draw.polygon(screen, self.get_colour(), self.vertices)

    def render_border(self, screen, border_colour) -> None:
        """ Draws a border around the hexagon """
        pygame.draw.aalines(screen, border_colour, closed=True, points=self.vertices)

    @property
    def centre(self) -> tuple[float, float]:
        """ Centre of the hexagon """
        x, y = self.position  # pylint: disable=invalid-name
        return (x, y + self.radius)

    @property
    def minimal_radius(self) -> float:
        """ Horizontal length of the hexagon """
        # https://en.wikipedia.org/wiki/Hexagon#Parameters
        return self.radius * np.cos(np.radians(30))

    def get_colour(self) -> tuple[int, int, int]:
        """ Colours the hexagons based on the presence of Simulation Objects """
        # Not traversable
        if self.tile.get_traverse() == False:
            return (20, 20, 20)
        # Animals are present
        agent_pres, stat_pred_pres, rand_pred_pres, patr_pred_pres = False, False, False, False
        for animal in self.tile.get_animals():
            if animal.get_name() == "Agent": 
                agent_pres = True
            elif animal.get_name() == "StationaryPredator": 
                stat_pred_pres = True
            elif animal.get_name() == "RandomPredator": 
                rand_pred_pres = True
            elif animal.get_name() == "PatrolPredator": 
                patr_pred_pres = True
        if agent_pres or stat_pred_pres or rand_pred_pres or patr_pred_pres:
            if agent_pres:
                if (stat_pred_pres or rand_pred_pres or patr_pred_pres):
                    return (200, 200, 200)
                else:
                    return (0, 255, 0)
            else:
                type_count = 0
                for pres in [stat_pred_pres, rand_pred_pres, patr_pred_pres]:
                    if pres == True:
                        type_count += 1
                if type_count > 1:
                    return (255, 0, 0)
                if stat_pred_pres:
                    return (255, 120, 150)
                if rand_pred_pres:
                    return (255, 80, 100)
                if patr_pred_pres:
                    return (255, 40, 50)
        # Resources present
        tree_pres = False
        r, g, b = 50, 50, 50
        for resource in self.tile.get_resources():
            if resource.get_name() == "Corpse": 
                r = 120
            if resource.get_name() == "BerryBush":
                g = 120
            if resource.get_name() == "Water": 
                b = 120
            if resource.get_name() == "Tree": 
                r, g, b = r, g + 60, b + 60
        if r != 50 or g != 50 or b != 50:
            return (r% 256, g% 256, b% 256)
        # Properties present
        if len(self.tile.get_properties()) > 0:
            q = len(self.tile.get_properties())*20
            return ((q+r) % 256, (q+g) % 256, (q+b) % 256)
        return (r, g, b)

class RenderTile(Tile):
    def __init__(self, *args):
        super().__init__(*args)

    def get_info(self) -> list[str, ...]:
        animals, resources, properties = self.get_animals(), self.get_resources(), self.get_properties()
        # Tiles
        tile_str = ["Tile: ", F"x, y = ({self.x}, {self.y})", F"Traversable = {self.traversable}"]
        tile_str.append("")
        animal_str, resource_str, property_str = ["Animals: "], ["Resources: "], ["Properties:"]
        # Animals
        if len(animals) > 0:
            for animal in animals:
                animal_str.append(animal.get_name())
                animal_str.extend([F"Object ID = {animal.get_obj_id()}", F"ID = {animal.get_id()}", F"Detectability = {animal.get_detectability()}"])
                animal_str.extend([F"Alive = {animal.get_alive()}", F"Health = {animal.get_health()}", F"Attack = {animal.get_attack()}"])
                # Agent
                if animal.get_name() == "Agent":
                    animal_str.extend([F"Hunger = {animal.get_hunger()}", F"Thirst = {animal.get_thirst()}"])
                # Predators
                if animal.get_name() == "PatrolPredator":
                    animal_str.extend([F"Origin = ({animal.origin.x}, {animal.origin.y})", F"Destination = ({animal.destination.x}, {animal.destination.y})"])
                animal_str.append("")
        else:
            animal_str.append("Empty")
            animal_str.append("")

        # Resources
        if len(resources) > 0:
            for resource in resources:
                resource_str.append(resource.get_name())
                resource_str.extend([F"Object ID = {resource.get_obj_id()}", F"ID = {resource.get_id()}", F"Detectability = {resource.get_detectability()}"])
                if resource.get_name() == "Tree":
                    resource_str.extend([F"Camouflage = {resource.get_camouflage()}", F"Agent Limit = {resource.get_limit()}", F"Current Agents = {len(resource.get_agents())}"])

                if resource.get_name() in ["BerryBush", "Corpse", "Water"]:
                    resource_str.extend([F"Quantity = {resource.get_quantity()}", F"Nutrition = {resource.get_nutrition()}", F"Food Group = {resource.get_group()}"])
                    if resource.get_name() == "BerryBush":
                        resource_str.append(F"Regen Chance = {resource.get_regen()}")
                    elif resource.get_name() == "Corpse":
                        resource_str.append(F"Decay Chance = {resource.get_decay()}")
                resource_str.append("")
        else:
            resource_str.append("Empty")
            resource_str.append("")

        # Properties
        if len(properties) > 0:
            for property in properties:
                property_str.append(property.get_name())
                animal = property.get_animal()
                property_str.extend([F"Animal = {animal.get_name()} ({animal.get_obj_id()}, {animal.get_id()})", F"Detectability = {property.get_detectability()}"])
                if property.get_name() == "Tracks":
                    property_str.extend([F"Direction = {property.get_direction()}", F"Strength = {property.get_strength()}"])
                property_str.append("")
        else:
            property_str.append("Empty")
            property_str.append("")
        return tile_str + animal_str + resource_str + property_str

class WorldEnvRender(WorldEnv):
    """ Subclass of WorldEnv that is capable of displaying the environment """
    def __init__(self, screen_width, screen_height, delay, *args):
        super().__init__(*args)
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        # set the pygame window name
        pygame.display.set_caption('⬡ Poly-Hex ⬡')
        # Sets Font
        self.font = pygame.font.Font('freesansbold.ttf', 24)

        self.clock = pygame.time.Clock()
        self.delay = delay
        self.auto_run = True
        self.terminated = False

    def reset(self) -> dict:
        """ Resets the environment and the hexagons used for drawing """
        super().reset()
        self.init_hexagons()

    def render(self) -> None:
        """ Renders hexagons on the Pygame screen """
        if not self.terminated:
            # Waits for input if it is not running normally
            next_turn = False
            while True:
                self.screen.fill((0, 0, 0))
                for hexagon in self.hexagons:
                    hexagon.render(self.screen)
                # draw borders around colliding hexagons and neighbours
                mouse_pos = pygame.mouse.get_pos()
                hit = None
                for hexagon in self.hexagons: 
                    if hexagon.collide_with_point(mouse_pos):
                        hit = hexagon
                        hit.render_border(self.screen, border_colour=(0, 0, 0))
                        # Draws text
                        text_colour = (255, 255, 255)#(124, 144, 207)
                        highlight = (202, 49, 105)#(255, 177, 205)
                        #print(hit.tile)
                        #text = self.font.render(str(hit.tile), True, green, blue)
                        width, height = pygame.display.get_surface().get_size()
                        font_height = self.font.get_height()
                        to_print = hit.tile.get_info()
                        text = self.font.render(F"Current Turn, Max Turn = ({self.get_turn()}, {self.get_max_turn()})", True, text_colour, highlight)
                        self.screen.blit(text, (0.60*width, 0.05*height))
                        text = self.font.render(F"Width, Height = ({self.get_grid_width()}, {self.get_grid_height()})", True, text_colour, highlight)
                        self.screen.blit(text, (0.60*width, 0.05*height+font_height))
                        text = self.font.render("", True, text_colour, highlight)
                        self.screen.blit(text, (0.60*width, 0.05*height+2*font_height))
                        for i in range(len(to_print)):
                            text = self.font.render(to_print[i], True, text_colour, highlight)
                            self.screen.blit(text, (0.60*width, 0.05*height+(i+3)*font_height))
                pygame.display.flip()
                # Checks events to see if it should continue
                next_turn = False
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.auto_run = not self.auto_run
                        next_turn = True
                    elif event.type == pygame.QUIT:
                        self.terminated = True
                        pygame.display.quit()
                        next_turn = True
                if self.auto_run or next_turn:
                    break
            pygame.time.delay(self.delay)

    def init_hexagons(self) -> None:
        """ Creates a HexagonTile map of the environment """
        width, height = pygame.display.get_surface().get_size()
        hex_width, hex_height = int(0.50*0.5*width // self.get_grid_width()), int(0.90*0.65*height // self.get_grid_height())
        radius = np.min([hex_width, hex_height])
        leftmost_hexagon = HexagonTile((0.05*width, 0.05*height), self.get_tile(0, 0), radius)

        #width, height = pygame.display.get_surface().get_size()
        #radius = np.min([width // self.get_grid_width(), height // self.get_grid_height() // 1.8])
        # Creates the first hexagon as an anchor
        #leftmost_hexagon = HexagonTile((radius*12, radius*2), self.get_tile(0, 0), radius)
        hexagons = [leftmost_hexagon]
        for y in range(0, self.get_grid_height()):
            hexagon = leftmost_hexagon
            for x in range(1, self.get_grid_width()):
                i, j = hexagon.position
                position = (i + hexagon.minimal_radius * 2, j)
                hexagon = HexagonTile(position, self.get_tile(x, y), radius)
                hexagons.append(hexagon)
            # Generates the next row when appropriate
            if y+1 < self.get_grid_height():
                index = 2 if y % 2 == 1 else 4
                position = leftmost_hexagon.vertices[index]
                leftmost_hexagon = HexagonTile(position, self.get_tile(0, y+1), radius)
                hexagons.append(leftmost_hexagon)
        self.hexagons = hexagons

    def create_hex_grid(self) -> None:
        """ Creates the hex-grid of grid_width and grid_height with traversability """
        self.tiles = []
        # Checks if all tiles are traversable
        trav = (self.get_non_trav_chance() == 0)
        for y in range(self.get_grid_height()):
            self.tiles.append([])
            for x in range(self.get_grid_width()):
                tile_num = y * self.get_grid_height() + x
                new_tile = RenderTile(x, y, tile_num, trav)
                self.tiles[y].append(new_tile)