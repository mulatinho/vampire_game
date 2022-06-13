import sys
import vampire as vampire_game

def main():
    players = []
    vampires = []
    # for _ in range(50):
    #     personNew = Person()
    #     players.append(personNew)
    #     personNew.greet()

    # for _ in range(50):
    #     personNew = Vampire(player_generation=9)
    #     vampires.append(personNew)
    #     personNew.greet()

    human = vampire_game.players.Person()
    vampire = vampire_game.players.Vampire(player_generation=9)
    vampire_game.game.battle([human, vampire])

if __name__ == '__main__':
    main()
