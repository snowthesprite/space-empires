import sys
sys.path.append('player_classes')
sys.path.append('games')
from game_0_3 import Game
from custom_playerMK2 import CustomPlayer

num_wins = {1: 0, 2: 0}
scouts_remaining = {1: 0, 2: 0}
for _ in range(200):
        players = [CustomPlayer(), CustomPlayer()]
        game = Game(players)
        game.run_to_completion()
        winner = game.game_state['winner']
        for scout in game.game_state['players'][winner]['scout_coords'].values() :
            if scout != None :
                scouts_remaining[winner] += 1

        num_wins[winner] += 1
avg_scouts_remaining = {k:v/200 for k,v in scouts_remaining.items()}

print(num_wins)
### Should be close (but probably not exactly equal) 
### to {1: 100, 2: 100}

### You shouldn't get a deviation more than +/- 20,
### meaning that

### Something like {1: 80, 2: 120} would be fine

### But something like {1: 40, 2: 160} would mean 
### something's wrong

print(avg_scouts_remaining)
### Should be close (but probably not exactly equal) 
### to {1: 0.9, 2: 0.9}

### Something like {1: 0.7, 2: 1.1} would be fine

### But something like {1: 0.3, 2: 1.5} would mean 
### something's wrong