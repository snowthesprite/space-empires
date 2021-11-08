import sys
sys.path.append('player_classes')
sys.path.append('games')
sys.path.append('strats')
from game_1_1 import Game
from strat_plr_1 import StratPlayer
from strat_1 import StraightToEnemyColony

from anton import PriorityAttacker
from charlie import MoveToOpponent
from justin import CompetitionStrat
from cayden import CaydenStrat
from william import Custom


names = ['Maia', 'Anton', 'Charlie', 'Justin', 'Cayden', 'William']

strats = [StraightToEnemyColony(), PriorityAttacker(), ]

for _ in range(100) :
    game = Game(players, '01vs_anton')
    game.run_to_completion()
    wins[names[game.winner-1]] += 1
    names.reverse()
    players.reverse()
#print(game.winner)
print(wins)