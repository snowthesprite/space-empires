## Complatable w/ game 1.2
import sys
sys.path.append('ships')
from ship_data import *

class StratPlayer():
    def __init__(self, stratagy):
        self.strat = stratagy
        self.plr_num = None
        self.cp = 200
    
    def buy_ships(self) :
        checkout = self.strat.buy_ships(self.cp)
        total_cost = 0
        for ship in all_ship_infos :
            if ship['name'] in checkout.keys() :
                for _ in range(checkout[ship['name']]) :
                    total_cost += ship['cp_cost']
        if self.cp - total_cost < 0 :
            return {}
        return checkout

    def set_start_data(self, n, cp):
        self.plr_num = n
        self.cp = cp
    
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

        board_copy[plr_data[1]['Home Colony']].insert(0,{'player_num': 1, 'obj_type': 'Colony', 'is_home_colony': True, 'coords': plr_data[1]['Home Colony']})
        board_copy[plr_data[2]['Home Colony']].insert(0,{'player_num': 2, 'obj_type': 'Colony', 'is_home_colony': True, 'coords': plr_data[2]['Home Colony']})
        #print(self.plr_num)
        #print(board, '\n\n')

        self.strat.simple_board = board_copy

    def update_data(self, ship_info, coords, mvmt) :
        new_coords = (coords[0]+mvmt[0], coords[1]+mvmt[1])

        self.strat.simple_board[coords].remove(ship_info)

        ship_info['coords'] = new_coords

        if new_coords not in list(self.strat.simple_board) :
            self.strat.simple_board[new_coords] = [ship_info]
        else :
            self.strat.simple_board[new_coords].append(ship_info)

    def choose_translation(self, ship, coord, choices):
        ship_info = ship.class_to_dict(coord)
        choice = self.strat.choose_translation(ship_info, choices)
        self.update_data(ship_info, coord, choice)
        if choice not in choices : 
            return (0,0)
            print('Bad Move Plr {}'.format(self.plr_num))
        return choice

    def choose_opponent(self, ship, current_battle) :
        coord = current_battle[0]['coords']
        ship_info = ship.class_to_dict(coord)
        enemy = self.strat.choose_target(ship_info, current_battle)
        enemy_ref = (enemy['player_num'], enemy['ship_id'])
        return enemy_ref
        