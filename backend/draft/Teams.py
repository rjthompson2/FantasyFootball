from dataclasses import dataclass, field


@dataclass
# TODO WIP
class Teams:
    teams: list

    def update_VOR(self, df):
        """Updates each players VOR"""
        pass

    def get_breakdown(self):
        team_positions = {}
        for i in range(len(self.teams)):
            team_positions[i + 1] = self.teams[i].break_down()

        for team in team_positions:
            print(str(team) + str(team_positions[team]))
            print()

    def compare(self):
        """Compares all teams and say who is the best team based on VOR"""
        pass

    def trade(self, player1, player2):
        """Switches players between teams"""
        team1, index1 = self.find_team_player(player1)
        team2, index2 = self.find_team_player(player2)

        temp = self.teams[team1].players[index1]
        self.teams[team1].players[index1] = self.teams[team2].players[index2]
        self.teams[team2].players[index2] = temp

    def find_team_player(self, player):
        """Switches players between teams"""
        index = [
            [i, j]
            for i in range(len(self.teams))
            for j in range(len(self.teams[i].players))
            if self.teams[i].players[j].player == player
        ]
        return index[0][0], index[0][1]

    def recommend_trades(self, team_name):
        """Gives a recommended list of who you could trade"""
        pass

    def best_trade(self, player):
        """Gives a recommended best trade based on a given player you need to trade"""
        self.in_position()
        self.all_positions()
        pass

    def pickup(self, pkayer1, player2):
        """Adds a player to your team and drops the other"""
        pass

    def convert_to_CSV(self):
        """Saves all teams to a CSV file"""
        pass

    def print_team(self, i):
        print(self.teams[i - 1])


@dataclass
class Player:
    player: str
    position: str
    order: str
    vor: str
    sort_index: float = field(init=False, repr=False)

    def __post_init__(self):
        self.sort_index = float(self.vor)


@dataclass
class Team:
    team: int
    players: list

    def break_down(self):
        positions_total = {
            "QB": 0,
            "RB": 0,
            "WR": 0,
            "TE": 0,
            "K": 0,
            "DST": 0,
        }
        for i in range(len(self.players)):
            positions_total[self.players[i].position] += 1
        return positions_total
