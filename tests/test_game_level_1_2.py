import sys
sys.path.append('player_classes')
sys.path.append('games')
sys.path.append('strats')
from game_1_2 import Game
from strat_plr_2 import StratPlayer
from tester_strat import TestStrat
from battle_strat_0_2 import BattleStrat
from dummy_strat import DummyStrat
from william import WallStrat

#print([chr(i) for i in range(ord('A'),ord('E')+1)])

## Test Game Works
''''
players = [StratPlayer(TestStrat()), StratPlayer(TestStrat())]
game = Game(players)
game.run_to_completion()
print(game.winner)
#'''

#''''
players = [StratPlayer(WallStrat()), StratPlayer(BattleStrat())]
names = ['Dummy', 'Battle', 'tie']

wins = {'Dummy': 0, 'Battle': 0, 'tie': 0}

for _ in range(1) :
    if _ % 100 == 0 :
        print(_)
    game = Game(players)
    game.run_to_completion()
    wins[names[game.winner-1]] += 1
    names.remove('tie')
    names.reverse()
    players.reverse()
    names.append('tie')
print(wins, '\n\n')
        #'''
#'''