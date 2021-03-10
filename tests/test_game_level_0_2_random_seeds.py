import sys
sys.path.append('player_classes')
sys.path.append('games')
from game_0_2 import Game
from custom_player import CustomPlayer

tests = [
    {'seed': 0, 'winner': 2},
    {'seed': 1, 'winner': 1},
    {'seed': 2, 'winner': 2},
    {'seed': 3, 'winner': 1},
    {'seed': 4, 'winner': 1},
    {'seed': 5, 'winner': 2},
    {'seed': 6, 'winner': 2},
    {'seed': 7, 'winner': 1},
    {'seed': 8, 'winner': 1},
    {'seed': 9, 'winner': 1}
]

for test in tests:
    players = [CustomPlayer(), CustomPlayer()]
    random_seed = test['seed']

    game = Game(players, random_seed)
    game.run_to_completion()

    desired_winner = test['winner']
    assert(game.game_state['winner'] == desired_winner)