## Sends three scouts out dif areas, finds shortest mvmt to enemy colony while avoiding enemies. Battle cruisers stay w/in a 3 space radius seek and destroy. All move as one unit unless multiple, then 2 goes after one w/ most health, 1 after other, or 1 for each
## Compatable w/ strat_plr_1
class BattleStrat () :
    def __init__(self) :
        self.simple_board = {}

    def choose_translation(self, ship_info, choices) :
        if ship_info['name'] == 'Scout' :
            return self.scout_trans(ship_info, choices)
        elif ship_info['name'] == 'BattleCruiser' :
            return self.battlecruiser_trans(ship_info, choices)

    def choose_target(self, ship, current_battle) :
        plr_num = ship['player_num']

        alt_id = (plr_num % 2) + 1

        opp_ships = {'BattleCruiser': [], 'Scout': []}

        self_ships = []

        ship_init = current_battle.index(ship)

        for index in range(current_battle) :
            ship_info = current_battle[index]
            if ship_info['player_num'] == plr_num :
                if index > ship_init :
                    self_ships.append(ship_info)
                continue
            opp_ships[ship_info['name']].append(ship_info)
        
        priority = []
        priority.extend(opp_ships['Scout'])

        for bc in opp_ships['BattleCruiser'] :
            if bc['hp'] == 1 :
                priority.insert(0, bc)
            else :
                priority.append(bc)
        
        return priority[0]
        
    def find_home_col(self, plr_num) :
        for coord, stuff in self.simple_board.items() :
            for obj in stuff :
                if obj['player_num'] == plr_num and obj['obj_type'] == 'Colony' and obj['is_home_colony'] :
                    return coord
    
    def opp_there(self, plr_num, coord) :
        if coord not in self.simple_board.keys() :
            return False
        test = {ship_info['player_num'] for ship_info in self.simple_board[coord] if ship_info['obj_type'] == 'ship'}
        if ((plr_num % 2) + 1) in test :
            return True
        return False
    
    def to_col(self, ship_coords, colony_coords, choices = [(1,0),(0,1), (-1,0), (0,-1), (0,0)]) :
        dist_sqr = (ship_coords[0] - colony_coords[0]) ** 2 + (ship_coords[1] - colony_coords[1]) ** 2
        best_mvmt = [0,0]

        for choice in choices :
            option = (choice[0] + ship_coords[0], choice[1] + ship_coords[1])
            option_dist_sqr = (option[0] - colony_coords[0]) ** 2 + (option[1] - colony_coords[1]) ** 2
            if option_dist_sqr <= dist_sqr :
                best_mvmt = choice
                dist_sqr = option_dist_sqr
        return best_mvmt


    def scout_trans(self, ship_info, choices) :
        plr_num = ship_info['player_num']
        opp_plr_num = (plr_num % 2) + 1

        ship_coords = ship_info['coords']

        opp_home_col_coords = self.find_home_col(opp_plr_num)
        worst_choice = self.to_col(ship_coords, self.find_home_col(plr_num), choices)
        mvmt = self.to_col(ship_coords, opp_home_col_coords, choices)
        new_coord = (ship_coords[0]+mvmt[0], ship_coords[1]+mvmt[1])
        while self.opp_there(plr_num, new_coord) :
            choices.remove(mvmt)
            mvmt = self.to_col(ship_coords, opp_home_col_coords, choices)
            new_coord = (ship_coords[0]+mvmt[0], ship_coords[1]+mvmt[1])
        return mvmt

    def battlecruiser_trans(self, ship_info, choices) :
        plr_num = ship_info['player_num']
        opp_plr_num = (plr_num % 2) + 1

        ship_coords = ship_info['coords']

        opp_home_col_coords = self.find_home_col(opp_plr_num)

        mvmt = self.to_col(my_ship_coords, opp_home_col_coords, choices)

        best_coord = (ship_coords[0]+mvmt[0], ship_coords[1]+mvmt[1])

        if self.opp_there(plr_num, best_coord) :
            return [0,0]

        return self.to_col(my_ship_coords, opp_home_col_coords, choices)
        #enemy_loc = []
        #for x in range(4) :
            #for y in range(4) :

