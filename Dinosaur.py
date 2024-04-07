import random
class Dinosaur:
    def __init__(self, **traits) -> None:
        #gamestats:
        self.dino_size = 20
        self.dino_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.dino_x = random.randint(1, (1920//20 - 2))
        self.dino_y = random.randint(1, (1080//20 - 2))
        self.dino_walls = None
        # Stats
        self.currHealth = 100
        self.totalHealth = 100
        self.carnVal = 1
        self.herbVal = 1
        self.energy = 100
        self.energyConsumption = 0
        self.power = 100
        self.isAlive = True
        self.dino_behavior = None

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
        new_traits = self.traits
        for i in new_traits.values():
            if i[1] == None:
                new_traits[i[0]] = other.traits[i[0]]

        youngling = Dinosaur(new_traits)
        youngling.dino_color = ((self.dino_color[0] + other.dino_color[0]) // 2, (self.dino_color[1] + other.dino_color[1]) // 2, (self.dino_color[2] + other.dino_color[2]) // 2)
        return youngling

    def calculateNextStep(self, obs, behaviorfunc):
        if self.dino_behavior == None:
            return behaviorfunc(self, obs)
        else:
            return self.dino_behavior(self,obs)

def getStats(dino):
    statList = ""
    for trait in dino.traits.values():
        statList += str(trait)
        statList += ","
    statList += str(dino.currHealth)
    statList += ","
    statList += str(dino.totalHealth)
    statList += ","
    statList += str(dino.carnVal)
    statList += ","
    statList += str(dino.herbVal)
    statList += ","
    statList += str(dino.energy)
    statList += ","
    statList += str(dino.energyConsumption)
    statList += ","
    statList += str(dino.power)
    statList += ","
    statList += str(dino.isAlive)

    return statList

def copDino(dino, obs):
    colors = ['lower', 'higher']
    criterion = random.choice(colors)
    
    if criterion == 'lower':
        nearest_dino = calculate_nearest_other_dino(dino, obs, criterion)
        actions = valid_movement_avoiding_walls(dino,obs)
        if nearest_dino:
            if nearest_dino[0] < dino.dino_x:
                if 'left' not in actions:
                    return 'right'
                else:
                    return 'left'
            elif nearest_dino[0] > dino.dino_x:
                if 'right' not in actions:
                    return 'left'
                else:
                    return 'right'
            elif nearest_dino[1] < dino.dino_y:
                if 'up' not in actions:
                    return 'down'
                else:
                    return 'up'
            elif nearest_dino[1] > dino.dino_y:
                if 'down' not in actions:
                    return 'up'
                else:
                    return 'down'
    else:
        nearest_dino = calculate_nearest_other_dino(dino, obs, criterion)
        actions = valid_movement_avoiding_walls(dino,obs)
        if nearest_dino:
            if nearest_dino[0] < dino.dino_x:
                if 'left' not in actions:
                    return 'right'
                else:
                    return 'left'
            elif nearest_dino[0] > dino.dino_x:
                if 'right' not in actions:
                    return 'left'
                else:
                    return 'right'
            elif nearest_dino[1] < dino.dino_y:
                if 'up' not in actions:
                    return 'down'
                else:
                    return 'up'
            elif nearest_dino[1] > dino.dino_y:
                if 'down' not in actions:
                    return 'up'
                else:
                    return 'down'
            
    return random.choice(['left', 'right', 'up', 'down'])

def cowardDino(dino, obs):
    direction = goToNearestDino(dino, obs)
    actions = valid_movement_avoiding_walls(dino, obs)
    if direction == 'left':
        if 'right' not in actions:
            return random.choice(actions)
        else:
            return 'right'
    elif direction == 'right':
        if 'left' not in actions:
            return random.choice(actions)
        else:
            return 'left'
    elif direction == 'up':
        if 'down' not in actions:
            return random.choice(actions)
        else:
            return 'down'
    else:
        if 'up' not in actions:
            return random.choice(actions)
        else:
            return 'up'

def fiftyFftydinoPlans(dino, obs):
    return random.choice([goToNearestDino(dino,obs), goToGreensOnly(dino, obs)])

def goToNearestDino(dino, obs):
    nearest_dino = calculate_nearest_other_dino(dino, obs)
    actions = valid_movement_avoiding_walls(dino,obs)
    if nearest_dino:
        if nearest_dino[0] < dino.dino_x:
            if 'left' not in actions:
                return 'right'
            else:
                return 'left'
        elif nearest_dino[0] > dino.dino_x:
            if 'right' not in actions:
                return 'left'
            else:
                return 'right'
        elif nearest_dino[1] < dino.dino_y:
            if 'up' not in actions:
                return 'down'
            else:
                return 'up'
        elif nearest_dino[1] > dino.dino_y:
            if 'down' not in actions:
                return 'up'
            else:
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

def randomBehav(dino, obs):
    return random.choice(['left', 'right', 'up', 'down'])

def paralyzed(dino, obs):
    return 'stay'

    
#helperFunctions
#dino is current dino we are looking at
# observation = {
#     'empty_spaces': empty_spaces,
#     'green_spaces': green_spaces,
#     'wall_spaces': wall_spaces,
#     'other_dino_positions': other_dino_positions,
#     'other_dino_powers':other_dino_powers,
#     'other_dino_colors':other_dino_colors,
#     'other_dino_energy_consumption': other_dino_energy_consumption,
#     'other_dino_energy': other_dino_energy,
#     'other_dino_herb': other_dino_herb,
#     'other_dino_carn': other_dino_carn
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



def calculate_min_carn_dino_space(dino, obs):
    min_carn_val = float('inf')
    min_carn_dino_space = None

    for dino_position, dino_carn_val in zip(obs['other_dino_positions'], obs['other_dino_carn']):
        if dino_carn_val < min_carn_val:
            min_carn_val = dino_carn_val
            min_carn_dino_space = dino_position

    return min_carn_dino_space

def calculate_most_carn_dino_space(dino, obs):
    max_carn_val = float('-inf')
    most_carn_dino_space = None

    for dino_position, dino_carn_val in zip(obs['other_dino_positions'], obs['other_dino_carn']):
        if dino_carn_val > max_carn_val:
            max_carn_val = dino_carn_val
            most_carn_dino_space = dino_position

    return most_carn_dino_space
def calculate_min_herb_dino_space(dino, obs):
    min_herb_val = float('inf')
    min_herb_dino_space = None

    for dino_position, dino_herb_val in zip(obs['other_dino_positions'], obs['other_dino_herb']):
        if dino_herb_val < min_herb_val:
            min_herb_val = dino_herb_val
            min_herb_dino_space = dino_position

    return min_herb_dino_space

def calculate_most_herb_dino_space(dino, obs):
    max_herb_val = float('-inf')
    most_herb_dino_space = None

    for dino_position, dino_herb_val in zip(obs['other_dino_positions'], obs['other_dino_herb']):
        if dino_herb_val > max_herb_val:
            max_herb_val = dino_herb_val
            most_herb_dino_space = dino_position

    return most_herb_dino_space


def calculate_max_energy_consumption_space(dino, obs):
    max_energy_consumption = float('-inf')
    max_energy_consumption_space = None

    for dino_position, dino_energy_consumption in zip(obs['other_dino_positions'], obs['other_dino_energy_consumption']):
        if dino_energy_consumption > max_energy_consumption:
            max_energy_consumption = dino_energy_consumption
            max_energy_consumption_space = dino_position

    return max_energy_consumption_space

def calculate_min_energy_consumption_space(dino, obs):
    min_energy_consumption = float('inf')
    min_energy_consumption_space = None

    for dino_position, dino_energy_consumption in zip(obs['other_dino_positions'], obs['other_dino_energy_consumption']):
        if dino_energy_consumption < min_energy_consumption:
            min_energy_consumption = dino_energy_consumptionin_energy_consumption = dino_energy_consumption
            min_energy_consumption_space = dino_position

    return min_energy_consumption_space


def calculate_strongest_dino_space(dino, obs):
    max_power = float('-inf')
    strongest_dino_space = None

    for dino_position, dino_power in zip(obs['other_dino_positions'], obs['other_dino_powers']):
        if dino_power > max_power:
            max_power = dino_power
            strongest_dino_space = dino_position

    return strongest_dino_space
def calculate_weakest_dino_space(dino, obs):
    min_power = float('inf')
    weakest_dino_space = None

    for dino_position, dino_power in zip(obs['other_dino_positions'], obs['other_dino_powers']):
        if dino_power < min_power:
            min_power = dino_power
            weakest_dino_space = dino_position

    return weakest_dino_space

def calculate_nearest_other_dino(dino, obs, colorCriterion='None'):
    min_distance = float('inf')
    nearest_dino = None

    if colorCriterion == 'None':
        for dino_position in obs['other_dino_positions']:
            distance = abs(dino_position[0] - dino.dino_x) + abs(dino_position[1] - dino.dino_y)
            if distance < min_distance:
                min_distance = distance
                nearest_dino = dino_position
    elif colorCriterion == 'lower':
        for dino_color in obs['other_dino_colors']:
            if dino_color[0][0] < 126 and dino_color[0][1] < 126 and dino_color[0][2] < 126:
                distance = abs(dino_color[1][0] - dino.dino_x) + abs(dino_color[1][1] - dino.dino_y) 
                if distance < min_distance:
                    min_distance = distance
                    nearest_dino = dino_color[1]
    else:
        for dino_color in obs['other_dino_colors']:
            if dino_color[0][0] >= 126 and dino_color[0][1] >= 126 and dino_color[0][2] >= 126:
                distance = abs(dino_color[1][0] - dino.dino_x) + abs(dino_color[1][1] - dino.dino_y) 
                if distance < min_distance:
                    min_distance = distance
                    nearest_dino = dino_color[1]

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
#define behaviors

#returns all valid positions not in walls
def valid_movement_avoiding_walls(dino, obs):
    possible_actions = ['left', 'right', 'up', 'down']
    valid_actions = []
    
    for action in possible_actions:
        if (action == 'left' and (dino.dino_x-1, dino.dino_y) not in dino.dino_walls) or \
        (action == 'right' and (dino.dino_x+1, dino.dino_y) not in dino.dino_walls) or \
        (action == 'up' and (dino.dino_x, dino.dino_y-1) not in dino.dino_walls) or \
        (action == 'down' and (dino.dino_x, dino.dino_y+1) not in dino.dino_walls):
            valid_actions.append(action)
    return valid_actions


    
