from random import random
import math

class RandomPlayer():
    def __init__(self):
        self.player_number = None

    def set_player_number(self, n):
        self.player_number = n

    def choose_translation(self, game_state, choices):
        # `choices` is a list of possible translations,
        # e.g. [(0,0), (-1,0), (0,1)] if the player's
        # scout is in the bottom-right corner of the board

        random_idx = math.floor(len(choices) * random())
        return choices[random_idx]