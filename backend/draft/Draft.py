from backend.data_collection.utils import (
    clean_name_str,
    change_player_name,
    change_team_name_str,
)
import pandas as pd
import re


class Draft:
    def __init__(self, df: pd.DataFrame, total_teams: int) -> None:
        self.increment = 1
        self.current_round = 1
        self.current_team = 1
        self.total_teams = total_teams
        self.mock = df.copy()
        self.draft = {"PLAYER": [], "POS": [], "TEAM": [], "ORDER": [], "VOR": []}

    def draft_player(self, player: str) -> None:
        """Drafts a single player by adding them to self.draft

        Args:
            player (str): The name of the player that's being added
        """
        player = clean_name_str(player)
        player = change_player_name(player)
        player = change_team_name_str(player)
        if player in self.mock.values:
            print(player)
            self.draft["PLAYER"] += [player]
            self.draft["POS"].append(
                self.mock.loc[self.mock["PLAYER"] == player].iloc[0, 1]
            )
            self.draft["TEAM"] += [self.current_team]
            self.draft["ORDER"] += [self.current_round]
            self.draft["VOR"].append(
                self.mock.loc[self.mock["PLAYER"] == player].iloc[0, 3].tolist()
            )

            self.mock = self.mock.loc[self.mock["PLAYER"] != player]

            self.current_round += 1
            self.current_team = self.snake_increment(self.current_team)
        else:
            print(player + " is not a valid player!")
            self.draft["PLAYER"] += [player]
            self.draft["POS"] += ["?"]
            self.draft["TEAM"] += ["?"]
            self.draft["ORDER"] += ["?"]
            self.draft["VOR"] += ["?"]

            self.current_round += 1
            self.current_team = self.snake_increment(self.current_team)

    def automated_draft(self, df: pd.DataFrame, pos: str) -> None:
        """Drafts players until none more left to add to self.draft

        Args:
            df (DataFrame): The dataframe used to get the player
            pos (str): Unused??
        """
        while self.current_round < len(df):
            player = df.iloc[self.current_round - 1, 1]
            self.draft_player(player)

    def snake_increment(self, i: int) -> int:
        """Increments to mimic a snaking draft

        Args:
            i (int): The current position of the draft

        Returns:
            int: Previous position incremented by 1. Uses a snaking system to increment
        """
        i = i + self.increment
        if i <= 0 and self.increment != 1:
            self.increment = 1
            i = 1
        elif i > self.total_teams and self.increment != -1:
            self.increment = -1
            i = self.total_teams
        return i

    def suggestions(self) -> None:
        """Suggests who to pick based on position and VOR"""
        positions = ["RB", "WR", "TE", "QB", "K", "DST"]
        for position in positions:
            if position == "K" or position == "DST":
                print("\n", self.mock.loc[self.mock["POS"] == position].head(1))
            else:
                print("\n", self.mock.loc[self.mock["POS"] == position].head(3))

    def scarcity(self) -> None:
        """Shows the amount of valuable players are left in each positions and how scarce they are"""
        modifier = {"QB": 1, "TE": 1, "WR": 2, "RB": 2}
        new_mock = self.mock.loc[self.mock["VALUERANK"] <= self.total_teams * 15]

        print()
        for position in modifier:
            total_top = len(new_mock.loc[new_mock["POS"] == position])
            print(
                position,
                ": ",
                total_top,
                (total_top / (self.total_teams * modifier[position])) * 10,
            )

    def recommend(self) -> None:
        """Recommends who to draft"""
        # TODO print all columns
        print("Team " + str(self.current_team) + "'s draft!")
        print(str(self.current_round) + " roster pick")
        self.scarcity()
        print("\nTop pick:")
        print(self.mock.head(1))
        self.suggestions()


class AutomatedDraft(Draft):
    def __init__(self, file_path: str, total_teams: int) -> None:
        self.increment = 1
        self.current_round = 1
        self.current_team = 1
        self.total_teams = total_teams
        self.file_path = file_path
        self.mock = pd.read_csv(file_path)
        self.draft = {"PLAYER": [], "POS": [], "TEAM": [], "ORDER": [], "VOR": []}

    def draft_player(self, player: str) -> None:
        """Drafts a single player by adding them to self.draft

        Args:
            player (str): The name of the player that's being added
        """
        super().draft_player(player)
        self.mock.to_csv(self.file_path, index=False)
