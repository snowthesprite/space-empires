## Heads to enemy colony, if going to run into a ship, waits three turns then engages

class WaitToAttack () :
    def __init__(self, wait) :
        self.plr_data = None
        self.plr_num = None
        self.board = None
        self.wait = 0
        self.wait_time = wait

    def pick_translation(self, coord, choices, ship_id = 1):
        myself = self.plr_data[self.plr_num]
        opponent_plr_num = (self.plr_num % 2) + 1
        opponent = self.plr_data[opponent_plr_num]

        my_ship_coords = coord
        opponent_home_colony_coords = opponent['Home Colony']

        dist_sqr = (my_ship_coords[0] - opponent_home_colony_coords[0]) ** 2 + (my_ship_coords[1] - opponent_home_colony_coords[1]) ** 2
        best_movement = None

        for choice in choices :
            option = (choice[0] + my_ship_coords[0], choice[1] + my_ship_coords[1])
            option_dist_sqr = (option[0] - opponent_home_colony_coords[0]) ** 2 + (option[1] - opponent_home_colony_coords[1]) ** 2
            if option_dist_sqr <= dist_sqr :
                best_movement = choice
                dist_sqr = option_dist_sqr
        new_coord = (my_ship_coords[0]+best_movement[0], my_ship_coords[1]+best_movement[1])
        if self.opponent_there(new_coord) and self.wait < self.wait_time * 3 :
            self.wait += 1
            return (0,0)
        return best_movement

    def pick_opponent(self, ship, current_battle) :
        alt_id = (self.plr_num % 2) + 1
        return self.find_ship_from_id(alt_id, current_battle[alt_id][0])

    def opponent_there(self, coord) :
        if coord not in self.board.keys() :
            return False
        test = {plr_data for (plr_data,ship_id) in self.board[coord]}
        if ((self.plr_num % 2) + 1) in test :
            return True
        return False
    
    def find_ship_from_id(self, plr_num, ship_id) :
        for ship in self.plr_data[plr_num]['ships'] :
            if ship.id == ship_id :
                return ship