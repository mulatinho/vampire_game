from random import randint, shuffle
from . import game
from . import utils

class Sheet:
    '''
    attributes
    # force, dexterity, stamina
    # charisma, manipulation, appearence
    # perception, inteligence, wits

    abilities:
    # alertness, athletics, brawl, dodge, intimidation
    # animal ken, drive, firearms, melee, stealth
    # academics, finance, investigation, medicine, occult
    '''
    name = ""
    player_type = "Human"
    player_generation = 13
    health = 0
    humanity = 0
    willpower = 0
    bloodpool = 0
    blood = randint(4, 10)
    dead = False
    attributes = []
    abilities = []

    def __init__(self, random_player=False, player_type="Human", player_generation=13):
        self.attributes = [
            [ 0, 0, 0 ], 
            [ 0, 0, 0 ],
            [ 0, 0, 0 ]
        ]
        self.abilities = [
            [ 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0 ]
        ]
        self.create_player(random_player, player_type, player_generation)

    def create_player(self, random_player=False, player_type="Human", player_generation=13):
        points_table_attr = [ 7, 5, 3 ]
        points_table_abil = [ 9, 7, 5 ]

        self.name = utils.define_name()
        self.player_type = player_type
        self.bloodpool = 10
        self.willpower = randint(3, 10)
        self.health = 14

        if self.player_type == "Human":
            self.humanity = randint(5, 9)
        elif self.player_type == "Vampire":
            self.bloodpool = 10 + (13 - player_generation)
            self.humanity = randint(3, 8)
        self.blood = randint(6, self.bloodpool)
        if random_player:
            shuffle(points_table_attr)
            shuffle(points_table_abil)
        self.distribute_points(self.attributes, points_table_attr)
        self.distribute_points(self.abilities, points_table_abil)

    def distribute_points(self, points=None, points_table=[]):
        loop = 0
        if points == None or points_table == []:
            return None
        for points_total in points_table:
            while points_total != 0:
                n = randint(0, len(points) - 1)
                if points[loop][n] >= 4 and self.player_type == "Human":
                    # print(f"continue {n} points[{loop}][{n}] = {points[loop][n]}, points_total = {points_total}")
                    # print(points)
                    # time.sleep(1)
                    continue

                points[loop][n] += 1
                points_total -= 1
            loop += 1



    def dice_penalty(self):
        return game.HEALTH[game.HEALTH_TOTAL - self.get_health()]['penalty']

    def greet(self):
        print(f'-> action: the {self.player_type} with name {self.name} says "Hello.."')
        print(f':. - attrs   -> force: {self.attributes[0][0]}, dexterity: {self.attributes[0][1]}, stamina: {self.attributes[0][2]}')
        print(f':. - attrs   -> charisma: {self.attributes[1][0]}, manipulation: {self.attributes[1][1]}, appearence: {self.attributes[1][2]}')
        print(f':. - attrs   -> perception: {self.attributes[2][0]}, inteligence: {self.attributes[2][1]}, wits: {self.attributes[2][2]}')
        print(f':. - abils   -> alertness: {self.abilities[0][0]}, athletics: {self.abilities[0][1]}, brawl: {self.abilities[0][2]}, dodge: {self.abilities[0][3]}, intimidation: {self.abilities[0][4]}')
        print(f':. - abils   -> animal ken: {self.abilities[1][0]}, drive: {self.abilities[1][1]}, firearms: {self.abilities[1][2]}, melee: {self.abilities[1][3]}, stealth: {self.abilities[1][4]}')
        print(f':. - abils   -> academics: {self.abilities[2][0]}, finance: {self.abilities[2][1]}, investigation: {self.abilities[2][2]}, medicine: {self.abilities[2][3]}, occult: {self.abilities[2][4]}')
        print(f':. [{self.name}] -> health: {self.health}, is_dead: {self.dead}, humanity: {self.humanity}, willpower: {self.willpower}, bloodpool: {self.bloodpool} / {self.blood}, penalty: {self.dice_penalty()}')

    def current_status(self):
        print(f':. {self.player_type} "{self.name}" -> health: {self.health}, is_dead: {self.dead}, humanity: {self.humanity}, willpower: {self.willpower}, bloodpool: {self.bloodpool} / {self.blood}, penalty: {self.dice_penalty()}')

class Person(Sheet):
    def is_dead(self):
        return self.dead

    def initiative(self):
        return (self.attributes[0][1] + self.attributes[2][2])

    def punch(self):
        return self.attributes[0][0] + 1

    def damage(self, amount, damage_type=game.ATTACK_BASHING):
        total_attack = 0
        if (self.health - amount) <= 0:
            self.health = 0
            self.dead = True
        else:
            total_attack = round(amount / 2)
            if damage_type == game.ATTACK_AGGRAVATED:
                total_attack = amount
            self.health -= total_attack
        self.sobrenatural()
        return total_attack

    def absorb(self, damage_type=game.ATTACK_BASHING):
        if damage_type != game.ATTACK_BASHING and self.player_type == "Human":
            return 0
        return self.attributes[0][2]

    def get_blood(self):
        return self.blood

    def get_health(self):
        return self.health

    def sobrenatural(self):
        pass

class Human(Person):
    pass


class Vampire(Person):
    def __init__(self, **kwargs):
        super().__init__(self, player_type="Vampire", **kwargs)
        #self.player_type = "Vampire"
        self.bloodpool = 10 + (13 - self.player_generation)
        self.vampire_bonus(1)

    def vampire_bonus(self, bonus):
        attr_size = len(self.attributes) - 1
        elem_size = len(self.attributes[0]) - 1
        for i in range(attr_size):
            for j in range(elem_size):
                self.attributes[i][j] += 1

    def spend_blood(self, amount=1, motive=game.BLOOD_HEALTH):
        if not self.is_hungry():
            self.blood -= 1
            if motive == game.BLOOD_HEALTH:
                print(f'-> Vampire "{self.name}" spent {amount} blood on Health')
                self.health += 2
            elif motive == game.BLOOD_DISCIPLINE:
                print(f'-> Vampire "{self.name}" spent {amount} blood activating Discipline')
            else:
                print(f'-> Vampire "{self.name}" spent {amount} blood increasing Attributes')
        else:
            print(f'-> Vampire "{self.name}" is Hungry (blood: {self.blood}) and not willing to spend blood')
        return self.blood

    def is_hungry(self):
        if self.blood < 5:
            return True
        return False

    def sobrenatural(self):
        if self.get_health() <= game.HEALTH_INJURED:
            self.spend_blood(motive=game.BLOOD_HEALTH)


class Faction:
    __name = ""
    __members = []
    __leaders = []

    def __init__(self, name=None):
        self.__name = name
        print(f'Faction {name}')

    def create_member(self, member):
        self.__members.append(member)

    def create_leader(self, leader):
        self.__leaders.append(leader)

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def size_leaders(self):
        return len(self.__leaders)

    def size_members(self):
        return len(self.__members)