import CollectPlayerData as cpd
import numpy as np
import math
from WebScraper import *
from os.path import exists
from datetime import date, datetime
import matplotlib.pyplot as plt

plt.close("all")

today = date.today()
year = today.year
if today.month == 1:
    year -= 1

URL = "https://www.prosportstransactions.com/football/Search/SearchResults.php?Player=&Team=&BeginDate=1900-01-01&EndDate=2022-03-11&ILChkBx=yes&submit=Search&start=0"

# TODO WIP
def gather_injury_data() -> None:
    ws = InjuryScraper()
    ws.start(url=URL, headless=True)
    if exists("data/injury_data.csv"):
        old_df = pd.read_csv("data/injury_data.csv")
        df = None
        i = len(old_df) // 25
        print(i)
        try:
            ws.find(i)
        except:
            df = old_df
        if df == None:
            df_list = ws.collect_all()
            df = pd.concat(df_list)
            # df = old_df.append(df) #deprecated
            df = pd.concat([old_df, df])
    else:
        df_list = ws.collect_all()
        df = pd.concat(df_list)
    df = df.drop_duplicates()
    df.to_csv(r"data/injury_data.csv", index=False, header=True)


def clean_injury_data() -> pd.DataFrame:
    injury_df = pd.read_csv("data/injury_data.csv")
    pd.set_option("display.max_columns", None)

    aquired_df = injury_df[~injury_df["Acquired"].isnull()]
    aquired_df = aquired_df.drop("Relinquished", axis=1)

    relinquished_df = injury_df[~injury_df["Relinquished"].isnull()]
    relinquished_df = relinquished_df.drop("Acquired", axis=1)

    df = pd.DataFrame(columns=["Name", "Team", "Relinquished", "Acquired", "Notes"])
    aquired_df = aquired_df.reset_index()
    i = 0

    for index, row in relinquished_df.iterrows():
        new_row = pd.DataFrame(
            {
                "Name": row["Relinquished"],
                "Team": row["Team"],
                "Acquired": None,
                "Relinquished": row["Date"],
                "Notes": row["Notes"],
            },
            index=[i],
        )
        i += 1
        # df = df.append(new_row) #DEPRECATED
        df = pd.concat([df, new_row])


    for index, row in aquired_df.iterrows():
        i = df.index[df["Name"] == row["Acquired"]]
        if len(i) > 0:
            for value in i:
                if df.iloc[value]["Acquired"] == None:
                    current = value
                    break
        else:
            current = i
        old = pd.to_datetime(row["Date"], infer_datetime_format=True)
        new = pd.to_datetime(
            df["Relinquished"].iloc[current], infer_datetime_format=True
        )
        if not isinstance(new, pd.core.series.Series) and (old > new):
            df.iloc[current]["Acquired"] = row["Date"]

    df.to_csv(r"data/injury_data_combined.csv", index=False, header=True)
    return df


def df_normalize() -> None:
    df = pd.read_csv("data/injury_data_combined.csv")
    numerical_df = pd.DataFrame(columns=["Description", "Time"])
    i = 0

    for index, row in df.iterrows():
        if row["Acquired"] != None and not pd.isna(row["Acquired"]):
            print(row["Acquired"])
            acquired = pd.to_datetime(row["Acquired"], infer_datetime_format=True)
            relinquished = pd.to_datetime(
                row["Relinquished"], infer_datetime_format=True
            )
            new_row = pd.DataFrame(
                {"Description": row["Notes"], "Time": (acquired - relinquished)},
                index=[i],
            )
            i += 1
            # numerical_df = numerical_df.append(new_row) #DEPRECATED
            numerical_df = pd.concat([numerical_df, new_row])

    numerical_df.to_csv(r"data/injury_data_numerical.csv", index=False, header=True)


def normal_dist(df: pd.DataFrame) -> None:
    df["Time"] = df["Time"].apply(lambda x: int(x.strip(" days")))
    plt.figure()
    df["Time"].hist()
    print(df.head())
    plt.show()


# TODO group by notes
def _groupby(_filter: str, df: pd.DataFrame) -> dict:
    return {_filter: df}


if __name__ == "__main__":
    # gather_injury_data()
    # clean_injury_data()
    # df_normalize()
    df = pd.read_csv("data/injury_data_numerical.csv")
    normal_dist(df)
