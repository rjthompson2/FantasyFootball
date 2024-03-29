from datetime import date
from backend.utils import find_in_data_folder
import re
import pandas as pd
import matplotlib.pyplot as plt


def main(year):
    df_rush_share = pd.read_csv(find_in_data_folder("rush_share_" + str(year) + ".csv"))
    df_rush_yards = pd.read_csv(
        find_in_data_folder("rush_yards_share_" + str(year) + ".csv")
    )
    df_wopr = pd.read_csv(find_in_data_folder("wopr_" + str(year) + ".csv"))
    # df_rush_attempt = pd.read_csv(find_in_data_folder("rush_attempts_" + str(year) + ".csv"))
    # df_targets = pd.read_csv(find_in_data_folder("reciever_tgts_" + str(year) + ".csv"))
    df_it = pd.read_csv(find_in_data_folder("rush_it_" + str(year) + ".csv"))

    for team in df_rush_share["TEAM"].unique():
        plot(df_rush_share, team, value="Rushing Share", year=year)
        plot(df_rush_yards, team, value="Rushing Yards Share", year=year)
        plot(df_wopr, team, value="WOPR", year=year)
        plot(df_it, team, value="Implied Touches", year=year)


def plot(df, team, value, year=None):
    colors = ["b", "g", "r", "c", "m", "y", "k"]
    patterns = [".", "x", "*", "^", "s"]
    c = 0
    p = 0

    df = df.loc[df["TEAM"] == team]
    columns = [
        column for column in df.columns if column not in ["PLAYER", "TEAM", "AVG"]
    ]
    new_df = df[columns]

    plt.figure()
    for i in range(len(new_df.index)):
        plt.plot(
            columns, new_df.iloc[i], colors[c] + patterns[p], label=df.iloc[i]["PLAYER"]
        )
        plt.plot(columns, new_df.iloc[i], colors[c])

        # iterate through colors and patterns
        # loop back to the beginning of each list when the index exceeds the list's length
        c += 1
        c %= len(colors)
        # only proceed to the next pattern type when the color resets to index 0
        if c == 0:
            p += 1
            p %= len(patterns)

    plt.title(team + " Weekly " + value)
    plt.xlabel("Week")
    plt.ylabel(value)
    if len(new_df.columns) > 9:
        plt.legend(loc="upper left")
    else:
        plt.legend(loc="upper right")

    if year:
        plt.savefig(
            find_in_data_folder(
                "WeeklyTeam"
                + re.sub(" ", "", value)
                + "/"
                + str(year)
                + "_"
                + team
                + "_"
                + re.sub(" ", "_", value.lower())
                + ".png"
            )
        )
    else:
        plt.savefig(
            find_in_data_folder(
                "WeeklyTeam"
                + re.sub(" ", "", value)
                + "/"
                + team
                + "_"
                + re.sub(" ", "_", value.lower())
                + ".png"
            )
        )
    plt.close()


if __name__ == "__main__":
    today = date.today()
    year = today.year
    if today.month == 1:
        year -= 1
    main(year=year)
