class StratPlayer():
    def __init__(self, stratagy):
        self.plr_num = None
        self.strat = stratagy

    def set_plr_num(self, n):
        self.strat.plr_num = n
        self.plr_num = n
    
    def set_data(self, plr_data, board) :
        plr_data_copy = {plr_num : 
            {'Home Colony' : 
                (plr_data[plr_num]['Home Colony'][0],plr_data[plr_num]['Home Colony'][1]),
                'ships' : [(ship.id, ship.hp) 
                for ship in plr_data[plr_num]['ships']]}
                for plr_num in range(1,3) }
        board_copy = {coord : [(plr_num, ship_id) for plr_num, ship_id in board[coord]] for coord in board.keys()}

        self.strat.plr_data = plr_data_copy
        self.strat.board = board_copy

    def pick_translation(self, coord, choices):
        choice = self.strat.pick_translation(coord, choices)
        return choice

    def pick_opponent(self, ship, current_battle) :
        return self.strat.pick_opponent(ship, current_battle)
        