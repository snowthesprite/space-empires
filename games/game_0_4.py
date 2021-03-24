import random as rand
import sys
sys.path.append('loggers')
from game_logger_2 import *

class Game:
    def __init__(self, players, board_size=[7,7]):
        self.log = GameLogger('/home/runner/space-empires/logs/game-4-log.txt')
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
        self.used_space = {(mid_x,7) : [(2,1),(2,2),(2,3)], (mid_x,1) : [(1,1),(1,2),(1,3)]}

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
        self.log.write('WINNER: PLAYER {}'.format(self.game_state['winner']))

    def check_winner(self) :
        all_players = self.game_state['players']
        for player_id in range(1, 3) :
            alt_id = (player_id % 2) + 1
            for scout_loc in all_players[player_id]['scout_coords'].values() :
                if scout_loc == all_players[alt_id]['home_colony_coords'] :
                    self.game_state['winner'] = player_id
                    break

    def complete_movement_phase(self) :
        self.log.begin_phase(self.game_state['turn'], 'MOVEMENT')
        self.log.write('\n')
        for player in self.players :
            player_data = self.game_state['players'][player.player_number]
            for scout_id in player_data['scout_coords'].keys() :
                coords = player_data['scout_coords'][scout_id]

                if coords in list(self.game_state['players'][(player.player_number % 2) + 1]['scout_coords'].values()) or coords == None :
                    continue

                translations = self.get_in_bounds_translations(coords)
                chosen_trans = player.choose_translation(self.game_state,   translations, scout_id)
                new_coords = (coords[0] + chosen_trans[0], coords[1] + chosen_trans[1])

                if new_coords not in list(self.used_space) :
                    self.used_space[new_coords] = [(player.player_number, scout_id)]
                else :
                    self.used_space[new_coords].append((player.player_number, scout_id))
                self.used_space[coords].remove((player.player_number, scout_id))

                player_data['scout_coords'][scout_id] = new_coords
                self.log.log_movement(player.player_number, scout_id, coords, new_coords)
        self.log.end_phase(self.game_state['turn'], 'MOVEMENT')
        for (key, scouts) in self.used_space.copy().items() :
            if scouts == [] :
                self.used_space.pop(key)
    
    def complete_combat_phase(self) :
        all_battles = self.combat_order()
        self.log.begin_phase(self.game_state['turn'], 'COMBAT')
        all_players = self.game_state['players']
        survivors = {}
        self.log.log_combat_locations({loc : self.used_space[loc] for loc in all_battles})
        for (fight_coords, players) in all_battles.items() :
            keep_running = True
            self.log.write('\n\tCombat at {}\n'.format(fight_coords))
            current_battle = all_battles[fight_coords]
            fighters = self.used_space[fight_coords]
            while keep_running :
                for (p_id, scout_id) in fighters.copy() :
                    alt_id = (p_id % 2) + 1
                    if current_battle[alt_id] == [] :
                        keep_running = False
                        survivors[fight_coords] = fighters
                        break
                    if scout_id not in current_battle[p_id] :
                        continue
                    hit = round(rand.random())
                    alt_scout = current_battle[alt_id][0]
                    self.log.log_combat((p_id,scout_id),(alt_id, alt_scout), hit)
                    if hit == 1 : 
                        all_players[alt_id]['scout_coords'][alt_scout] = None
                        current_battle[alt_id].pop(0)
                        fighters.pop(fighters.index((alt_id,alt_scout)))
        
        self.log.log_survivors(survivors)
        ''''
                for (p_id, scout_id) in fighters :
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
                        self.log.log_combat((p_id,scout),(alt_id, alt_scout), hit)
                        if hit == 1 : 
                            all_players[alt_id]['scout_coords'][alt_scout] = None
                            players[alt_id].pop(0)
        '''
            
        self.log.end_phase(self.game_state['turn'], 'COMBAT')
    
    def combat_order(self) :
        combat_dict = {}
        for (loc, scouts) in self.used_space.items() :
            test = {plr_id for (plr_id,scout_id) in scouts}
            if len(test) == 1 :
                continue
            combat_dict[loc] = {1:[],2:[]}
            for (plr_id, scout_id) in scouts :
                combat_dict[loc][plr_id].append(scout_id)
        return combat_dict
        ''''
        all_players = self.game_state['players']
        p1_scouts = all_players[1]['scout_coords']
        p2_scouts = all_players[2]['scout_coords']
        combat_dict = {coord : {1:[],2:[]} for coord in p1_scouts.values() if coord in list(p2_scouts.values()) and coord != None}
        for (player_id,coords) in all_players.items() :
            for (scout_id,scout_loc) in coords['scout_coords'].items() :
                if scout_loc in list(combat_dict.keys()) :
                    combat_dict[scout_loc][player_id].append(scout_id)
        return combat_dict
        '''

        
    # you can add more helper methods if you want