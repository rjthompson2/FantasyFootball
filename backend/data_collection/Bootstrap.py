from sklearn.utils import resample
from matplotlib import pyplot as plt
from itertools import repeat
import seaborn as sns

sns.set_style("whitegrid")
import numpy as np
import pandas as pd
import itertools
import multiprocessing
import logging


LOG = logging.getLogger(__name__)


plt.close("all")


def get_bootstrap(fpts_df: pd.DataFrame):
    data = []
    callback_list = []
    players = fpts_df["PLAYER"].unique()
    with multiprocessing.Pool() as pool:
        data = pool.starmap(mp_bootstrap, zip(players, repeat(fpts_df)))
        pool.close()
        pool.join()
        pool.terminate()
    # for player in players:
    #     data.append(mp_bootstrap(player, fpts_df))
    return data


def mp_bootstrap(player: str, fpts_df: pd.DataFrame):
    new_df = fpts_df.loc[fpts_df["PLAYER"] == player]
    new_df = new_df.drop(columns=["PLAYER", "POS"])
    new_df = new_df.dropna(axis=1, how="all").dropna()
    
    # More than length 1: everything worked
    if len(new_df.values.tolist()) > 1:
        new_list = [new_df.values.tolist()]
        output = calculate_ceiling_floor(
            arrays=new_list, player_names=[player], stdout=False
        )
        return output
    
    # Less than length 1: no data
    elif len(new_df.values.tolist()) < 1:
        return None

    mean = new_df.values.tolist()[0][0]


    # Exactly length 1: not enough data to produce ceiling and floor
    if mean != 0:
        return {
            "player": player,
            "mean": mean,
            "ceiling": "N/A",
            "floor": "N/A",
            "std": "N/A",
        }
    return None


def get_cf(data: list) -> pd.DataFrame:
    """Gets each player's ceiling and floor for the best/worst they might perform"""
    temp_df = []
    for dictionary in data:
        if dictionary != None:
            values = [
                dictionary["player"],
                dictionary["mean"],
                dictionary["ceiling"],
                dictionary["floor"],
                dictionary["std"],
            ]
            temp_df.append(
                pd.DataFrame([values], columns=["PLAYER", "FPTS", "C", "F", "STD"])
            )
    cf_df = pd.concat(temp_df)
    return cf_df


def calculate_bootstrap_df(
    *proj_points_arrays: tuple, player_names=None, n_iterations=10000
) -> pd.DataFrame:
    df_data = {}

    for i, arr in enumerate(proj_points_arrays):
        proj_points_means = []
        for n in range(n_iterations):
            # find boostrap resample array
            boot = resample(arr, n_samples=len(arr))
            # append the mean of the boostrap array to a list of means
            proj_points_means.append(np.mean(boot))

        # if player names are provided, set the player names as the column values
        # otherwise, use player_1, player_2, player_3, etc.
        if player_names:
            df_data[player_names[i]] = proj_points_means
        else:
            df_data[f"player_{i+1}"] = proj_points_means

    return pd.DataFrame(df_data)


def plot_kde(*args: tuple, figsize=(10, 8), **kwargs: dict) -> None:
    # Plot each player's bootstrapped means as a kernel density estimation

    df = calculate_bootstrap_df(*args, **kwargs)  # get boostrap df
    df.plot.kde()  # plot as kernel density estimation

    fig, ax = plt.gcf(), plt.gca()  # get current figure, current axis from above
    fig.set_size_inches(figsize)
    colors = itertools.cycle(["blue", "orange", "green", "orange"])

    for i, (arr, color) in enumerate(zip(args, colors)):
        l = ax.lines[i]
        x = l.get_xydata()[:, 0]
        y = l.get_xydata()[:, 1]
        ax.fill_between(
            x, y, color=color, alpha=0.2
        )  # fill in the area underneath the KDE plots with their associated color
        x_loc = x[
            np.where(y == y.max())[0]
        ]  # find the x-location of the max of each KDE
        ax.vlines(
            x=x_loc, ymax=y.max(), ymin=0, linestyles="dashed", alpha=0.5, color=color
        )  # plot a vertical line leading up to the max of the KDE

    plt.show()


def calculate_ceiling_floor(arrays=[[]], player_names=None, stdout=False) -> dict:
    for i, arr in enumerate(arrays):
        boot = calculate_bootstrap_df(arr, player_names=player_names).values
        mean = boot.mean()  # find the mean of the means

        ceiling = np.percentile(
            boot, 95
        )  # find the upper bound of the confidence interval
        floor = np.percentile(
            boot, 5
        )  # find the lower bound of the confidence interval
        std = np.std(boot)

        data = {
            "player": "Player " + str(i),
            "mean": mean,
            "ceiling": ceiling,
            "floor": floor,
            "std": std,
        }

        if player_names != None:
            data["player"] = player_names[i]

    if stdout:
        for player, player_data in data.items():
            print(
                player_data["player"],
                "has a mean projected output of",
                round(player_data["mean"], 2),
                "a ceiling of",
                round(player_data["ceiling"], 2),
                "and a floor of",
                round(player_data["floor"], 2),
                "with a standard deviation of",
                round(player_data["std"], 2),
            )
            print("\n")

    return data
