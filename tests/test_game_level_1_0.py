import sys
sys.path.append('player_classes')
sys.path.append('games')
sys.path.append('strats')
from game_1_0 import Game
from strat_plr_0 import StratPlayer
from wait import WaitToAttack
from runaway import Runaway
#from random_strat import AllRandom

players = [StratPlayer(WaitToAttack(3)), StratPlayer(WaitToAttack(3))]
game = Game(players)
game.run_to_completion()
print(game.winner)

players = [StratPlayer(Runaway()), StratPlayer(Runaway())]
game = Game(players)
game.run_to_completion()
#print(game.winner)
