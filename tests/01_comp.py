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

strats = [StraightToEnemyColony(), PriorityAttacker(), MoveToOpponent(), CompetitionStrat(), CaydenStrat(), Custom()]

all_wins = []

for plr_1 in range(len(names)) :
    for plr_2 in range(plr_1+1, len(names)) :
        wins = {names[plr_1] : 0, names[plr_2] : 0, 'tie': 0}
        players = [StratPlayer(strats[plr_1]), StratPlayer(strats[plr_2])]
        plr_names = [names[plr_1], names[plr_2], 'tie']
        #'''
        #print(plr_names)
        for _ in range(100) :
            game = Game(players, '01comp')
            game.run_to_completion()
            wins[plr_names[game.winner-1]] += 1
            plr_names.remove('tie')
            plr_names.reverse()
            players.reverse()
            plr_names.append('tie')
        all_wins.append(wins)
        print(wins, '\n\n')
        #'''