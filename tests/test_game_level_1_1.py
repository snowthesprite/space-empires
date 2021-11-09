import sys
sys.path.append('player_classes')
sys.path.append('games')
sys.path.append('strats')
from game_1_1 import Game
from strat_plr_1 import StratPlayer
from strat_1 import StraightToEnemyColony
from battle_strat_0_1 import BattleStrat

'''
players = [StratPlayer(StraightToEnemyColony()), StratPlayer(StraightToEnemyColony())]
game = Game(players)
game.run_to_completion()
#print(game.winner)
#'''

##Testing battle_strat_0_1
players = [StratPlayer(StraightToEnemyColony()), StratPlayer(BattleStrat())]
''''
game = Game(players)
game.run_to_completion()
print(game.winner)
#'''

#''''
names = ['Straight', 'Battle']

wins = {'Straight': 0, 'Battle': 0}

for _ in range(1000) :
    game = Game(players)
    game.run_to_completion()
    wins[names[game.winner-1]] += 1
    names.reverse()
    players.reverse()
#print(game.winner)
print(wins)
#'''