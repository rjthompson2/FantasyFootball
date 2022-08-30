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
    flex = None
    weekly_ftps = 0

    def __init__(self, team_name: str) -> None:
        self.team_name = team_name

    def pick(self, add_player: Player, remove_player=None) -> None:
        if len(self.players) >= MAX_PLAYERS:
            raise RuntimeError("Unable to add player")
        self.players += add_player
        if remove_player != None:
            self.players -= remove_player

    def start(self, add_player: Player, remove_player=None) -> None:
        if remove_player == None:
            if self.pos_avail[add_player.pos] > 0:
                self.pos_avail[add_player.pos] -= 1
                self.lineup += add_player
            elif self.pos_avail["FLEX"] > 0 and add_player.pos in ["WR", "RB", "TE"]:
                self.pos_avail["FLEX"] -= 1
                self.lineup += add_player
                self.flex = add_player
            else:
                raise RuntimeError("Unable to add player")
        elif remove_player.pos == add_player.pos:
            self.lineup += add_player
            self.lineup -= remove_player
        elif self.flex == remove_player and add_player.pos in ["WR", "RB", "TE"]:
            self.flex = add_player
            self.lineup += add_player
            self.lineup -= remove_player

    def trade(self, Team, add_player: Player, remove_player: Player) -> None:
        if add_player in Team.players and remove_player in self.players:
            self.players += add_player
            self.players -= remove_player
        else:
            raise RuntimeError("Unable to trade player")

    def weekly_ftps(self) -> None:
        self.weekly_ftps = 0
        for player in self.lineup:
            self.weekly_ftps += player.ftps


class Player(ABC):
    self.ftps = 0

    def __init__(self, name: str, position: str, data) -> None:
        self.name = name
        self.pos = position
        self.data = data

    def update(self, ftps: float) -> None:
        self.ftps = ftps
