class dinosaur:
    def __init__(self, **traits) -> None:
        #Stats
        self.currentHealth = 0
        self.totalHealth = 100
        self.carnivore_scalar = 0
        self.herbivore_scalar = 0
        self.speed = 0
        self.energy = 0
        self.energyConsumption = 0
        
        #Features of this dinosaur
        self.defaultTraits = {'Size': None,
                       'Mouth' : None,
                       'Mobility' : None,
                       'Combat' : None,
                       'Neck' : None,
                       'Tail' : None,
                       }
        self.traits = {**self.defaultTraits, **traits}
        
        self.healthModifiers = {'Large' : 1.5,
                                'Medium' : 1.25,
                                'Small' : 1.0,
                                'Bipedal' : 1.0,
                                'Quadruped' : 1.25,
                                'Flying': }

    def child(self,other):
        