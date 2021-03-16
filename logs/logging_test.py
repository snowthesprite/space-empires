from logger import *
import sys
sys.path.append('player_classes')
sys.path.append('games')
from game_0_3_1 import Game
from custom_playerMK2 import CustomPlayer

#logger = Logger('/home/runner/space-empires/logs/silly-log.txt')
#logger.write('stuff')

players = [CustomPlayer(), CustomPlayer()]
game = Game(players)
game.run_to_completion()