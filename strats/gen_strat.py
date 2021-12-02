## Compatable w/ strat_plr 0.2
class GenStrat () :
    def __init__(self) :
        self.simple_board = {}

    def buy_ships(self, cp_amount) :
        ship_amounts = {'Scout': 5, 'BattleCruiser': 0, 'Cruiser': 0, 'Destroyer': 0, 'Dreadnaught': 0}
        return ship_amounts

    def choose_translation(self, ship_info, choices) :
        plr_num = ship_info['player_num']
        opp_plr_num = (plr_num % 2) + 1

        ship_coords = ship_info['coords']

        opp_home_col_coords = self.find_home_col(opp_plr_num)

        mvmt = self.to_col(ship_coords, opp_home_col_coords, choices)

        #print(self.opp_there(plr_num, best_coord))

        return mvmt

    def choose_target(self, ship, current_battle) :
        plr_num = ship['player_num']

        alt_id = (plr_num % 2) + 1

        opp_ships = [ship_info for ship_info in current_battle if ship_info['player_num'] == alt_id]

        self_ships = [ship_info for ship_info in current_battle if ship_info['player_num'] == plr_num]

        return opp_ships[0]

        
    def find_home_col(self, plr_num) :
        for coord, stuff in self.simple_board.items() :
            for obj in stuff :
                if obj['player_num'] == plr_num and obj['obj_type'] == 'Colony' and obj['is_home_colony'] :
                    return coord
    
    def opp_there(self, plr_num, coord) :
        if coord not in self.simple_board.keys() :
            return False
        test = {ship_info['player_num'] for ship_info in self.simple_board[coord] if ship_info['obj_type'] == 'Ship'}
        if ((plr_num % 2) + 1) in test :
            return True
        return False

    
    def to_col(self, ship_coords, colony_coords, choices = [(1,0),(0,1), (-1,0), (0,-1)]) :
        dist_sqr = (ship_coords[0] - colony_coords[0]) ** 2 + (ship_coords[1] - colony_coords[1]) ** 2
        best_mvmt = (0,0)

        for choice in choices :
            option = (choice[0] + ship_coords[0], choice[1] + ship_coords[1])
            option_dist_sqr = (option[0] - colony_coords[0]) ** 2 + (option[1] - colony_coords[1]) ** 2
            if option_dist_sqr <= dist_sqr :
                best_mvmt = choice
                dist_sqr = option_dist_sqr
        return best_mvmt