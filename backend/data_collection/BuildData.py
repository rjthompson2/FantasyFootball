from backend.data_collection.WebScraper import Scraper
from backend.data_collection.utils import Positions

# from Teams import *
from typing import Tuple, List
import pandas as pd
import re
import logging
import numpy as np


LOG = logging.getLogger(__name__)


# TODO maybe split into smaller chunks and give each chunk its own python file
def build_players(df: pd.DataFrame) -> Tuple[dict, dict]:
    replacement_players = {}
    replacement_values = {}
    values = {"QB": 24, "RB": 48, "WR": 48, "TE": 24}

    df_list = [df.loc[df["POS"] == x] for x in list(values.keys())]

    for pos_df in df_list:
        position = pos_df["POS"].unique()[0]
        shortened_df = pos_df.iloc[: values[position]]
        for _, row in shortened_df.iterrows():
            player = row["PLAYER"]
            replacement_players[position] = player

    for position, player in replacement_players.items():
        if Positions.has_value(position.lower()):
            replacement_values[position] = df.loc[df["PLAYER"] == player].values[0, 2]

    return replacement_players, replacement_values


def player_data(BASE_URL: str, data, ws: Scraper, pos: str) -> pd.DataFrame:
    final_df = pd.DataFrame()
    df_list = [
        build_player_data(
            ws.new_collect(BASE_URL.format(position=position), "id", data), position
        )
        for position in pos
    ]  # collect data with list comprehensions
    final_df = pd.concat(df_list)
    return final_df


def build_player_data(df: pd.DataFrame, position: str) -> pd.DataFrame:
    new_df = pd.DataFrame()
    for column in df.columns:
        if column[0] in ["PASSING", "RUSHING"]:
            new_df[column[0] + " " + column[1]] = df[column]
        else:
            new_df[column[1].upper()] = df[column]
    new_df["POS"] = position.upper()
    return new_df


def build_drafting_data(df: pd.DataFrame) -> pd.DataFrame:
    changes = {
        "Patrick Mahomes": "Patrick Mahomes II",
        "Darrell Henderson Jr": "Darrell Henderson",
    }
    df = df.iloc[::-1]  # inverts data
    df = df.loc[~df["Player"].str.contains("Round")]
    df["Player"] = df["Player"].apply(
        lambda x: re.sub("\.", "", x)
    )  # removing punctuation
    df["Player"] = df["Player"].apply(
        lambda x: re.sub("QB$|WR$|RB$|TE$|K$|DEF$", "", x)
    )  # removing positions
    df["Player"] = df["Player"].apply(
        lambda x: re.sub(
            "NE$|LV$|Phi$|NYJ$|Pit$|Hou$|Jax$|Ari$|Ten$|TB$|Det$|SF$|Ind$|Atl$|NYG$|Mia$|KC$|NO$|GB$|LAC$|Buf$|Car$|LAR$|Cle$|Bal$|Cin$|Dal$|Min$|Chi$|Den$|Sea$|Was$",
            "",
            x,
        )
    )  # removing teams
    df["Player"] = df["Player"].apply(
        lambda x: re.sub("[ \t]+$", "", x)
    )  # removing any spaces at the end
    df["Player"] = df["Player"].replace(changes)  # getting the correct names
    return df


# TODO DONT DELETE!
# def build_teams(df:pd.DataFrame) -> Teams:
#     '''Builds the teams from the given pandas dataframe'''
#     total_teams = df.sort_values(by='TEAM', ascending=False).iloc[0]['TEAM']
#     teams = Teams([])
#     for i in range(total_teams):
#         temp = df.loc[df['TEAM'] == i + 1]
#         team = Team(i + 1, [])
#         for j in range(len(temp)):
#             team.players.append(Player(temp.iloc[j]["PLAYER"], temp.iloc[j]["POS"], temp.iloc[j]["ORDER"], temp.iloc[j]["VOR"]))
#         teams.teams.append(team)
#     return teams


def calculate_VOR(
    df: pd.DataFrame, final_df: pd.DataFrame, replacement_values: dict
) -> pd.DataFrame:
    df["VOR"] = df.apply(
        lambda row: row["FPTS"] - replacement_values[row["POS"]]
        if (row["POS"] != "DST" and row["POS"] != "K")
        else None,
        axis=1,
    )
    df = df.sort_values(by="VOR", ascending=False)
    df["VALUERANK"] = df["VOR"].rank(ascending=False)

    final_df["ADPRANK"] = final_df["AVG"].rank(
        method="first"
    )  # set method=first so we don't average the ranks on ties.
    final_df = df.merge(final_df, how="left", on=["PLAYER", "POS"])
    final_df["SLEEPERSCORE"] = final_df["ADPRANK"] - final_df["VALUERANK"]
    return final_df


def opportunity(df: pd.DataFrame) -> pd.DataFrame:
    df["TGT/G"] = round(df["TGT"] / df["G"], 2)
    df["RA/G"] = round(df["RUSHING ATT"] / df["G"], 2)
    df["COMPLETION %"] = round((df["REC"] / df["TGT"]) * 100, 2)
    df["IT"] = df["TGT"] + df["RUSHING ATT"]
    df["IT/G"] = round(df["IT"] / df["G"], 2)
    df = df[
        [
            "PLAYER",
            "POS",
            "TGT",
            "TGT/G",
            "COMPLETION %",
            "RUSHING ATT",
            "RA/G",
            "G",
            "IT",
            "IT/G",
            "FPTS",
            "FPTS/G",
        ]
    ]
    return df


################################################
# TODO overlap with other functions, make generic
def flex_wopr(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        raise Exception("DataFrame Empty")
    rec_df = (
        df.groupby(["receiver_player_id", "posteam", "game_id"], as_index=False)[
            [
                "pass_attempt",
                "yards_gained",
                "air_yards",
                "complete_pass",
                "pass_touchdown",
                "touchdown",
            ]
        ]
        .sum()
        .assign(
            raw_rec_fpts=lambda x: x.yards_gained * 0.1
            + x.complete_pass
            + x.pass_touchdown * 6
        )
    )
    team_stats = (
        df.loc[(df["pass_attempt"] == 1) & (df["receiver_player_id"].notnull())]
        .groupby(["game_id", "posteam"], as_index=False)[["air_yards", "pass_attempt"]]
        .sum()
    )
    rec_df = rec_df.merge(
        team_stats, on=["game_id", "posteam"], suffixes=("_player", "_team")
    )
    rec_df["target_share"] = round(
        (rec_df["pass_attempt_player"] / rec_df["pass_attempt_team"]) * 100, 2
    )
    rec_df["air_yards_share"] = round(
        (rec_df["air_yards_player"] / rec_df["air_yards_team"]) * 100, 2
    )
    rec_df = (
        rec_df.groupby(["receiver_player_id"], as_index=False)
        .mean()
        .sort_values(by="raw_rec_fpts", ascending=False)
    )
    rec_df = rec_df[
        [
            "receiver_player_id",
            "raw_rec_fpts",
            "pass_attempt_player",
            "air_yards_player",
            "target_share",
            "air_yards_share",
        ]
    ].rename(
        columns={
            "pass_attempt_player": "Avg. Targets",
            "air_yards_player": "Avg. Air Yards",
            "raw_rec_fpts": "Avg. Raw Fpts",
            "air_yards_share": "Avg. Air Yards Share",
            "target_share": "Avg. Target Share",
        }
    )
    rz = (
        df.loc[
            (df["pass_attempt"] == 1) & (df["receiver_player_id"].notnull()),
            ["receiver_player_id", "air_yards", "yardline_100", "pass_touchdown"],
        ]
        .assign(
            pass_loc=lambda x: x.yardline_100 - x.air_yards,
            redzone_look=lambda x: x.pass_loc <= 20,
        )
        .groupby("receiver_player_id", as_index=False)["redzone_look"]
        .sum()
        .sort_values(by="redzone_look", ascending=False)
        .rename(columns={"redzone_look": "Redzone Looks"})
    )
    rec_df = rec_df.merge(rz, on="receiver_player_id")
    player_id_table = df.groupby(["receiver_player_id"], as_index=False)[
        ["posteam", "receiver_player_name"]
    ].first()
    # reorganizing some columns after merging
    rec_df = rec_df.merge(player_id_table, on="receiver_player_id")[
        ["receiver_player_name", "posteam"] + rec_df.columns.tolist()
    ]
    rec_df = rec_df.rename(
        columns={"receiver_player_name": "Receiver", "posteam": "Team"}
    )
    # creating WOPR column
    rec_df["Avg. WOPR"] = round(
        (rec_df["Avg. Target Share"] * 1.5 + rec_df["Avg. Air Yards Share"] * 0.7), 2
    )

    # merging total FPTS scored in to our original df
    rec_df = (
        rec_df.merge(
            df.groupby(["receiver_player_id"], as_index=False)[
                ["yards_gained", "complete_pass", "touchdown"]
            ]
            .sum()
            .assign(
                total_fpts=lambda x: round(
                    x.yards_gained * 0.1 + x.touchdown * 6 + x.complete_pass, 1
                )
            ),
            on="receiver_player_id",
        )
        .sort_values(by="total_fpts", ascending=False)
        .drop(columns=["yards_gained", "complete_pass", "touchdown"])
    )
    rec_df = rec_df[
        [column for column in rec_df.columns if column != "receiver_player_id"]
    ]

    return rec_df


def rb_share(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        raise Exception("DataFrame Empty")
    rush_df = (
        df.groupby(["rusher_player_id", "posteam", "game_id"], as_index=False)[
            [
                "rush_attempt",
                "pass_attempt",
                "yards_gained",
                "complete_pass",
                "rushing_yards",
                "rush_touchdown",
                "touchdown",
            ]
        ]
        .sum()
        .assign(
            raw_rush_fpts=lambda x: x.yards_gained * 0.1
            + x.complete_pass
            + x.touchdown * 6
        )
    )
    team_stats = (
        df.loc[(df["rush_attempt"] == 1) & (df["rusher_player_id"].notnull())]
        .groupby(["game_id", "posteam"], as_index=False)[
            ["rushing_yards", "rush_attempt", "pass_attempt"]
        ]
        .sum()
    )
    rush_df = rush_df.merge(
        team_stats, on=["game_id", "posteam"], suffixes=("_player", "_team")
    )
    rush_df["rush_share"] = round(
        (rush_df["rush_attempt_player"] / rush_df["rush_attempt_team"]) * 100, 2
    )
    rush_df["rushing_yards_share"] = round(
        (rush_df["rushing_yards_player"] / rush_df["rushing_yards_team"]) * 100, 2
    )
    rush_df = (
        rush_df.groupby(["rusher_player_id"], as_index=False)
        .mean()
        .sort_values(by="raw_rush_fpts", ascending=False)
    )
    rush_df = rush_df[
        [
            "rusher_player_id",
            "raw_rush_fpts",
            "rush_attempt_player",
            "rushing_yards_player",
            "rush_share",
            "rushing_yards_share",
        ]
    ].rename(
        columns={
            "rush_attempt_player": "Avg. Rushing Attempt",
            "rushing_yards_player": "Avg. Rushing Yards",
            "raw_rush_fpts": "Avg. Raw Fpts",
            "rushing_yards_share": "Avg. Rushing Yards Share",
            "rush_share": "Avg. Rushing Share",
        }
    )
    rz = (
        df.loc[
            (df["rush_attempt"] == 1) & (df["rusher_player_id"].notnull()),
            ["rusher_player_id", "rushing_yards", "yardline_100", "rush_touchdown"],
        ]
        .assign(
            rush_loc=lambda x: x.yardline_100 - x.rushing_yards,
            redzone_look=lambda x: x.rush_loc <= 10,
            greenzone_look=lambda x: x.rush_loc <= 5,
        )
        .groupby("rusher_player_id", as_index=False)["redzone_look", "greenzone_look"]
        .sum()
        .sort_values(by="redzone_look", ascending=False)
        .rename(
            columns={
                "redzone_look": "Redzone Looks",
                "greenzone_look": "Greenzone Looks",
            }
        )
    )
    rush_df = rush_df.merge(rz, on="rusher_player_id")
    player_id_table = df.groupby(["rusher_player_id"], as_index=False)[
        ["posteam", "rusher_player_name"]
    ].first()
    # reorganizing some columns after merging
    rush_df = rush_df.merge(player_id_table, on="rusher_player_id")[
        ["rusher_player_name", "posteam"] + rush_df.columns.tolist()
    ]
    rush_df = rush_df.rename(
        columns={"rusher_player_name": "Rusher", "posteam": "Team"}
    )

    # merging total FPTS scored in to our original df
    rush_df = (
        rush_df.merge(
            df.groupby(["rusher_player_id"], as_index=False)[
                [
                    "rushing_yards",
                    "yards_gained",
                    "complete_pass",
                    "rush_touchdown",
                    "touchdown",
                ]
            ]
            .sum()
            .assign(
                total_fpts=lambda x: round(
                    x.yards_gained * 0.1 + x.touchdown * 6 + x.complete_pass, 1
                )
            ),
            on="rusher_player_id",
        )
        .sort_values(by="total_fpts", ascending=False)
        .drop(columns=["rushing_yards", "complete_pass", "rush_touchdown"])
    )
    rush_df = rush_df[
        [column for column in rush_df.columns if column != "rusher_player_id"]
    ]
    return rush_df


################################################


def df_combine(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    on: List[str],
    merge_values: List[str],
    convert_to=None,
):
    df1, df2 = check_convert_to(convert_to, df1, df2, merge_values)

    final_df = pd.DataFrame()
    for i in range(len(df1)):
        player = df1["PLAYER"][i]
        df_sum = check_list(player, df1, df2, on, merge_values, i)
        for column in on:
            df_sum[column] = df1[column][i]
        final_df = final_df.append(df_sum)
    
    final_df = final_df[on + merge_values]
    final_df = final_df[final_df["PLAYER"].notna()]
    final_df[merge_values] = final_df[merge_values].replace({"0": np.nan, 0: np.nan})

    final_df["AVG"] = final_df.mean(axis=1)
    return final_df

def check_convert_to(convert_to, df1, df2, merge_values):
    if not convert_to:
        return df1, df2
    for value in merge_values:
        df1[value] = pd.to_numeric(df1[value], downcast=convert_to)
        df2[value] = pd.to_numeric(df2[value], downcast=convert_to)
    return df1, df2

def check_list(player, df1, df2, on, merge_values, i):
    if not player in df2["PLAYER"].to_list():
        return df1.iloc[i].loc[merge_values].fillna(0)

    df_sum = df2.copy()
    for each in on:
        df_sum = df_sum.loc[df2[each] == df1[each][i]]
    df_sum = df_sum[merge_values].fillna(0)

    return df1.iloc[i].loc[merge_values].fillna(0).add(df_sum)