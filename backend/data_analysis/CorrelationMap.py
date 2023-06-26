from datetime import date
from backend.utils import find_in_data_folder
import backend.CollectPlayerData
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import re
import multiprocessing


def main(start_year, end_year):
    with multiprocessing.Pool() as pool:
        pool.apply_async(qb(start_year, end_year))
        pool.apply_async(wr_te(start_year, end_year))
        pool.apply_async(rb(start_year, end_year))
        pool.close()
        pool.join()
        pool.terminate()


def qb(start_year, end_year):
    df = pd.DataFrame()
    for year in range(start_year, end_year + 1):
        qb_df = pd.read_csv(
            find_in_data_folder("HistoricData/qb_data_" + str(year) + ".csv")
        )
        qb_df = qb_df.drop("RANK", axis=1)
        # df = df.append(qb_df) #DEPRECATED
        df = pd.concat([df, qb_df])

    make_map(df, name=find_in_data_folder("CorrelationMatrix/qb_matrix.png"))


def rb(start_year, end_year):
    df = pd.DataFrame()
    for year in range(start_year, end_year + 1):
        rb_df = pd.read_csv(
            find_in_data_folder("HistoricData/rb_data_" + str(year) + ".csv")
        )
        rb_op_df = pd.read_csv(
            find_in_data_folder("HistoricData/rb_opportunity_" + str(year) + ".csv")
        )
        rb_share_df = pd.read_csv(
            find_in_data_folder("HistoricData/rb_share_" + str(year) + ".csv")
        )

        values = rb_op_df["RA/G"]
        rb_df = rb_df.join(values)

        values = rb_share_df[["Avg. Rushing Share", "Avg. Rushing Yards Share"]]
        rb_df = rb_df.join(values)
        rb_df = rb_df.drop("RUSHING 20+", axis=1)
        rb_df = rb_df.drop("RANK", axis=1)
        # df = df.append(rb_df) #DEPRECATED
        df = pd.concat([df, rb_df])
    df = df[
        [
            "PLAYER",
            "RUSHING ATT",
            "RUSHING YDS",
            "RUSHING Y/A",
            "RUSHING LG",
            "RUSHING TD",
            "REC",
            "TGT",
            "YDS",
            "Y/R",
            "TD",
            "FL",
            "ROST",
            "POS",
            "IT",
            "IT/G",
            "RA/G",
            "Avg. Rushing Share",
            "Avg. Rushing Yards Share",
            "G",
            "FPTS",
            "FPTS/G",
        ]
    ]

    make_map(df, name=find_in_data_folder("CorrelationMatrix/rb_matrix.png"))


def wr_te(start_year, end_year):
    final_wr_df = pd.DataFrame()
    final_te_df = pd.DataFrame()
    for year in range(start_year, end_year + 1):
        df = pd.read_csv(
            find_in_data_folder("HistoricData/wr-te_data_" + str(year) + ".csv")
        )
        df = df.drop("20+", axis=1)

        wr_df = df.loc[df["POS"] == "WR"]
        wr_df = get_players(wr_df)

        te_df = df.loc[df["POS"] == "TE"]
        te_df = get_players(te_df)

        share_df = pd.read_csv(
            find_in_data_folder("HistoricData/wr-te_wopr_" + str(year) + ".csv")
        )
        share_df["PLAYER"] = share_df["Receiver"]

        wr_df = merge(wr_df, share_df)

        te_df = merge(te_df, share_df)

        # final_wr_df = final_wr_df.append(wr_df) #DEPRECATED
        final_wr_df = pd.concat([final_wr_df, wr_df])
        # final_te_df = final_te_df.append(te_df) #DEPRECATED
        final_te_df = pd.concat([final_te_df, te_df])

    make_map(final_wr_df, name=find_in_data_folder("CorrelationMatrix/wr_matrix.png"))
    make_map(final_te_df, name=find_in_data_folder("CorrelationMatrix/te_matrix.png"))


def get_players(df):
    df["PLAYER"] = df["PLAYER"].apply(lambda x: re.sub(" \(.+\)", "", x))
    df["PLAYER"] = df["PLAYER"].apply(lambda x: re.sub(" Sr.", "", x))
    df["PLAYER"] = df["PLAYER"].apply(lambda x: re.sub(" Jr.", "", x))
    df["PLAYER"] = df["PLAYER"].apply(
        lambda x: re.sub("[^A-Z]+", ".", x.split(" ")[0]) + x.split(" ")[-1]
    )
    return df


def make_map(df, name):
    corre_map = df.corr()
    sn.heatmap(corre_map, annot=True)

    figure = plt.gcf()
    figure.set_size_inches(12, 10)
    plt.savefig(name, dpi=100)
    plt.close()


def merge(df, df2):
    df = df.merge(df2, on="PLAYER", how="outer")
    df["Total Air Yards"] = df["Avg. Air Yards"] * df["G"]
    df = df[
        [
            "PLAYER",
            "REC",
            "TGT",
            "YDS",
            "Y/R",
            "RUSHING ATT",
            "RUSHING YDS",
            "FL",
            "G",
            "Total Air Yards",
            "Avg. Target Share",
            "Avg. Air Yards Share",
            "Avg. Air Yards",
            "Avg. WOPR",
            "FPTS/G",
            "FPTS",
        ]
    ]
    return df


if __name__ == "__main__":
    today = date.today()
    year = today.year
    if today.month == 1:
        year -= 1

    end_year = year
    start_year = 2002

    # CollectPlayerData.collect_all_data(start_year, end_year)

    main(start_year, end_year)
