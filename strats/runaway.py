## Trys to run off the board

class Runaway () :
    def __init__(self, wait) :
        self.plr_data = None
        self.plr_num = None
        self.board = None

    def pick_translation(self, coord, choices) :
        return (0,-1)

    def pick_opponent(self, ship, current_battle) :
        alt_id = (self.plr_num % 2) + 1
        return (alt_id, current_battle[alt_id][0])