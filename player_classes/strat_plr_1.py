class StratPlayer():
    def __init__(self, stratagy):
        self.strat = stratagy
        self.plr_num = None

    def set_plr_num(self, n):
        self.strat.plr_num = n
        self.plr_num = n
    
    def set_data(self, plr_data, board) :
        board_copy = {}

        board_items = list(board.items())
        board_items.extend([(plr_data[1]['Home Colony'], []), (plr_data[2]['Home Colony'], [])])
        
        for coords, ships in board_items :
            if coords in list(board_copy) :
                continue
            board_copy[coords] = []
            for (plr_id, ship_id) in ships :
                for ship in plr_data[plr_id]['ships'] :
                    if ship.id == ship_id :
                        ship_dict = ship.class_to_dict(coords)
                        board_copy[coords].append(ship_dict)
                        break

        board_copy[plr_data[1]['Home Colony']].insert(0,{'player_num': 1, 'obj_type': 'colony'})
        board_copy[plr_data[2]['Home Colony']].insert(0,{'player_num': 2, 'obj_type': 'colony'})

        self.strat.simple_board = board_copy

    def choose_translation(self, ship, coord, choices):
        ship_info = ship.class_to_dict(coord)
        choice = self.strat.choose_translation(ship_info, choices)
        if choice not in choices :
            return (0,0)
        return choice

    def choose_opponent(self, ship, current_battle) :
        coord = current_battle[0]['coords']
        ship_info = ship.class_to_dict(coord)
        enemy = self.strat.choose_target(ship_info, current_battle)
        enemy_ref = (enemy['player_num'], enemy['name'] + str(enemy['ship_num']))
        return enemy_ref
        