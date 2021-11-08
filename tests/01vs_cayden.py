import sys
sys.path.append('player_classes')
sys.path.append('games')
sys.path.append('strats')
from game_1_1 import Game
from strat_plr_1 import StratPlayer
from strat_1 import StraightToEnemyColony
from cayden import CaydenStrat

players = [StratPlayer(CaydenStrat()), StratPlayer(StraightToEnemyColony())]

names = ['Me', 'Cayden']

wins = {'Cayden': 0, 'Me': 0}

print('Cayden')

for _ in range(100) :
    game = Game(players, '01vs_cayden')
    game.run_to_completion()
    wins[names[game.winner-1]] += 1
    names.reverse()
    players.reverse()
#print(game.winner)
print(wins)

