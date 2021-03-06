''''
players = [CustomPlayer(), CustomPlayer()]
>>> game = Game(players)
>>> game.state['players']
{
    1: {
        'scout_coords': (4, 1),
        'home_colony_coords': (4, 1)
    },
    2: {
        'scout_coords': (4, 7),
        'home_colony_coords': (4, 7)
    }
}

>>> game.complete_movement_phase()
>>> game.state['players']
{
    1: {
        'scout_coords': (4, 5),
        'home_colony_coords': (4, 1)
    },
    2: {
        'scout_coords': (4, 6),
        'home_colony_coords': (4, 7)
    }
}

>>> game.complete_combat_phase()
Nothing changes since no units occupy the same location

>>> game.complete_movement_phase()
>>> game.state['players']
{
    1: {
        'scout_coords': (4, 6),
        'home_colony_coords': (4, 1)
    },
    2: {
        'scout_coords': (4, 6),
        'home_colony_coords': (4, 7)
    }
}

Note that player 2's scout cannot move anywhere since
player 1's scout has moved into its coordinates

>>> game.complete_combat_phase()
One of the scouts is randomly selected to be destroyed.

>>> game.state['players']
There are two possible outcomes:

Possibility 1:
{
    1: {
        'scout_coords': None,
        'home_colony_coords': (4, 1)
    },
    2: {
        'scout_coords': (4, 6),
        'home_colony_coords': (4, 7)
    }
}

Possibility 2:
{
    1: {
        'scout_coords': (4, 6),
        'home_colony_coords': (4, 1)
    },
    2: {
        'scout_coords': None,
        'home_colony_coords': (4, 7)
    }
}
Test B

>>> num_wins = {1: 0, 2: 0}
>>> for _ in range(200):
        players = [CustomPlayer(), CustomPlayer()]
        game = Game(players)
        game.run_to_completion()
        winner = game.state['winner']
        num_wins[winner] += 1

>>> num_wins
Should be close (but probably not exactly equal) 
to {1: 100, 2: 100}

You shouldn't get a deviation more than +/- 20,
meaning that

Something like {1: 80, 2: 120} would be fine

But something like {1: 40, 2: 160} would mean 
something's wrong
'''