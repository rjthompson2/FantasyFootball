import pandas as pd
import re

class Draft():
    def __init__(self, df:pd.DataFrame, total_teams:int):
        self.increment = 1
        self.current_round = 1
        self.current_team = 1
        self.total_teams = total_teams
        self.mock = df.copy()
        self.draft = {'PLAYER': [],'POS': [], 'TEAM': [], 'ORDER': [], 'VOR': []}

    def draft_player(self, player):
        '''Drafts a single player by adding them to self.draft'''
        if player in self.mock.values:
            self.draft['PLAYER'] += [player]
            self.draft['POS'].append(self.mock.loc[self.mock['PLAYER'] == player].iloc[0, 1])
            self.draft['TEAM'] += [self.current_team]
            self.draft['ORDER'] += [self.current_round]
            self.draft['VOR'].append(self.mock.loc[self.mock['PLAYER'] == player].iloc[0, 3].tolist())

            self.mock = self.mock.loc[self.mock['PLAYER'] != player]

            self.current_round+=1
            self.current_team = self.snake_increment(self.current_team)
        else:
            print(player + " is not a valid player!")

    def automated_draft(self, df, pos):
        '''Drafts players until none more left to add to self.draft'''
        while self.current_round < len(df):
            player = df.iloc[self.current_round - 1, 1]
            self.draft_player(player)

    def snake_increment(self, i):
        '''Increments to mimic a snaking draft'''
        i = i + self.increment
        if(i <= 0 and self.increment != 1):
            self.increment = 1
            i = 1
        elif(i > self.total_teams and self.increment != -1):
            self.increment = -1
            i = self.total_teams
        return i

    def suggestions(self):
        '''Suggests who to pick based on position and VOR'''
        positions = ['RB', 'WR', 'TE', 'QB', 'K', 'DST']
        for position in positions:
            if position == 'K' or position == 'DST':
                print('\n', self.mock.loc[self.mock['POS'] == position].head(1))
            else:
                print('\n', self.mock.loc[self.mock['POS'] == position].head(3))

    def scarcity(self):
        '''Shows the amount of valuable players are left in each positions and how scarce they are'''
        modifier = {
            "QB": 1,
            "TE": 1,
            "WR": 2,
            "RB": 2
        }
        new_mock = self.mock.loc[self.mock['VALUERANK'] <= self.total_teams * 15]

        print()
        for position in modifier:
            total_top = len(new_mock.loc[new_mock['POS'] == position])
            print(position, ': ', total_top, (total_top/(self.total_teams * modifier[position]))*10)

    def recommend(self):
        '''Recommends who to draft'''
        #TODO print all columns
        print("Team " + str(self.current_team) + "'s draft!")
        print(str(self.current_round) + " roster pick")
        self.scarcity()
        print("\nTop pick:")
        print(self.mock.head(1))
        self.suggestions()