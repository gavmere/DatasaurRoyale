import random


def calcFeatureScalar(dino):
    return -1


def eatOtherGuy(dino, calVal):
    dino.energy += calVal*dino.carnVal
    return


def eatPlant(dino, calVal):
    dino.energy += calVal*dino.herbVal
    return


def combatSimulation(dinoOne, dinoTwo):
    # power calculations:
    powerOne = dinoOne.size * (dinoOne.currHealth/dinoOne.totalHealth) * \
        random.randint(10, 100) * calcFeatureScalar(dinoOne) + dinoOne.attack
    powerTwo = dinoTwo.size * (dinoTwo.currHealth/dinoTwo.totalHealth) * \
        random.randint(10, 100) * calcFeatureScalar(dinoTwo) + dinoTwo.attack

    # generates for health calculations
    victorValue = random.randint(10, 200)

    # if you're reading this suck my nuts this is just health value changes
    if (powerOne > powerTwo):
        if victorValue >= 100:
            dinoTwo.isAlive = False
            eatOtherGuy(dinoOne, dinoTwo.kcal)
        else:
            dinoTwo.currHealth = dinoTwo.currHealth * (victorValue/100)
    elif (powerOne < powerTwo):
        if victorValue >= 100:
            dinoOne.isAlive = False
            eatOtherGuy(dinoTwo, dinoOne.kcal)
        else:
            dinoOne.currHealth = dinoTwo.currHealth * (victorValue/100)
    else:
        if victorValue >= 100:
            dinoTwo.isAlive = False
            dinoOne.isAlive = False
        else:
            dinoTwo.currHealth = dinoTwo.currHealth * (victorValue/100)
            dinoOne.currHealth = dinoTwo.currHealth * (victorValue/100)
