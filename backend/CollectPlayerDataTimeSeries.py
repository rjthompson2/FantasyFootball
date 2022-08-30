import backend.data_collection.BuildData as bd
import nfl_data_py as nfl
import pandas as pd
import numpy as np
from datetime import date
from backend.utils import find_in_data_folder


def main(year):
    df = nfl.import_pbp_data([year])

    weeks = df.week.unique()
    rb_data_list = []
    flex_data_list = []
    for week in weeks:
        temp_df = df.loc[df["week"] == week]
        rb_data_list.append(bd.rb_share(temp_df))
        flex_data_list.append(bd.flex_wopr(temp_df))

    df_rush_share = build(rb_data_list, "Rusher", "Avg. Rushing Share")
    df_rush_yards = build(rb_data_list, "Rusher", "Avg. Rushing Yards Share")
    df_wopr = build(flex_data_list, "Receiver", "Avg. WOPR")

    df_rush_share.to_csv(
        find_in_data_folder("rush_share_" + str(year) + ".csv"),
        header=True,
        index=False,
    )
    df_rush_yards.to_csv(
        find_in_data_folder("rush_yards_share_" + str(year) + ".csv"),
        header=True,
        index=False,
    )
    df_wopr.to_csv(
        find_in_data_folder("wopr_" + str(year) + ".csv"), header=True, index=False
    )


def build(data_list, player_type, value):
    delta_df = pd.DataFrame()
    for i in range(len(data_list)):
        new_df = pd.DataFrame()
        if i == 0:
            delta_df = get_values(data_list, i, player_type, value)
        else:
            new_df = get_values(data_list, i, player_type, value)
            delta_df = delta_df.merge(new_df, on=["PLAYER", "TEAM"], how="outer")

    delta_df["AVG"] = delta_df.mean(axis=1)
    return delta_df


def get_values(data_list, i, player_type, value):
    df = pd.DataFrame()
    df["PLAYER"] = data_list[i][player_type]
    df["TEAM"] = data_list[i]["Team"]
    df[i + 1] = data_list[i][value]
    return df


if __name__ == "__main__":
    today = date.today()
    year = today.year
    if today.month == 1:
        year -= 1
    main(year)
