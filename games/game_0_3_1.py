import random as rand

class Game:
    def __init__(self, players, board_size=[7,7]):
        self.players = players
        self.set_player_numbers()

        board_x, board_y = board_size
        mid_x = (board_x + 1) // 2
        mid_y = (board_y + 1) // 2

        self.game_state = {
            'turn': 1,
            'board_size': board_size,
            'players': {
                1: {
                    'scout_coords': [(mid_x, 1), (mid_x, 1), (mid_x, 1)],
                    'home_colony_coords': (mid_x, 1)
                },
                2: {
                    'scout_coords': [(mid_x, 1), (mid_x, 1), (mid_x, 1)],
                    'home_colony_coords': (mid_x, board_y)
                }
            },
            'winner': None 
        }

    def set_player_numbers(self):
        for i, player in enumerate(self.players):
            player.set_player_number(i+1)

    def check_if_coords_are_in_bounds(self, coords):
        x, y = coords
        board_x, board_y = self.game_state['board_size']
        if 1 <= x and x <= board_x:
            if 1 <= y and y <= board_y:
                return True
        return False

    def check_if_translation_is_in_bounds(self, coords, translation):
        max_x, max_y = self.game_state['board_size']
        x, y = coords
        dx, dy = translation
        new_coords = (x+dx,y+dy)
        return self.check_if_coords_are_in_bounds(new_coords)

    def get_in_bounds_translations(self, coords):
        translations = [(0,0), (0,1), (0,-1), (1,0), (-1,0)]
        in_bounds_translations = []
        for translation in translations:
            if self.check_if_translation_is_in_bounds(coords, translation):
                in_bounds_translations.append(translation)
        return in_bounds_translations

    def complete_turn(self):
        self.complete_movement_phase()
        self.complete_combat_phase()

        self.game_state['turn'] += 1

    def run_to_completion(self) :
        while self.game_state['winner'] == None :
            self.complete_turn()
            self.check_winner()

    def check_winner(self) :
        all_players = self.game_state['players']
        for player_id in range(1, 3) :
            alt_id = (player_id % 2) + 1
            if all_players[player_id]['scout_coords'] == [] :
                self.game_state['winner'] = alt_id

    def complete_movement_phase(self) :
        for player in self.players :
            player_data = self.game_state['players'][player.player_number]
            for scout_id in range(len(player_data['scout_coords'])) :
                coords = player_data['scout_coords'][scout_id]

                if coords in self.game_state['players'][(player.player_number % 2) + 1]['scout_coords'] :
                    continue

                translations = self.get_in_bounds_translations(coords)
                chosen_trans = player.choose_translation(self.game_state,   translations, scout_id)
                player_data['scout_coords'][scout_id] = (coords[0] + chosen_trans[0], coords[1] + chosen_trans[1])
    
    def complete_combat_phase(self) :
        all_players = self.game_state['players']
        p1_scouts = all_players[1]['scout_coords']
        p2_scouts = all_players[2]['scout_coords']
        for p1_scout in p1_scouts :
            if p1_scout in p2_scouts :
                scout_indices = [p1_scouts.index(p1_scout), p2_scouts.index(p1_scout)]
                judge = rand.randint(1,2)
                all_players[judge]['scout_coords'].pop(scout_indices[judge-1])
    # you can add more helper methods if you want
