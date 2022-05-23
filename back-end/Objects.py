from abc import ABC

class FFPlayer(ABC):
    players = []
    lineup = []
    pos_avail = {
        "QB": 1,
        "WR": 2,
        "RB": 2,
        "TE": 1,
        "FLEX": 1,
        "K": 1,
        "DEF": 1,
    }

    def __init__(self, team_name):
        self.team_name = team_name

    def pick(self, add_player, remove_player=None):
        if players >= MAX_PLAYERS:
            raise RuntimeError("Unable to add player")
        players += add_player
        if remove_player != None:
            players -= remove_player


    def start(self, add_player, remove_player=None):
        if remove_player == None:
            if self.pos_avail[add_player.pos] > 0:
                self.pos_avail[add_player.pos] -= 1
                lineup += add_player
            elif self.pos_avail["FLEX"] > 0 and add_player.pos in ["WR", "RB", "TE"]:
                self.pos_avail["FLEX"] -= 1
                lineup += add_player
            else:
                raise RuntimeError("Unable to add player")
        elif remove_player.pos == add_player.pos:
            lineup += add_player
            lineup -= remove_player

    def trade(self, Team, add_player, remove_player):
        if add_player in Team.players:
            players += add_player
            players -= remove_player
        else:
            raise RuntimeError("Unable to trade player")
        

class Player(ABC):
    self.ftps = 0
    def __init__(self, name, position, data):
        self.name = name
        self.pos = position
        self.data = data

    def update(self, ftps):
        self.ftps = ftps
