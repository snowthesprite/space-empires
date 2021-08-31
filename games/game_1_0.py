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
        self.used_space = {(mid_x,7) : [(2,'SC0'),(2,'SC1'),(2,'SC2')], (mid_x,1) : [(1,'SC0'),(1,'SC1'),(1,'SC2')]}

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
        self.complete_combat_phase()

        self.turn += 1

    def run_to_completion(self) :
        while self.winner == None :
            self.complete_turn()
            self.check_winner()
        self.log.write('WINNER: PLAYER {}'.format(self.winner))

    def check_winner(self) :
        for player_num in range(1, 3) :
            if self.plr_data[player_num]['Home Colony'] not in self.used_space.keys() :
                continue
            if self.opponent_there(self.plr_data[player_num]['Home Colony']) :
                self.winner = (player_num % 2) + 1
                break

    def find_ship_coords(self, plr_num, ship_id) :
        for (coord, ships) in self.used_space.items() :
            if (plr_num, ship_id) in ships :
                return coord
    
    def opponent_there(self, coord) :
        test = {plr_id for (plr_id,ship_id) in self.used_space[coord]}
        if len(test) == 1 :
            return False
        return True

    def complete_movement_phase(self) :
        self.log.begin_phase(self.turn, 'MOVEMENT')
        self.log.write('\n')
        for player in self.players :
            player_data = self.plr_data[player.player_number]
            for ship in player_data['ships'] :

                coords = self.find_ship_coords(player.player_number, ship.id)

                if self.opponent_there(coords) :
                    self.log.write('\n\tPlayer {} Ship {} is caught in battle at {}'.format(player.player_number, ship.id, coords))
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
    
    def if_hit(self, rolled, attacker, defender) :
        if rolled == 1 :
            return True
        
    
    def find_ship_from_id(self, player_id, ship_id) :
        index = 0
        for ship in self.plr_data[player_id]['ships'] :
            if ship.id == ship_id :
                return (index, ship)
            index += 1
        print('ERROR: NO SUCH SHIP WITH ID')
            

    def complete_combat_phase(self) :
        all_battles = self.combat_order()
        self.log.begin_phase(self.turn, 'COMBAT')
        survivors = {}
        self.log.log_combat_locations({loc : self.used_space[loc] for loc in all_battles})
        for (fight_coords, players) in all_battles.items() :
            keep_running = True
            self.log.write('\n\tCombat at {}\n'.format(fight_coords))
            current_battle = all_battles[fight_coords]
            fighters = all_battles[fight_coords]['combat order']
            while keep_running :
                for (plr_id, ship_id) in fighters.copy() :
                    alt_id = (plr_id % 2) + 1
                    if not self.opponent_there(fight_coords) :
                        keep_running = False
                        survivors[fight_coords] = fighters
                        break
                    if ship_id not in current_battle[plr_id] :
                        continue
                    attacker = self.find_ship_from_id(plr_id, ship_id)
                    defender = self.find_ship_from_id(alt_id, current_battle[alt_id][0])
                    hit = self.if_hit(rand.randint(1,10), attacker[1], defender[1])
                    self.log.log_combat((plr_id,ship_id),(alt_id, defender[1].id), hit)
                    if hit : 
                        self.plr_data[alt_id]['ships'].pop(defender[0])
                        self.used_space[fight_coords].pop(self.used_space[fight_coords].index((alt_id,defender[1].id)))
        
        self.log.log_survivors(survivors)
        self.log.end_phase(self.turn, 'COMBAT')
    
    def combat_order(self) :
        combat_dict = {}
        for (coord, ship_ref) in self.used_space.items() :
            if not self.opponent_there(coord) :
                continue
            combat_dict[coord] = {1:[],2:[]}
            ship_class = {'A': [], 'B': [], 'C':[], 'D': [], 'E': []}
            for (plr_id, ship_id) in ship_ref :
                combat_dict[coord][plr_id].append(ship_id)
                ship = self.find_ship_from_id(plr_id, ship_id)[1]
                ship_class[ship.type].append((plr_id, ship_id))
            combat_dict[coord]['combat order'] = ship_class['A'] + ship_class['B'] + ship_class['C'] + ship_class['D'] + ship_class['E']

        return combat_dict
       
        
    # you can add more helper methods if you want