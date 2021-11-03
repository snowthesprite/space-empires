import sys
sys.path.append('player_classes')
sys.path.append('games')
sys.path.append('strats')
from game_1_1 import Game
from strat_plr_1 import StratPlayer
from strat_1 import StraightToEnemyColony
from william import Custom

players = [StratPlayer(Custom()), StratPlayer(StraightToEnemyColony())]
game = Game(players, '01vs_william')
game.run_to_completion()
#print(game.winner)
