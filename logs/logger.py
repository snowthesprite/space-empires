class Logger:
    def __init__(self, filename='log.txt'):
        self.filename = filename

    def clear_log(self):
        with open(self.filename, 'w') as file:
            file.writelines([''])

    def write(self, string=None):
        with open(self.filename, 'a') as file:
            file.writelines([string])

class GameLogger (Logger) :
    def __init__(self, filename='log.txt'):
        self.filename = filename
    
    def log_movement(self, player_id, scout_id, start, stop) :
        self.write('\n \t')
        line = 'Player {}, Scout {}: {} --> {}'.format(player_id,scout_id,start,stop)
        self.write(line)

    def begin_phase (self, turn, phase) :
        if phase == 'M' :
            phase_name = 'MOVEMENT'
        elif phase == 'C' :
            phase_name = 'COMBAT'
        elif phase == 'E' :
            phase_name = 'ECONOMIC'

        line = 'BEGIN TURN {} {} PHASE'.format(turn, phase_name)
        self.write(line)
        self.write('\n')

    def end_phase (self, turn, phase) :
        self.write('\n \n')
        if phase == 'M' :
            phase_name = 'MOVEMENT'
        elif phase == 'C' :
            phase_name = 'COMBAT'
        elif phase == 'E' :
            phase_name = 'ECONOMIC'

        line = 'END TURN {} {} PHASE'.format(turn, phase_name)
        self.write(line)
        self.write('\n \n')

    def log_combat(self, player_id, scout_id) :
        self.write('\n \t \t')
        line = 'Player {}, Scout {} has been destroyed!'.format(player_id,scout_id)
        self.write(line)
    
    def begin_combat(self, coords) :
        self.write('\n \t')
        line = 'Begin Combat at {}'.format(coords)
        self.write(line)
        self.write('\n')

    def log_winner(self,winner):
        line = 'WINNER: PLAYER {}'.format(winner)
        self.write(line)

class GameLoggerMK2 (GameLogger) :
    def __init__(self, filename='log.txt'):
        self.filename = filename
    
    def log_combat(self, attacker, defender, hit) :
        self.write('\n \t \t')
        line = 'Attacker : Player {}, Scout {}'.format(attacker[0],attacker[1])
        self.write(line)

        self.write('\n \t \t')
        line = 'Defender : Player {}, Scout {}'.format(defender[0],defender[1])
        self.write(line)

        if hit :
            self.write('\n \t \tHit!')
            self.write('\n \t \t')
            line = 'Player {}, Scout {} was destroyed!'.format(defender[0],defender[1])
        else :
            self.write('\n \t \t(Miss)')
        self.write('\n')
            
    def log_survivors(self, survivors, winner) :
        self.write('\n \t End of encounter')
        self.write('\n \t Survivors:')
        for survivor in survivors :
            self.write('\n \t \t')
            line = 'Player {}, Scout {}'.format(winner, survivor)
            self.write(line) 
