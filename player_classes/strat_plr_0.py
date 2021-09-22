class StratPlayer():
    def __init__(self, stratagy):
        self.plr_num = None
        self.strat = stratagy

    def set_plr_num(self, n):
        self.strat.plr_num = n
        self.plr_num = n
    
    def set_data(self, plr_data, board) :
        self.strat.plr_data = plr_data
        self.strat.board = board

    def pick_translation(self, coord, choices):
        choice = self.strat.pick_translation(coord, choices)
        return choice

    def pick_opponent(self, ship, current_battle) :
        return self.strat.pick_opponent(ship, current_battle)
        