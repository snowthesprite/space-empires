import sys
sys.path.append('player_classes')
sys.path.append('games')
from game_1_0 import Game
from random_playerMK2 import RandomPlayer

players = [RandomPlayer(), RandomPlayer()]
game = Game(players)
game.run_to_completion()
print(game.winner)