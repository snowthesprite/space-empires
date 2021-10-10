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
                'obj_type': att['other'][2]}
        return ship_dict

class Scout (Ship) :
    def __init__(self, player_number, id) :
        self.hp = 1
        self.atk = 3
        self.df = 0
        self.pn = player_number
        self.id = 'SC' + str(id)
        self.type = 'E'
        self.list_id = None
        self.other = ['SC', id, 'Ship']


    
class BattleCruiser (Ship) :
    def __init__(self, player_number,id) :
        self.hp = 2
        self.df = 1
        self.atk = 5
        self.pn = player_number
        self.id = 'BC' + str(id)
        self.type = 'B'
        self.list_id = None
        self.other = ['BC', id, 'Ship']
