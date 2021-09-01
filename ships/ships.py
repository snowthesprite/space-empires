class Scout() :
    def __init__(self, player_number, id) :
        self.hp = 1
        self.atk = 3
        self.df = 0
        self.pn = player_number
        self.id = 'SC' + str(id)
        self.type = 'E'


class BattleCruiser () :
    def __init__(self, player_number,id) :
        self.hp = 2
        self.df = 1
        self.atk = 5
        self.pn = player_number
        self.id = 'BC' + str(id)
        self.type = 'B'