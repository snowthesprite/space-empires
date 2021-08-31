class CustomPlayer():
    def __init__(self):
        self.player_number = None

    def set_player_number(self, n):
        self.player_number = n

    def get_opponent_player_number(self):
        if self.player_number == None:
            return None
        else :
            return (self.player_number % 2) + 1

    def choose_translation(self, player_data, choices, ship_id = 1):
        myself = player_data[self.player_number]
        opponent_player_number = self.get_opponent_player_number()
        opponent = player_data[opponent_player_number]

        my_ship_coords = myself['ships'][ship_id]
        opponent_home_colony_coords = opponent['home_colony_coords']

        dist_sqr = (my_ship_coords[0] - opponent_home_colony_coords[0]) ** 2 + (my_ship_coords[1] - opponent_home_colony_coords[1]) ** 2
        best_movement = None

        for choice in choices :
            option = (choice[0] + my_ship_coords[0], choice[1] + my_ship_coords[1])
            option_dist_sqr = (option[0] - opponent_home_colony_coords[0]) ** 2 + (option[1] - opponent_home_colony_coords[1]) ** 2
            if option_dist_sqr <= dist_sqr :
                best_movement = choice
                dist_sqr = option_dist_sqr

        return best_movement