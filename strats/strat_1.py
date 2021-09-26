## Calculates the shortest distance and moves along that path not caring about running into enemies. When attacking it will pick the enemy with the lowest health

class StraightToEnemyColony () :
    def __init__(self) :
        self.plr_data = None
        self.plr_num = None
        self.board = None

    def pick_translation(self, coord, choices) :
        myself = self.plr_data[self.plr_num]
        opponent_plr_num = (self.plr_num % 2) + 1
        opponent = plr_data[opponent_plr_num]

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

        return best_movement

    def pick_opponent(self, ship, current_battle) :
        pass