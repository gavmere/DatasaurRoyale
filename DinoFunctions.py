import random

def eatOtherGuy(dino, calVal):
    dino.energy += calVal*dino.carnVal * 2

def eatPlant(dino, calVal):
    dino.energy += calVal*dino.herbVal

def stepStill(dino):
    dino.energy -= 1*dino.energyConsumption / dino.speed

def stepMoveUp(dino):
    dino.energy -= 2*dino.energyConsumption / dino.speed
    

def stepMoveDown(dino):
    dino.energy -= 2*dino.energyConsumption / dino.speed
    
def stepMoveLeft(dino):
    dino.energy -= 2*dino.energyConsumption / dino.speed

def stepMoveRight(dino):
    dino.energy -= 2*dino.energyConsumption / dino.speed

def combatSimulation(dinoOne, dinoTwo):
    # power calculations:
    powerOne = dinoOne.power * (dinoOne.currHealth/dinoOne.totalHealth) * \
        random.randint(10, 100) 
    powerTwo = dinoTwo.power * (dinoTwo.currHealth/dinoTwo.totalHealth) * \
        random.randint(10, 100)

    # generates for health calculations
    victorValue = random.randint(10, 200)

    # health value changes
    if (powerOne > powerTwo):
        if victorValue >= 100:
            dinoTwo.isAlive = False
            eatOtherGuy(dinoOne, dinoTwo.energyConsumption)
        else:
            dinoTwo.currHealth = dinoTwo.currHealth * (victorValue/100) 
    elif (powerOne < powerTwo):
        if victorValue >= 100:
            dinoOne.isAlive = False
            eatOtherGuy(dinoTwo, dinoOne.energyConsumption)
        else:
            dinoOne.currHealth = dinoOne.currHealth * (victorValue/100) 
    else:
        if victorValue >= 100:
            dinoTwo.isAlive = False
            dinoOne.isAlive = False
        else:
            dinoTwo.currHealth = dinoTwo.currHealth * (victorValue/100) 
            dinoOne.currHealth = dinoTwo.currHealth * (victorValue/100)
