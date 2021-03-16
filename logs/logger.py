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
