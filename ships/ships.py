class Scout() :
    def __init__(self, player_number, id) :
        self.hp = 1
        self.dmg = 3
        self.df = 0
        self.pn = player_number
        self.id = 'S' + str(id)


class BattleCruiser () :
    def __init__(self, player_number,id) :
        self.hp = 2
        self.df = 1
        self.dmg = 5
        self.pn = player_number
        self.id = 'BC' + str(id)