## Calculates the shortest distance and moves along that path not caring about running into enemies. Whopp attacking it will pick the first opp
## Compatable w/ strat_plr_1
class StraightToEnemyColony () :
    def __init__(self) :
        self.plr_data = None
        self.plr_num = None
        self.board = None

    def update_data(self, ship_info, mvmt) :
        old_coords = ship_info['coords']
        new_coords = (old_coords[0]+mvmt[0], old_coords[1]+mvmt[1])

        self.plr_data[ship_info['player_num']]['ships'].remove(ship_info)
        self.board[old_coords].remove(ship_info)

        ship_info['coords'] = new_coords

        self.plr_data[ship_info['player_num']]['ships'].append(ship_info)
        if new_coords not in list(self.board) :
            self.board[new_coords] = [ship_info]
        else :
            self.board[new_coords].append(ship_info)

    def pick_translation(self, ship_info, choices) :
        myself = self.plr_data[self.plr_num]
        opp_plr_num = (self.plr_num % 2) + 1
        opp = self.plr_data[opp_plr_num]

        my_ship_coords = ship_info['coords']
        opp_home_col_coords = opp['Home Colony']

        dist_sqr = (my_ship_coords[0] - opp_home_col_coords[0]) ** 2 + (my_ship_coords[1] - opp_home_col_coords[1]) ** 2
        best_mvmt = None

        for choice in choices :
            option = (choice[0] + my_ship_coords[0], choice[1] + my_ship_coords[1])
            option_dist_sqr = (option[0] - opp_home_col_coords[0]) ** 2 + (option[1] - opp_home_col_coords[1]) ** 2
            if option_dist_sqr <= dist_sqr :
                best_mvmt = choice
                dist_sqr = option_dist_sqr
        self.update_data(ship_info, best_mvmt)
        return best_mvmt

    def pick_opponent(self, ship, current_battle) :
        alt_id = (self.plr_num % 2) + 1
        opp_ships = [ship_info for ship_info in current_battle if ship_info['player_num'] == alt_id]
        self_ships = [ship_info for ship_info in current_battle if ship_info['player_num'] == self.plr_num]
        return opp_ships[0]
