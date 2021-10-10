from logger import *

class GameLogger (Logger) :
    def __init__(self, filename='log.txt', loc='/home/runner/space-empires/logs/') :
        self.filename = loc + filename
    
    def log_movement(self, player_id, ship_id, start, stop) :
        self.write('\n\t')
        self.write('Player {} Ship {}: {} -> {}'.format(player_id,ship_id,start,stop))
        #I personally like "Player {}, Ship {}: {} -->  but go off

    def begin_phase (self, turn, phase) :
        #Personally like 'BEGIN TURN {} {} PHASE' 
        self.write('BEGINNING OF TURN {} {} PHASE'.format(turn, phase))

    def end_phase (self, turn, phase) :
        self.write('\n\n')
        #still like this... 'END TURN {} {} PHASE'
        self.write('END OF TURN {} {} PHASE'.format(turn, phase))
        self.write('\n\n')
    
    def log_combat_locations(self, battles) :
        if battles != {} :
            self.write('\n\n\tCombat Locations:')
        for (coords, fighters) in battles.items() :
            self.write('\n\n\t\t')
            self.write(str(coords))
            self.write('\n')
            for (p_id,ship_id) in fighters :
                self.write('\n\t\t\t')
                self.write('Player {} Ship {}'.format(p_id,ship_id))
        if battles != {} :
            self.write('\n')
    
    def log_combat(self, attacker, defender, hit) :
        self.write('\n\t\t')
        self.write('Attacker: Player {} Ship {}'.format(attacker[0],attacker[1]))

        self.write('\n\t\t')
        self.write('Defender: Player {} Ship {}'.format(defender[0],defender[1]))

        if hit:
            self.write('\n\t\tHit!')
        else :
            self.write('\n\t\t(Miss)')
        self.write('\n')
    
    def log_damage(self, ship) :
        self.write('\n\t\t')
        self.write('Player {} Ship {} HP reduced to {}!'.format(ship.pn, ship.id, ship.hp))
        self.write('\n')
        if ship.hp == 0 :
            self.write('\t\t')
            self.write('Player {} Ship {} was destroyed!'.format(ship.pn, ship.id))
            self.write('\n')
            
    def log_survivors(self, battle_survivors) :
        if battle_survivors != {} :
            self.write('\n\tSurvivors:')
        for (battle, survivors) in battle_survivors.items() :
            self.write('\n\n\t\t')
            self.write(str(battle))
            self.write('\n')
            for (p_id, ship_id) in survivors :
                self.write('\n\t\t\t')
                self.write('Player {} Ship {}'.format(p_id, ship_id))