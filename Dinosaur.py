import random
class Dinosaur:
    def __init__(self, **traits) -> None:
        #gamestats:
        self.dino_size = 20
        self.dino_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.dino_x = random.randint(1, (1920//20 - 2))
        self.dino_y = random.randint(1, (1080//20 - 2))
        # Stats
        self.currHealth = 100
        self.totalHealth = 100
        self.carnVal = 1
        self.herbVal = 1
        self.energy = 100
        self.energyConsumption = 0
        self.power = 100
        self.isAlive = True

        # Features of this dinosaur
        self.defaultTraits = {
            'Size': None,
            'Mouth': None,
            'Mobility': None,
            'Combat': None,
            'Neck': None,
            'Tail': None,
        }
        self.traits = {**self.defaultTraits, **traits}

        # Setting up energy
        self.energyModifier = {
            'Large': 1.5,
            'Medium': 1.25,
            'Small': 1,
            'Bipedal': 1,
            'Quadruped': 1.25,
            'Flying': 0.75,
            None: 1,
            'Long': 1}
        self.energy = int(100 * self.energyModifier[self.traits['Size']] * \
            self.energyModifier[self.traits['Mobility']] * \
            self.energyModifier[self.traits['Neck']])

        # Setting up Power
        self.powerModifier = {
            #multiplier
            'Large': 10, 
            'Medium': 5, 
            'Small': 2,

            #adding
            'Beak' : 30,
            'Herbivore Teeth' : 10,
            'Carnivore Teeth' : 50,
            'Spikes' : 15,
            'Horns' : 30,
            'Claws' : 50,
            'Bipedal' : 30,
            'Quadruped' : -10,
            'Flying' : 20,
            'Long' : - 30,
            None : 0,
            'Mobile Tail' : 10,
            'Attack Tail' : 40
        }
        self.power *= self.powerModifier[self.traits['Size']]
        self.power += self.powerModifier[self.traits['Mouth']] + self.powerModifier[self.traits['Mobility']] \
        + self.powerModifier[self.traits['Combat']] + self.powerModifier[self.traits['Neck']] + self.powerModifier[self.traits['Tail']] 

        # Setting up carnVal
        self.carnValModifier = {
            'Large': 1,
            'Medium': 1,
            'Small': 0.5,
            'Beak': 1,
            'Herbivore Teeth': 0.5,
            'Carnivore Teeth': 1,
            'Spikes': 0.5,
            'Horns': 0.75,
            'Claws': 1,
            'Bipedal': 1,
            'Quadruped': 0.5,
            'Flying': 1,
            'Long': 0.5,
            None: 1,
            'Mobile Tail': 1,
            'Attack Tail': 0.75
        }
        self.carnVal *= self.carnValModifier[self.traits['Size']] * self.carnValModifier[self.traits['Mouth']] \
            * self.carnValModifier[self.traits['Mobility']] * self.carnValModifier[self.traits['Combat']] * self.carnValModifier[self.traits['Neck']] * self.carnValModifier[self.traits['Tail']]

        # Setting up herbVal
        self.herbValModifier = {
            'Large': 0.5,
            'Medium': 0.75,
            'Small': 1,
            'Beak': 1,
            'Herbivore Teeth': 1,
            'Carnivore Teeth': 0.5,
            'Spikes': 1,
            'Horns': 1,
            'Claws': 0.5,
            'Bipedal': 0.75,
            'Quadruped': 1,
            'Flying': 0.75,
            'Long': 1,
            None: 1,
            'Mobile Tail': 0.75,
            'Attack Tail': 1
        }
        self.herbVal *= self.herbValModifier[self.traits['Size']] * self.herbValModifier[self.traits['Mouth']] \
            * self.herbValModifier[self.traits['Mobility']] * self.herbValModifier[self.traits['Combat']] * self.herbValModifier[self.traits['Neck']] * self.herbValModifier[self.traits['Tail']]

        self.energyConsumptionModifier = {
            'Large': 1.5,
            'Medium': 1.25,
            'Small': 1,
            'Bipedal': 0.75,
            'Quadruped': 1.25,
            'Flying': 0.5,
            None: 1
        }
        self.energyConsumption = round(
            50 * self.energyConsumptionModifier[self.traits['Size']] * self.energyConsumptionModifier[self.traits['Mobility']])

    def child(self, other):
        if self.energy > 20:
            new_traits = self.traits
            for i in new_traits.values():
                if i[1] == None:
                    new_traits[i[0]] = other.traits[i[0]]
            return Dinosaur(new_traits)
        else:
            return
    def calculateNextStep(self, obs, behaviorfunc):
        return behaviorfunc(self, obs)

def fiftyFftydinoPlans(dino, obs):
    return random.choice([goToNearestDino(dino,obs), goToGreensOnly(dino, obs)])

def goToNearestDino(dino, obs):
    nearest_dino = calculate_nearest_other_dino(dino, obs)
    if nearest_dino:
        if nearest_dino[0] < dino.dino_x:
            return 'left'
        elif nearest_dino[0] > dino.dino_x:
            return 'right'
        elif nearest_dino[1] < dino.dino_y:
            return 'up'
        elif nearest_dino[1] > dino.dino_y:
            return 'down'
        
    return random.choice(['left', 'right', 'up', 'down'])

def goToGreensOnly(dino, obs):
    nearest_green_space = calculate_nearest_green_space(dino, obs)
    if nearest_green_space:
        if nearest_green_space[0] < dino.dino_x:
            return 'left'
        elif nearest_green_space[0] > dino.dino_x:
            return 'right'
        elif nearest_green_space[1] < dino.dino_y:
            return 'up'
        elif nearest_green_space[1] > dino.dino_y:
            return 'down'
    return random.choice(['left', 'right', 'up', 'down'])
#helperFunctions
#dino is current dino we are looking at
# observation = {
#     'empty_spaces': empty_spaces,
#     'green_spaces': green_spaces,
#     'wall_spaces': wall_spaces,
#     'other_dino_positions': other_dino_positions
# }
def calculate_nearest_green_space(dino, obs):
    min_distance = float('inf')
    nearest_green_space = None

    for green_space in obs['green_spaces']:
        distance = abs(green_space[0] - dino.dino_x) + abs(green_space[1] - dino.dino_y)
        if distance < min_distance:
            min_distance = distance
            nearest_green_space = green_space

    return nearest_green_space

def calculate_nearest_other_dino(dino, obs):
    min_distance = float('inf')
    nearest_dino = None

    for dino_position in obs['other_dino_positions']:
        distance = abs(dino_position[0] - dino.dino_x) + abs(dino_position[1] - dino.dino_y)
        if distance < min_distance:
            min_distance = distance
            nearest_dino = dino_position

    return nearest_dino

def calculate_nearest_wall(dino, obs):
    min_distance = float('inf')
    nearest_wall = None

    for wall_space in obs['wall_spaces']:
        distance = abs(wall_space[0] - dino.dino_x) + abs(wall_space[1] - dino.dino_y)
        if distance < min_distance:
            min_distance = distance
            nearest_wall = wall_space

    return nearest_wall


def calculate_nearest_group_of_green_spaces(dino, obs, group_size):
    min_distance = float('inf')
    nearest_group = None

    for i in range(len(obs['green_spaces']) - group_size + 1):
        group = obs['green_spaces'][i:i+group_size]
        group_center = (sum(coord[0] for coord in group) // group_size, sum(coord[1] for coord in group) // group_size)
        distance = abs(group_center[0] - dino.dino_x) + abs(group_center[1] - dino.dino_y)
        if distance < min_distance:
            min_distance = distance
            nearest_group = group

    return nearest_group
#define begaviors
#returns all valid positions not in walls
def valid_movement_avoiding_walls(dino, obs):
    possible_actions = ['left', 'right', 'up', 'down']
    valid_actions = []
    
    for action in possible_actions:
        if (action == 'left' and (dino.dino_x-1, dino.dino_y) not in self.walls) or \
        (action == 'right' and (dino.dino_x+1, dino.dino_y) not in self.walls) or \
        (action == 'up' and (dino.dino_x, dino.dino_y-1) not in self.walls) or \
        (action == 'down' and (dino.dino_x, dino.dino_y+1) not in self.walls):
            valid_actions.append(action)
    return valid_actions


    
