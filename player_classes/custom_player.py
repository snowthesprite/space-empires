from random import random
import math

class CustomPlayer():
    def __init__(self):
        self.player_number = None

    def set_player_number(self, n):
        self.player_number = n

    def get_opponent_player_number(self):
        if self.player_number == None:
            return None
        elif self.player_number == 1:
            return 2
        elif self.player_number == 2:
            return 1

    def choose_translation(self, game_state, choices):
        myself = game_state['players'][self.player_number]
        opponent_player_number = self.get_opponent_player_number()
        opponent = game_state['players'][opponent_player_number]

        my_scout_coords = myself['scout_coords']
        opponent_home_colony_coords = opponent['home_colony_coords']

        dist_sqr = (my_scout_coords[0] - opponent_home_colony_coords[0]) ** 2 + (my_scout_coords[1] - opponent_home_colony_coords[1]) ** 2
        best_movement = None

        for choice in choices :
            option = (choice[0] + my_scout_coords[0], choice[1] + my_scout_coords[1])
            option_dist_sqr = (option[0] - opponent_home_colony_coords[0]) ** 2 + (option[1] - opponent_home_colony_coords[1]) ** 2
            if option_dist_sqr < dist_sqr :
                best_movement = choice
                dist_sqr = option_dist_sqr

        return best_movement