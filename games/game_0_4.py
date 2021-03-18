import random as rand
import sys
sys.path.append('logs')
from logger import *

class Game:
    def __init__(self, players, board_size=[7,7]):
        self.log = GameLoggerMK2('/home/runner/space-empires/logs/game-4-log.txt')
        self.log.clear_log()
        self.players = players
        self.set_player_numbers()
        rand.seed(1)

        board_x, board_y = board_size
        mid_x = (board_x + 1) // 2
        mid_y = (board_y + 1) // 2

        self.game_state = {
            'turn': 1,
            'board_size': board_size,
            'players': {
                1: {
                    'scout_coords': {
                        1: (mid_x, 1),
                        2: (mid_x, 1),
                        3: (mid_x, 1)
                    },
                    'home_colony_coords': (mid_x, 1)
                },
                2: {
                    'scout_coords': {
                        1: (mid_x, 7),
                        2: (mid_x, 7),
                        3: (mid_x, 7)
                    },
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
        self.log.log_winner(self.game_state['winner'])

    def check_winner(self) :
        all_players = self.game_state['players']
        for player_id in range(1, 3) :
            alt_id = (player_id % 2) + 1
            for scout_loc in all_players[player_id]['scout_coords'].values() :
                if scout_loc == all_players[alt_id]['home_colony_coords'] :
                    self.game_state['winner'] = player_id

    def complete_movement_phase(self) :
        self.log.begin_phase(self.game_state['turn'], 'M')
        for player in self.players :
            player_data = self.game_state['players'][player.player_number]
            for scout_id in player_data['scout_coords'].keys() :
                coords = player_data['scout_coords'][scout_id]

                if coords in list(self.game_state['players'][(player.player_number % 2) + 1]['scout_coords'].values()) or coords == None :
                    continue

                translations = self.get_in_bounds_translations(coords)
                chosen_trans = player.choose_translation(self.game_state,   translations, scout_id)
                new_coords = (coords[0] + chosen_trans[0], coords[1] + chosen_trans[1])
                player_data['scout_coords'][scout_id] = new_coords
                self.log.log_movement(player.player_number, scout_id, coords, new_coords)
        self.log.end_phase(self.game_state['turn'], 'M')
    
    def complete_combat_phase(self) :
        all_battles = self.combat_order()
        self.log.begin_phase(self.game_state['turn'], 'C')
        all_players = self.game_state['players']
        
        for (fight_coords, players) in all_battles.items() :
            self.log.begin_combat(fight_coords)
            keep_running = True
            while keep_running :
                for (p_id, scouts) in players.items() :
                    alt_id = (p_id % 2) + 1
                    if scouts == [] :
                        keep_running = False
                        self.log.log_survivors(players[alt_id], alt_id)
                        break
                    for scout in scouts :
                        if players[alt_id] == [] :
                            break
                        hit = round(rand.random())
                        alt_scout = players[alt_id][0]
                        if hit == 1 : 
                            self.log.log_combat((p_id,scout),(alt_id, alt_scout), True)
                            all_players[alt_id]['scout_coords'][alt_scout] = None
                            players[alt_id].pop(0)
                        else :
                            self.log.log_combat((p_id,scout),(alt_id, alt_scout), False)
        self.log.end_phase(self.game_state['turn'], 'C')
    
    def combat_order(self) :
        all_players = self.game_state['players']
        p1_scouts = all_players[1]['scout_coords']
        p2_scouts = all_players[2]['scout_coords']
        combat_dict = {coord : {1:[],2:[]} for coord in p1_scouts.values() if coord in list(p2_scouts.values()) and coord != None}
        for (player_id,coords) in all_players.items() :
            for (scout_id,scout_loc) in coords['scout_coords'].items() :
                if scout_loc in list(combat_dict.keys()) :
                    combat_dict[scout_loc][player_id].append(scout_id)
        return combat_dict

        
    # you can add more helper methods if you want