import DinoFunctions
import Dinosaur
import random

def pickSize():
    sizeList = ['Small', 'Medium', 'Large']
    return random.choice(sizeList)

def pickMouth():
    mouthList = ['Beak', 'Herbivore Teeth', 'Carnivore Teeth']
    return random.choice(mouthList)

def pickMobility():
    mobilityList = ['Bipedal', 'Quadruped', 'Flying']
    return random.choice(mobilityList)

def pickCombat():
    combatList = [None, 'Spikes', 'Horns', 'Claws']
    return random.choice(combatList)

def pickNeck():
    neckList = ['Long', None]
    return random.choice(neckList)

def pickTail():
    tailList = [None, 'Mobile Tail', 'Attack Tail']
    return random.choice(tailList)


def createDino():
    newDino = Dinosaur.Dinosaur(Size = pickSize(), Mouth = pickMouth(), Mobility = pickMobility(), Combat = pickCombat(), Neck = pickNeck(), Tail = pickTail())
    return newDino

def populateDinoList(num, parent=None):
    dinoList = []
    for i in range(num):
        dinoList.append(createDino())
    return dinoList
    
