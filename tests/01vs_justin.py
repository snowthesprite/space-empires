import sys
sys.path.append('player_classes')
sys.path.append('games')
sys.path.append('strats')
from game_1_1 import Game
from strat_plr_1 import StratPlayer
from strat_1 import StraightToEnemyColony
from justin import MoveToClosestCol

players = [StratPlayer(StraightToEnemyColony()), StratPlayer(MoveToClosestCol())]
game = Game(players, '01vs_justin')
game.run_to_completion()
#print(game.winner)