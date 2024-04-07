class Dinosaur:
    def __init__(self, **traits) -> None:
        #Stats
        self.currHealth = 100
        self.totalHealth = 100
        self.carnVal = 1
        self.herbVal = 1
        self.speed = 0
        self.energy = 0
        self.energyConsumption = 0
        self.power = 100
        
        #Features of this dinosaur
        self.defaultTraits = {
            'Size': None,
            'Mouth' : None,
            'Mobility' : None,
            'Combat' : None,
            'Neck' : None,
            'Tail' : None,
            }
        self.traits = {**self.defaultTraits, **traits}
        
        #Setting up speed
        self.speedModifiers = {
            'Large' : -1,
            'Medium' : 0,
            'Small' : 1,
            'Bipedal' : 1,
            'Quadruped' : -1,
            'Flying' : 1,
            None : 0,
            'Mobile Tail': 1,
            'Attack Tail' : -1,
            'Long' : -1}
        self.speed = 4 + self.speedModifiers[self.traits['Size']] + self.speedModifiers[self.traits['Mobility']] + self.speedModifiers[self.traits['Tail']] + self.speedModifiers[self.traits['Neck']]

        #Setting up energy
        self.energyModifier = {
            'Large' : 1.5,
            'Medium' : 1.25,
            'Small' : 1,
            'Bipedal' : 1,
            'Quadruped' : 1.25,
            'Flying' : 0.75,
            None : 0,
            'Long': 1}
        self.energy = 100 * self.energyModifiers[self.traits['Size']] * self.energyModifiers[self.traits['Mobility']] * self.energyModifiers[self.traits['Neck']]

        #Setting up Power
        self.powerModifier = {
            'Large' : 10,
            'Medium' : 5,
            'Small' : 2,
            }
        self.power *= self.energyModifiers[self.traits['Size']]

        #Setting up carnVal
        self.carnValModifier = {'Large' : 1,
                                'Medium' : 1,
                                'Small' : 0.66,
                                'Beak' : 1,
                                'Herbivore Teeth' : 0.5,
                                'Carnivore Teeth' : 1,
                                'Spikes' : 0.75,
                                'Horns' : 1,
                                'Claws': 1,
                                'Bipedal' : 1,
                                'Quadruped' : 1,
                                'Flying' : 1,
                                'Long' : 0.66,
                                None : 1,
                                'Mobile Tail' : 1,
                                'Attack Tail' : 1,}
        self.carnVal *= self.carnValModifier[self.traits['Size']] * self.carnValModifier[self.traits['Mouth']] \
        * self.carnValModifier[self.traits['Mobility']] * self.carnValModifier[self.traits['Combat']] * self.carnValModifier[self.traits['Neck']] * self.carnValModifier[self.traits['Tail']]

        #Setting up herbVal
        self.carnValModifier = {'Large' : 1,
                                'Medium' : 1,
                                'Small' : 0.66,
                                'Beak' : 1,
                                'Herbivore Teeth' : 0.5,
                                'Carnivore Teeth' : 1,
                                'Spikes' : 0.75,
                                'Horns' : 1,
                                'Claws': 1,
                                'Bipedal' : 1,
                                'Quadruped' : 1,
                                'Flying' : 1,
                                'Long' : 0.66,
                                None : 1,
                                'Mobile Tail' : 1,
                                'Attack Tail' : 1,}
        self.carnVal *= self.carnValModifier[self.traits['Size']] * self.carnValModifier[self.traits['Mouth']] \
        * self.carnValModifier[self.traits['Mobility']] * self.carnValModifier[self.traits['Combat']] * self.carnValModifier[self.traits['Neck']] * self.carnValModifier[self.traits['Tail']]
        
    def child(self,other):
        if self.energy > 20:
            new_traits = self.traits
            for i in new_traits.values():
                if i[1] == None:
                    new_traits[i[0]] = other.traits[i[0]]
            return Dinosaur(new_traits)
        else:
            return