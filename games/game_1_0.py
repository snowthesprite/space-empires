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
        #rand.seed(1)

        board_x, board_y = board_size
        mid_x = (board_x + 1) // 2
        
        mid_y = (board_y + 1) // 2

        self.plr_data = {
            1:{
                'Home Colony' : (mid_x,1), #Alive
                'ships': [Scout(1,0), Scout(1,1), BattleCruiser(1,0)],
                'Total Scouts': 2,
                'Battlecruiser': 1,
            },
            2: {
                'Home Colony' : (mid_x,7), #Alive
                'ships': [Scout(2,0), Scout(2,1), BattleCruiser(2,0)],
                'Total Scouts': 2,
                'Battlecruiser': 1,
            }
        }

        self.used_coords = {(mid_x,7) : [(2,ship.id) for ship in self.plr_data[2]['ships']], (mid_x,1) : [(1,ship.id) for ship in self.plr_data[1]['ships']]}

    def set_player_numbers(self):
        for i, player in enumerate(self.players):
            player.set_plr_num(i+1)

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
            if self.plr_data[player_num]['Home Colony'] not in self.used_coords.keys() :
                continue
            if self.opponent_there(self.plr_data[player_num]['Home Colony'], player_num) :
                self.winner = (player_num % 2) + 1
                break

    def find_ship_coords(self, plr_num, ship_id) :
        for (coord, ships) in self.used_coords.items() :
            if (plr_num, ship_id) in ships :
                return coord
    
    def opponent_there(self, coord, player_num) :
        test = {plr_id for (plr_id,ship_id) in self.used_coords[coord]}
        if ((player_num % 2) + 1) in test :
            return True
        return False

    def complete_movement_phase(self) :
        self.log.begin_phase(self.turn, 'MOVEMENT')
        self.log.write('\n')
        for player in self.players :
            player_data = self.plr_data[player.plr_num]
            for ship in player_data['ships'] :
                player.set_data(self.plr_data, self.used_coords)

                coords = self.find_ship_coords(player.plr_num, ship.id)

                if self.opponent_there(coords, player.plr_num) :
                    self.log.write('\n\tPlayer {} Ship {} is caught in battle at {}'.format(player.plr_num, ship.id, coords))
                    continue

                translations = self.get_in_bounds_translations(coords)
                chosen_trans = player.pick_translation(coords, translations)
                new_coords = (coords[0] + chosen_trans[0], coords[1] + chosen_trans[1])

                if new_coords not in list(self.used_coords) :
                    self.used_coords[new_coords] = [(player.plr_num, ship.id)]
                else :
                    self.used_coords[new_coords].append((player.plr_num, ship.id))
                self.used_coords[coords].remove((player.plr_num, ship.id))

                self.log.log_movement(player.plr_num, ship.id, coords, new_coords)
        self.log.end_phase(self.turn, 'MOVEMENT')
        for (key, ships) in self.used_coords.copy().items() :
            if ships == [] :
                self.used_coords.pop(key)
        self.players[0].set_data(self.plr_data, self.used_coords)
        self.players[1].set_data(self.plr_data, self.used_coords)
    
    def if_hit(self, rolled, attacker, defender) :
        max_hit = attacker.atk - defender.df
        self.log.write('\n\t\tRolled a {}, less than or equal to {}'.format(rolled,max_hit))
        if rolled <= max_hit or rolled == 1 :
            return True
        return False
        
    
    def find_ship_from_id(self, player_id, ship_id) :
        index = 0
        for ship in self.plr_data[player_id]['ships'] :
            if ship.id == ship_id :
                ship.list_id = index
                return ship
            index += 1
        #print('ERROR: NO SUCH SHIP WITH ID')
            

    def complete_combat_phase(self) :
        all_battles = self.combat_order()
        self.log.begin_phase(self.turn, 'COMBAT')
        survivors = {}
        self.log.log_combat_locations({loc : self.used_coords[loc] for loc in all_battles})
        for (fight_coords, players) in all_battles.items() :
            keep_running = True
            self.log.write('\n\tCombat at {}\n'.format(fight_coords))
            current_battle = all_battles[fight_coords]
            battlefield = self.used_coords[fight_coords]
            while keep_running :
                for (plr_id, ship_id) in current_battle['combat order'] :
                    alt_id = (plr_id % 2) + 1
                    if not self.opponent_there(fight_coords, plr_id) :
                        keep_running = False
                        survivors[fight_coords] = battlefield
                        break
                    attacker = self.find_ship_from_id(plr_id, ship_id)
                    if attacker == None :
                        continue
                    defender = self.players[plr_id - 1].pick_opponent( attacker, current_battle)
                    #print(attacker, defender)
                    hit = self.if_hit(rand.randint(1,10), attacker, defender)
                    self.log.log_combat((plr_id,ship_id),(alt_id, defender.id), hit)
                    if hit : 
                        defender.hp -= 1
                        self.log.write('\n\t\tPlayer {} Ship {} HP reduced to {}!\n'.format(alt_id, defender.id, defender.hp))
                    if defender.hp == 0 :
                        self.plr_data[alt_id]['ships'].pop(defender.list_id)
                        battlefield.pop(battlefield.index((alt_id,defender.id)))
                        current_battle[alt_id].remove(defender.id)
                        self.log.write('\t\tPlayer {} Ship {} was destroyed!\n'.format(alt_id, defender.id))
                    self.players 
        
        self.log.log_survivors(survivors)
        self.log.end_phase(self.turn, 'COMBAT')
    
    def combat_order(self) :
        combat_dict = {}
        for (coord, ship_list) in self.used_coords.items() :
            test = {plr_id for (plr_id,ship_id) in ship_list}
            if len(test) == 1 :
                continue
            combat_dict[coord] = {1:[],2:[]}
            ship_class = {'A': [], 'B': [], 'C':[], 'D': [], 'E': []}
            for (plr_id, ship_id) in ship_list :
                combat_dict[coord][plr_id].append(ship_id)
                ship = self.find_ship_from_id(plr_id, ship_id)
                ship_class[ship.type].append((plr_id, ship_id))
            combat_dict[coord]['combat order'] = ship_class['A'] + ship_class['B'] + ship_class['C'] + ship_class['D'] + ship_class['E']

        return combat_dict
       
        
    # you can add more helper methods if you want