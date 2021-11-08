import sys
sys.path.append('player_classes')
sys.path.append('games')
sys.path.append('strats')
from game_1_1 import Game
from strat_plr_1 import StratPlayer
from strat_1 import StraightToEnemyColony
from william import Custom

players = [StratPlayer(Custom()), StratPlayer(StraightToEnemyColony())]

names = ['Me', 'William']

wins = {'William': 0, 'Me': 0}

print('William')

for _ in range(100) :
    game = Game(players, '01vs_william')
    game.run_to_completion()
    wins[names[game.winner-1]] += 1
    names.reverse()
    players.reverse()
#print(game.winner)
print(wins)
