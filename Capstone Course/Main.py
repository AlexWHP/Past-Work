""" Main.py functions as a foundation for using the environment and integrating it with OpenAI gym. env_parameters
    provide the foundational information for the environment to structure itself around. obj_counts defines the 
    the amount of Simulation Objects with each correlating to agents, stationary predators, random predators, 
    patrol predators, berry bushes, water sources, and trees respectively. obj_parameters are for every attribute
    of the Simulation Objects with each of the keys defining the values for each of them.
    Notably, the example below works by randomly selecting movement and actions yet the environment outputs a fully
    defined observation_space that can be used to inform the agents and give information to OpenAI gym.
    Logging works by outputting statements throughout the code to a text file stored within the logs file and give
    an understanding of what is occuring within the environment and provides context to the visualisation. """

from Environment import WorldEnv
from Visualiser import WorldEnvRender
from Logging import Logging

def get_parameters():
    """ Returns the parameters the environment uses for initialisation """
    env_parameters = {
        "width":                30,
        "height":               30,
        "seed":                 1,
        "max_turns":            80,
        "non_trav_chance":      40
    }
    # AGENT, SPREDATOR, RPREDATOR, PPREDATOR, BBUSH, WATER, TREE
    obj_counts = [20, 5, 5, 5, 30, 30, 30]
    obj_parameters = {
        "agent": {
            "detectability":    80,
            "health":           10,
            "attack":           1,
            "hunger":           20,
            "thirst":           20
        },
        "spredator": {
            "detectability":    80,
            "health":           10,
            "attack":           1
        },
        "rpredator": {
            "detectability":    80,
            "health":           10,
            "attack":           1
        },
        "ppredator": {
            "detectability":    80,
            "health":           10,
            "attack":           1
        },
        "bbush": {
            "detectability":    100,
            "quantity":         2,
            "nutrition":        10,
            "regen":            30
        },
        "corpse": {
            "detectability":    100,
            "quantity":         2,
            "nutrition":        10,
            "decay":            30
        },
        "water": {
            "detectability":    100,
            "quantity":         1,
            "nutrition":        20
        },
        "tree": {
            "detectability":    100,
            "camouflage":       10,
            "limit":            3
        },
        "tracks": {
            "detectability":    100,
            "strength":         4
        }
    }
    return env_parameters, obj_counts, obj_parameters

def main() -> None:
    """ Simple example with valid random movement and actions performed by an agent """
    log = Logging()
    env_parameters, obj_counts, obj_parameters = get_parameters()
    # Screen width, height, and delay for the visualisation before rendering
    screen_width, screen_height, delay = 1900, 1000, 10
    env = WorldEnvRender(screen_width, screen_height, delay, env_parameters, obj_counts, obj_parameters, log)
    #env = WorldEnv(env_parameters, obj_counts, obj_parameters, log)
    state = env.reset()
    state_space = env.generate_state_space()
    #print(state_space.sample())
    score = 0
    done = False
    while not done:
        env.log("")
        env.log(str(env.get_turn()))
        for agent in env.get_agents():
            env.render()
            if agent.get_alive():
                # Select a random movement until it is valid move
                destination = None
                possible = [agent.get_tile()] + agent.get_tile().get_neighbours()
                while destination == None:
                    movement = env.rng(0, 7)
                    destination = possible[movement]
                # Retrieve the actions possible in the destination tile and select randomly
                actions = destination.get_actions(agent)
                act = actions[env.rng(0, len(actions))]
                action =  [agent.get_id(), movement] + act
            else:
                action = [agent.get_id(), 0, 0,0,0]
            n_state, reward, done, info = env.step(action)
            agent.add_score(reward)
            #print(n_state)
            agent.score += reward
        if done:
            env.reset()
            done = False
    env.log("")
    for agent in env.get_agents():
        env.log("{} | Location: {} | Survival-Time: {} | Kill-Count: {} | Health: {} | Hunger: {} | Thirst: {} | Score: {}".format(agent, agent.get_tile().get_position(), agent.get_turn(), agent.get_kills(), agent.get_health(), agent.get_hunger(), agent.get_thirst(), agent.get_score()))
    for pred in env.get_predators():
        env.log("{} | Location: {} | Survival-Time: {} | Kill-Count: {} | Health: {} | Hunger: {} | Thirst: {} |".format(pred, pred.get_tile().get_position(), pred.get_turn(), pred.get_kills(), pred.get_health(), pred.get_hunger(), pred.get_thirst()))
    env.log("")
    log.close()
main()