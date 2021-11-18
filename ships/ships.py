class Ship () :
    def class_to_dict(self, coords = None) :
        att = self.__dict__
        ship_dict = {'hp': att['hp'], 
                'atk': att['atk'],
                'df': att['df'],
                'player_num': att['pn'],
                'coords': coords,
                'ship_num': att['other'][1],
                'name': att['other'][0],
                'ship_class': att['type'],
                'obj_type': att['other'][2],
                'ship_id': att['id']}
        return ship_dict

class Battleship (Ship) :
    def __init__(self, player_number, id) :
        self.hp = 3
        self.atk = 5
        self.df = 2
        self.pn = player_number
        self.id = 'BB' + str(id)
        self.type = 'A'
        #self.list_id = None
        self.other = ['Battleship', id, 'Ship']

class BattleCruiser (Ship) :
    def __init__(self, player_number,id) :
        self.hp = 2
        self.df = 1
        self.atk = 5
        self.pn = player_number
        self.id = 'BC' + str(id)
        self.type = 'B'
        #self.list_id = None
        self.other = ['BattleCruiser', id, 'Ship']

class Cruiser (Ship) :
    def __init__(self, player_number, id) :
        self.hp = 2
        self.atk = 4
        self.df = 1
        self.pn = player_number
        self.id = 'CA' + str(id)
        self.type = 'C'
        #self.list_id = None
        self.other = ['Cruiser', id, 'Ship']

class Destroyer (Ship) :
    def __init__(self, player_number, id) :
        self.hp = 1
        self.atk = 4
        self.df = 0
        self.pn = player_number
        self.id = 'DD' + str(id)
        self.type = 'D'
        #self.list_id = None
        self.other = ['Destroyer', id, 'Ship']

class Dreadnaught (Ship) :
    def __init__(self, player_number, id) :
        self.hp = 3
        self.atk = 6
        self.df = 3
        self.pn = player_number
        self.id = 'DN' + str(id)
        self.type = 'A'
        #self.list_id = None
        self.other = ['Dreadnaught', id, 'Ship']

class Scout (Ship) :
    def __init__(self, player_number, id) :
        self.hp = 1
        self.atk = 3
        self.df = 0
        self.pn = player_number
        self.id = 'SC' + str(id)
        self.type = 'E'
        #self.list_id = None
        self.other = ['Scout', id, 'Ship']

class ShipYard (Ship) :
    def __init__(self, player_number, id) :
        self.hp = 1
        self.atk = 3
        self.df = 0
        self.pn = player_number
        self.id = 'SY' + str(id)
        self.type = 'C'
        #self.list_id = None
        self.other = ['ShipYard', id, 'Yard']


