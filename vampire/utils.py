from random import randint, shuffle

FIRST_NAMES = [
    "John", "Armand", "Carlo", "Italo", "Lucas", "Carolina",
    "Cristina", "Adele", "Phillip", "Boris", "Katerina",
    "Ulysses", "Randal", "Arnold", "Nathaniel", "Bartholomew",
    "Abigale", "Yolanthe", "Ada", "Thalia", "Kafara"
]

LAST_NAMES = [
    "Beckett",  "Browne", "Klein", "Kimball", "Norman", "Payne",
    "Zimmerman", "Nuemann", "Cosimo", "MacQuoid", "Drogo", "Baratheon",
    "BAKER", "GONZALEZ", "CARTER", "MITCHELL", "PEREZ", "CAMPBELL", 
    "EDWARDS", "COLLINS", "STEWART", "SANCHEZ", "RIVERA", "TORRES",
    "RAMIREZ"
]

def roll(dice_size=10, times=1, difficult=6):
    dice_rolls = []
    result = 0
    for i in range(1, times + 1):
        dice_result = randint(1, dice_size+1)
        if dice_result >= difficult:
            result += 1
        elif dice_result == 1:
            result -= 1
        dice_rolls.append(dice_result)
    return (result, dice_rolls, difficult)

def define_name():
    full_name = ""
    names_size = len(FIRST_NAMES)
    choosen_number = randint(0, names_size - 1)

    full_name = str(FIRST_NAMES[choosen_number]).capitalize()
    names_size = len(LAST_NAMES)
    choosen_number = randint(0, names_size - 1)

    full_name = full_name + " " + str(LAST_NAMES[choosen_number]).capitalize()
    return full_name