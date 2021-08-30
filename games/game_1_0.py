import random as rand
import sys
sys.path.append('loggers')
from game_logger_3 import *
sys.path.append('ships')
from ships import *

class Game:
    def __init__(self, players, board_size=[7,7]):
        self.log = GameLogger('/home/runner/space-empires/logs/game-1_0-log.txt')
        self.log.clear_log()
        self.winner = None
        self.players = players
        self.turn = 1
        self.board_size = board_size
        self.set_player_numbers()
        rand.seed(1)

        board_x, board_y = board_size
        mid_x = (board_x + 1) // 2
        
        mid_y = (board_y + 1) // 2

        self.plr_data = {
            1:{
                'Home Colony' : (mid_x,1), #Alive
                'ships': [Scout(1,0), Scout(1,1), Scout(1,2)],
                'Total Scouts': 3,
                'Battlecruiser': 0,
            },
            2: {
                'Home Colony' : (mid_x,7), #Alive
                'ships': [Scout(2,0), Scout(2,1), Scout(2,2)],
                'Total Scouts': 3,
                'Battlecruiser': 0,
            }
        }

        ''''
        self.board = [[[] for columns in range(board_y)] for rows in range(board_x)]
        self.board[mid_x][0].push([(1,'Home Colony'), (1,'S0'), (1,'S1'), (1,'S3')])
        self.board[mid_x][mid_y].push([(2, 'Home Colony'), (2,'S0'), (2,'S1'), (2,'S3')])
        '''
        self.used_space = {(mid_x,7) : [(2,'S0'),(2,'S1'),(2,'S2')], (mid_x,1) : [(1,'S0'),(1,'S1'),(1,'S2')]}

    def set_player_numbers(self):
        for i, player in enumerate(self.players):
            player.set_player_number(i+1)

    def check_if_coords_are_in_bounds(self, coords):
        x, y = coords
        board_x, board_y = self.board_size
        if 1 <= x and x <= board_x:
            if 1 <= y and y <= board_y:
                return True
        return False

    def check_if_translation_is_in_bounds(self, coords, translation):
        max_x, max_y = self.board_size
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
        #self.complete_combat_phase()

        self.turn += 1

    def run_to_completion(self) :
        while self.winner == None :
            self.complete_turn()
            self.check_winner()
        self.log.write('WINNER: PLAYER {}'.format(self.winner))

    def check_winner(self) :
        for player_id in range(1, 3) :
            if self.plr_data[player_id]['Home Colony'] not in self.used_space.keys() :
                continue
            alt_id = (player_id % 2) + 1
            for (player, ship_id) in self.used_space[self.plr_data[player_id]['Home Colony']] :
                if player == alt_id :
                    self.winner = alt_id
                    break

    def find_ship_coords(self, plr_num, ship_id) :
        for (coord, ships) in self.used_space.items() :
            if (plr_num, ship_id) in ships :
                return coord
    
    def opponent_there(self, coord) :
        pass

    def complete_movement_phase(self) :
        self.log.begin_phase(self.turn, 'MOVEMENT')
        self.log.write('\n')
        for player in self.players :
            player_data = self.plr_data[player.player_number]
            for ship in player_data['ships'] :

                coords = self.find_ship_coords(player.player_number, ship.id)

                if self.opponent_there(coords) :
                    continue

                translations = self.get_in_bounds_translations(coords)
                chosen_trans = player.choose_translation(self.plr_data, translations)
                new_coords = (coords[0] + chosen_trans[0], coords[1] + chosen_trans[1])

                if new_coords not in list(self.used_space) :
                    self.used_space[new_coords] = [(player.player_number, ship.id)]
                else :
                    self.used_space[new_coords].append((player.player_number, ship.id))
                self.used_space[coords].remove((player.player_number, ship.id))

                self.log.log_movement(player.player_number, ship.id, coords, new_coords)
        self.log.end_phase(self.turn, 'MOVEMENT')
        for (key, ships) in self.used_space.copy().items() :
            if ships == [] :
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
                for (p_id, ship.id) in fighters.copy() :
                    alt_id = (p_id % 2) + 1
                    if current_battle[alt_id] == [] :
                        keep_running = False
                        survivors[fight_coords] = fighters
                        break
                    if ship.id not in current_battle[p_id] :
                        continue
                    hit = round(rand.random())
                    alt_scout = current_battle[alt_id][0]
                    self.log.log_combat((p_id,ship.id),(alt_id, alt_scout), hit)
                    if hit == 1 : 
                        all_players[alt_id]['scout_coords'][alt_scout] = None
                        current_battle[alt_id].pop(0)
                        fighters.pop(fighters.index((alt_id,alt_scout)))
        
        self.log.log_survivors(survivors)
        self.log.end_phase(self.game_state['turn'], 'COMBAT')
    
    def combat_order(self) :
        combat_dict = {}
        for (loc, scouts) in self.used_space.items() :
            test = {plr_id for (plr_id,ship.id) in scouts}
            if len(test) == 1 :
                continue
            combat_dict[loc] = {1:[],2:[]}
            for (plr_id, ship.id) in scouts :
                combat_dict[loc][plr_id].append(ship.id)
        return combat_dict
       
        
    # you can add more helper methods if you want