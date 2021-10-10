class StratPlayer():
    def __init__(self, stratagy):
        self.strat = stratagy
        self.plr_num = None

    def set_plr_num(self, n):
        self.strat.plr_num = n
        self.plr_num = n
    
    def set_data(self, plr_data, board) :
        plr_data_copy = {plr_num : 
            {'Home Colony' : 
                plr_data[plr_num]['Home Colony'],
                'ships' : [] }
                for plr_num in range(1,3) }
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
                        plr_data_copy[plr_id]['ships'].append(ship_dict)
                        break

        board_copy[plr_data[1]['Home Colony']].insert(0,{'obj_type': 'colony'})
        board_copy[plr_data[2]['Home Colony']].insert(0,{'obj_type': 'colony'})

        self.strat.plr_data = plr_data_copy
        self.strat.board = board_copy

    def pick_translation(self, ship, coord, choices):
        ship_info = ship.class_to_dict(coord)
        choice = self.strat.pick_translation(ship_info, choices)
        if choice not in choices :
            return (0,0)
        return choice

    def pick_opponent(self, ship, current_battle) :
        coord = current_battle[0]['coords']
        ship_info = ship.class_to_dict(coord)
        enemy = self.strat.pick_opponent(ship_info, current_battle)
        enemy_ref = (enemy['player_num'], enemy['name'] + str(enemy['ship_num']))
        return enemy_ref
        