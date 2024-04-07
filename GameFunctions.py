import DinoFunctions
import Dinosaur
import random

def pickSize():
    sizeList = ['Small', 'Medium', 'Large']
    return random.choice(sizeList)

def pickMouth():
    mouthList = ['Beak', 'Medium', 'Large']
    return random.choice(mouthList)

def pickMobility():
    mobilityList = ['Bipedal', 'Quadruped', 'Flying']
    return random.choice(mobilityList)

def pickCombat():
    combatList = ['Spikes', 'Horns', 'Claws']
    return random.choice(combatList)

def pickNeck():
    neckList = ['longNeck', 'normNeck']
    return random.choice(neckList)

def pickTail():
    tailList = ['noTail', 'Mobile Tail', 'Attack Tail']
    return random.choice(tailList)


def createDino():
    newDino = Dinosaur.dinosaur([])
    return newDino

def populateDinoList(num, parent=None):
    dinoList = []
    for i in range(num):
        ...
    return dinoList
    
