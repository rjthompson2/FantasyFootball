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
    df_rush_attempt = build(rb_data_list, "Rusher", "Avg. Rushing Attempt")
    df_rush_rz = build(
        rb_data_list, "Rusher", "Redzone Looks", final_type=["total", "avg"]
    )
    df_rush_gz = build(
        rb_data_list, "Rusher", "Greenzone Looks", final_type=["total", "avg"]
    )
    df_wopr = build(flex_data_list, "Receiver", "Avg. WOPR")
    df_tgt = build(flex_data_list, "Receiver", "Avg. Targets")
    df_rec_rz = build(
        flex_data_list, "Receiver", "Redzone Looks", final_type=["total", "avg"]
    )
    df_it = bd.df_combine(
        df1=df_rush_attempt,
        df2=df_tgt,
        on=["PLAYER", "TEAM"],
        merge_values=df_rush_attempt.columns.to_list()[2:-1],
        convert_to="float",
    )

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
    df_rush_attempt.to_csv(
        find_in_data_folder("rush_attempts_" + str(year) + ".csv"),
        header=True,
        index=False,
    )
    # df_rush_rz.to_csv(
    #     find_in_data_folder("rush_rz_" + str(year) + ".csv"),
    #     header=True,
    #     index=False,
    # )
    df_rush_gz.to_csv(
        find_in_data_folder("rush_gz_" + str(year) + ".csv"),
        header=True,
        index=False,
    )
    df_rec_rz.to_csv(
        find_in_data_folder("rec_rz_" + str(year) + ".csv"),
        header=True,
        index=False,
    )
    df_wopr.to_csv(
        find_in_data_folder("wopr_" + str(year) + ".csv"),
        header=True,
        index=False,
    )
    df_tgt.to_csv(
        find_in_data_folder("reciever_tgts_" + str(year) + ".csv"),
        header=True,
        index=False,
    )
    df_it.to_csv(
        find_in_data_folder("rush_it_" + str(year) + ".csv"),
        header=True,
        index=False,
    )


def build(data_list, player_type, value, final_type=["avg"]):
    delta_df = pd.DataFrame()
    for i in range(len(data_list)):
        new_df = pd.DataFrame()
        if i == 0:
            delta_df = get_values(data_list, i, player_type, value)
        else:
            new_df = get_values(data_list, i, player_type, value)
            delta_df = delta_df.merge(new_df, on=["PLAYER", "TEAM"], how="outer")

    final_df = delta_df.copy()
    if "avg" in final_type:
        final_df["AVG"] = delta_df.mean(axis=1, numeric_only=True)
    if "total" in final_type:
        final_df["TOTAL"] = delta_df.sum(axis=1, numeric_only=True)
    return final_df


def get_values(data_list, i, player_type, value):
    df = pd.DataFrame()
    df["PLAYER"] = data_list[i][player_type]
    df["TEAM"] = data_list[i]["Team"]
    df[i + 1] = data_list[i][value]
    return df


if __name__ == "__main__":
    today = date.today()
    year = today.year
    # if today.month == 1:
    #     year -= 1
    main(year)
