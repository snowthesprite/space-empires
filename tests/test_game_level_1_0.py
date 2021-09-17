import sys
sys.path.append('player_classes')
sys.path.append('games')
from game_1_0 import Game
from strat_plr_0 import CustomPlayer
from random_playerMK2 import RandomPlayer

players = [RandomPlayer(), RandomPlayer()]
#players = [CustomPlayer(), RandomPlayer()]
game = Game(players)
game.run_to_completion()
print(game.winner)