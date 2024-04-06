class dinosaur:
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
            'Attack Tail' : -1}
        self.speed = 4 + self.speedModifiers[self.traits['Size']] + self.speedModifiers[self.traits['Mobility']] + self.speedModifiers[self.traits['Tail']]

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

        self.powerModifier = {
            'Large' : 10,
            'Medium' : 5,
            'Small' : 2,
            }
        self.power *= self.energyModifiers[self.traits['Size']]
        
    def child(self,other):
        ...    