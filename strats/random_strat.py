## Picks a random move and random enemy
from random import random
import math

class AllRandom () :
    def __init__(self) :
        self.plr_data = None
        self.plr_num = None
        self.board = None

    def pick_translation(self, coords, choices) :
        random_idx = math.floor(len(choices) * random())
        return choices[random_idx]

    def pick_opponent(self, ship, current_battle) :
        alt_id = (self.plr_num % 2) + 1
        random_idx = math.floor(len(current_battle[alt_id]) * random())
        enemy_id = current_battle[alt_id][random_idx]
        for enemy_ship in self.plr_data[alt_id]['ships'] :
            if enemy_ship.id == enemy_id :
                return enemy_ship
