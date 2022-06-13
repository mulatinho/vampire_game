from random import randint, shuffle

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
