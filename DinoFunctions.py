import random


def calcFeatureScalar(dino):
    return -1


def eatOtherGuy(dino, calVal):
    dino.actionV += calVal*dino.carnVal

def eatPlant(dino, calVal):
    dino.actionV += calVal*dino.herbVal

def stepStill(dino):
    dino.actionV -= 1*dino.actionC

def stepMoveUp(dino):
    dino.actionV -= 2*dino.actionC
    

def stepMoveDown(dino):
    dino.actionV -= 2*dino.actionC
    
def stepMoveLeft(dino):
    dino.actionV -= 2*dino.actionC

def stepMoveRight(dino):
    dino.actionV -= 2*dino.actionC

def combatSimulation(dinoOne, dinoTwo):
    # power calculations:
    powerOne = dinoOne.size * (dinoOne.currHealth/dinoOne.totalHealth) * \
        random.randint(10, 100) * calcFeatureScalar(dinoOne) + dinoOne.attack
    powerTwo = dinoTwo.size * (dinoTwo.currHealth/dinoTwo.totalHealth) * \
        random.randint(10, 100) * calcFeatureScalar(dinoTwo) + dinoTwo.attack

    # generates for health calculations
    victorValue = random.randint(10, 200)

    # health value changes
    if (powerOne > powerTwo):
        if victorValue >= 100:
            dinoTwo.isAlive = False
            eatOtherGuy(dinoOne, dinoTwo.kcal)
        else:
            dinoTwo.currHealth = dinoTwo.currHealth * (victorValue/100) + dinoTwo.defense 
    elif (powerOne < powerTwo):
        if victorValue >= 100:
            dinoOne.isAlive = False
            eatOtherGuy(dinoTwo, dinoOne.kcal)
        else:
            dinoOne.currHealth = dinoOne.currHealth * (victorValue/100) + dinoOne.defense
    else:
        if victorValue >= 100:
            dinoTwo.isAlive = False
            dinoOne.isAlive = False
        else:
            dinoTwo.currHealth = dinoTwo.currHealth * (victorValue/100) + dinoTwo.defense
            dinoOne.currHealth = dinoTwo.currHealth * (victorValue/100) + dinoOne.defense
