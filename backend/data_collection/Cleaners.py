import re
import logging
import pandas as pd
from typing import List
from backend.data_collection.utils import clean_name, change_team_name, Positions


LOG = logging.getLogger(__name__)


class ADPCleaner:
    """Cleans the average draaft pick for each player"""

    def clean_data(self, df):
        df = df[["Player Team (Bye)", "POS", "AVG"]]
        df["PLAYER"] = df["Player Team (Bye)"].apply(
            lambda x: " ".join(x.split()[:-2])
            if x.split()[-1] != "DST"
            else " ".join(x.split()[:-1])
        )  # removing the team and position
        df = clean_name(df)
        df["POS"] = df["POS"].apply(
            lambda x: x[:1] if x[0] == "K" else (x[:3] if x[:3] == "DST" else x[:2])
        )  # removing the position rank
        df = df[["PLAYER", "POS", "AVG"]].sort_values(by="AVG")
        return df


class FPTSCleaner:
    """Cleans the predicted Fantasy Points for each player"""

    def clean_data(self, df_dict: dict) -> pd.DataFrame:
        df = pd.DataFrame()
        df_list = []

        for data in df_dict.keys():
            temp = df_dict[data]
            if data == "TableBase-table":
                df_list += [
                    self.fpts_multi_index_output(position.value, temp[position.value])
                    for position in Positions
                ]  # collect data with list comprehensions
            elif data == "projections":
                df_list += [
                    self.new_fpts_output(position.value, temp[position.value])
                    for position in Positions
                    if position.value not in ["k", "dst"]
                ]
            else:
                df_list += [
                    self.fpts_output(
                        position.value, temp[position.value], ["k", "dst"], "FPTS"
                    )
                    for position in Positions
                ]

        df = pd.concat(df_list)
        df = df.sort_values(
            by="FPTS", ascending=False
        )  # sort df in descending order on FPTS column
        return df

    # TODO better names
    def fpts_output(
        self, position: str, df: pd.DataFrame, check_array: List[str], ftps: str
    ) -> pd.DataFrame:
        if position not in check_array:
            df.columns = df.columns.droplevel(
                level=0
            )  # our data has a multi-level column index. The first column level is useless so let's drop it.
        df["PLAYER"] = df["Player"].apply(
            lambda x: re.sub("\.", "", " ".join(x.split()[:-1]))
        )  # fixing player name to not include team
        df["PLAYER"] = change_team_name(df["PLAYER"])
        df["FPTS"] = df[ftps]
        df["POS"] = position.upper()  # add a position column
        df = df[["PLAYER", "POS", "FPTS"]]
        df = clean_name(df)
        return df

    def new_fpts_output(self, position: str, df: pd.DataFrame) -> pd.DataFrame:
        df["PLAYER"] = change_team_name(df[1])  # fixing player name to not include team
        df["FPTS"] = df[len(df.columns) - 2]
        df["POS"] = position.upper()  # add a position column
        df = df[["PLAYER", "POS", "FPTS"]]
        df = clean_name(df)
        return df

    def fpts_multi_index_output(self, position: str, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = df.columns.droplevel(level=0)
        if position != "dst":
            df["PLAYER"] = df["Player"].apply(
                lambda x: re.sub("\.", "", " ".join(x.split()[4:6]))
            )
        else:
            # TODO change names to long form
            df["PLAYER"] = change_team_name(df["Team"])
        df["POS"] = position.upper()
        df = df.loc[df["fpts  Fantasy Points"] != "—"]
        df["FPTS"] = df["fpts  Fantasy Points"].apply(lambda x: float(x))
        df = df[["PLAYER", "POS", "FPTS"]]
        df = df.sort_values(by="FPTS", ascending=False)
        df = clean_name(df)
        return df


class InjuryCleaner:
    """Cleans the injury data for each player"""

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(
            columns={
                "player-name": "PLAYER",
                "injury-count": "CI",
                "injury-percent": "IJ%",
                "proj-games-missed": "PGM",
                "prob-injury-per-game": "IPG%",
                "durability-score": "D",
            }
        )
        df["PLAYER"] = df["PLAYER"].apply(lambda x: x.split(",")[0])
        df["IJ%"] = df["IJ%"].apply(
            lambda x: x.translate({ord(" "): None, ord("\n"): None})
        )
        df = clean_name(df)
        return df


class ESPNCleaner:
    """Cleans the injury data for each player"""

    def clean_data(self, data: dict) -> pd.DataFrame:
        data_list = data["players"]
        names = [data["player"]["fullName"] for data in data_list]
        fpts = [
            data["player"]["stats"][-1]["appliedTotal"]
            if "stats" in data["player"]
            else None
            for data in data_list
        ]
        return pd.DataFrame({"PLAYER": names, "FPTS": fpts})


class ECRCleaner:
    """Cleans the injury data for each player"""

    def clean_data(self, data: dict) -> pd.DataFrame:
        data_list = data["players"]
        names = [data["player_name"] for data in data_list]
        ranks = [data["rank_ecr"] for data in data_list]
        df = pd.DataFrame({"PLAYER": names, "ECR": ranks})
        df = df.dropna()
        df["PLAYER"] = df["PLAYER"].apply(lambda x: re.sub("\s\(.*", "", x))
        df = clean_name(df)
        return df


class CBSCleaner:
    """Cleans the data from cbs' site"""
    #TODO make a cleaner for CBS data
    def clean_data(self, data: list) -> pd.DataFrame:
        data_list = []
        for pos_list in data:
            if pos_list[0] == "Running":
                data_list.append(self.data_cleaner(pos_list, [52, 12, 14]))
            elif pos_list[0] == "Passing":
                data_list.append(self.data_cleaner(pos_list, [54, 13, 15]))
            elif pos_list[0] == "Tight":
                data_list.append(self.data_cleaner(pos_list, [37, 8, 10]))
            elif pos_list[0] == "Wide":
                data_list.append(self.data_cleaner(pos_list, [52, 12, 14]))
            elif pos_list[0] == "FG":
                data_list.append(self.data_cleaner(pos_list, [69, 16, 18]))
            elif pos_list[0] == "Defense/Special":
                data_list.append(self.data_cleaner(pos_list, [66, 13, 15], dst=True))
            else:
                print(pos_list)
                exit()
        return pd.concat(data_list)

    def data_cleaner(self, data: list, prunes: list, dst=False) -> pd.DataFrame:
        columns = data[:prunes[0]]
        data = data[prunes[0]:]
        regexp = re.compile(r'[A-Z]')
        players = []
        fpts = []
        while data != []:
            j = 0
            names = []
            while regexp.search(data[j][0]):
                names.append(data[j])
                j+=1
            if not dst:
               players.append(" ".join([name for name in names[len(names)//2:]]))
            else:
                players.append(" ".join([name for name in names]))
            data = data[j:]
            fpts.append(data[prunes[1]])
            data = data[prunes[2]:]
        return pd.DataFrame({"PLAYERS": players, "FPTS":fpts})
