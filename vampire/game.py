from random import randint, shuffle
import time
from . import players
from . import utils

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

HEALTH = [
    { "name": "Bruised", "penalty": 0 },
    { "name": "Bruised", "penalty": 0 },
    { "name": "Hurted", "penalty": -1  },
    { "name": "Hurted", "penalty": -1  },
    { "name": "Injured", "penalty": -1  },
    { "name": "Injured", "penalty": -1  },
    { "name": "Wounded", "penalty": -2  },
    { "name": "Wounded", "penalty": -2  },
    { "name": "Mauled", "penalty": -2  },
    { "name": "Mauled", "penalty": -2  },
    { "name": "Crippled", "penalty": -5  },
    { "name": "Crippled", "penalty": -5  },
    { "name": "Incapacitated", "penalty": -10 },
    { "name": "Incapacitated", "penalty": -10 },
    { "name": "Dead", "penalty": -100 }
]

HEALTH_TOTAL = 14

HEALTH_BRUISED = 12
HEALTH_HURTED = 10
HEALTH_INJURED = 8
HEALTH_WOUNDED = 6
HEALTH_MAULED = 6
HEALTH_CRIPPLED = 4
HEALTH_INCAPACITATED = 2
HEALTH_DEAD = 0

BLOOD_HEALTH = 0
BLOOD_SKILL = 0
BLOOD_DISCIPLINE = 0

ATTACK_BASHING = 1
ATTACK_LETHAL = 2
ATTACK_AGGRAVATED = 3

def battle(opponents=[]):
    end_battle = False
    print(f'there is a battle starting... ')
    if opponents[0] is None or opponents[1] is None:
        return None
    opponents[0].greet()
    opponents[1].greet()
    while not end_battle:
        index_first = 0
        print('')
        player_one_dice = utils.roll(10, opponents[0].initiative())
        print(f'{opponents[0].name} rolling a dice for inititive {player_one_dice}...')
        player_two_dice = utils.roll(10, opponents[1].initiative())
        print(f'{opponents[1].name} rolling a dice for inititive {player_two_dice}...')
        if player_one_dice[0] == player_two_dice[0]:
            index_first = randint(0, 1)
        elif player_two_dice[0] > player_one_dice[0]:
            index_first = 1
        # print(f'-- player_one_dice {player_one_dice[0]} vs player_two_dice {player_two_dice[0]} index_first is {index_first}')
        for _ in range(len(opponents)):
            player = opponents[index_first % len(opponents)]
            player_dice = utils.roll(10, player.punch() - player.dice_penalty())
            print(f'{player.name} rolling a dice for attack {player_dice}...')
            if player_dice[0] > 0:
                enemy = opponents[(index_first + 1) % len(opponents)]
                enemy_dice = utils.roll(10, enemy.absorb() - enemy.dice_penalty())
                print(f'{enemy.name} rolling a dice for absorb {enemy_dice}...')
                damage = player_dice[0] - enemy_dice[0]
                if damage < 0:
                    damage = 0
                total_damage = enemy.damage(damage)
                player.current_status()
                enemy.current_status()
                if enemy.is_dead():
                    print(f'-> The {enemy.player_type} with name {enemy.name} died!')
                    end_battle = True
                    break
                elif total_damage == 0:
                    print(f'-> The enemy {enemy.name} absorbed the attack from {player.name}!')
                else:
                    print(f'-> The player {player.name} attacked {enemy.name} inflicting {total_damage} points')
            index_first += 1

        time.sleep(1.5)
