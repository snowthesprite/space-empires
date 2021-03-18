import sys
sys.path.append('player_classes')
sys.path.append('games')
from game_0_4 import Game
from custom_playerMK2 import CustomPlayer

players = [CustomPlayer(), CustomPlayer()]
game = Game(players)
game.run_to_completion()