from matplotlib import pyplot as plt
from scipy import stats
from io import BytesIO
from backend.utils import find_in_data_folder
import matplotlib as mpl
import numpy as np
import seaborn as sns
import pandas as pd
import backend.epa.main as epa
import requests

# TODO make plotting more general with standardized proportions
def main():
    schedule_epa = epa.epa_schedule([2022])

    plt.style.use("ggplot")

    schedule_epa = schedule_epa.set_index("Team")
    x = schedule_epa["Offense_EPA_Delta"].values
    y = schedule_epa["Defense_EPA_Delta"].values

    fig, ax = plt.subplots(figsize=(15, 15))

    ax.grid(alpha=0.5)
    # plot a vertical and horixontal line to create separate quadrants
    ax.vlines(0, -0.2, 0.2, color="#fcc331", alpha=0.7, lw=4, linestyles="dashed")
    ax.hlines(0, -0.2, 0.2, color="#fcc331", alpha=0.7, lw=4, linestyles="dashed")
    ax.set_ylim(-0.1, 0.1)
    ax.set_xlim(-0.1, 0.1)
    ax.set_xlabel("Offense_EPA_Delta", fontsize=20)
    ax.set_ylabel("Defense_EPA_Delta", fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    annot_styles = {
        "bbox": {
            "boxstyle": "round,pad=0.5",
            "facecolor": "none",
            "edgecolor": "#fcc331",
        },
        "fontsize": 20,
        "color": "#202f52",
    }

    # annotate the axis
    ax.annotate("Increasing Offense Difficulty", xy=(0.06, 0), **annot_styles)
    ax.annotate("Decreasing Offense Difficulty", xy=(-0.1, -0.015), **annot_styles)
    ax.annotate("Decreasing Defense Difficulty", xy=(-0.03, 0.08), **annot_styles)
    ax.annotate("Increasing Defense Difficulty", xy=(-0.03, -0.085), **annot_styles)

    team_colors = pd.read_csv(
        "https://raw.githubusercontent.com/guga31bb/nflfastR-data/master/teams_colors_logos.csv"
    )

    # annotate the points with team logos
    for idx, row in schedule_epa.iterrows():
        offense_epa = row["Offense_EPA_Delta"]
        defense_epa = row["Defense_EPA_Delta"]
        logo_src = team_colors[team_colors["team_abbr"] == idx][
            "team_logo_espn"
        ].values[0]
        res = requests.get(logo_src)
        img = plt.imread(BytesIO(res.content))
        ax.imshow(
            img,
            extent=[
                row["Offense_EPA_Delta"] - 0.0085,
                row["Offense_EPA_Delta"] + 0.0085,
                row["Defense_EPA_Delta"] - 0.00725,
                row["Defense_EPA_Delta"] + 0.00725,
            ],
            aspect="equal",
            zorder=1000,
        )

    ax.set_title("Offense EPA and Defense EPA", fontsize=20)
    plt.savefig(find_in_data_folder("EPA/schedule_remaining.png"))


def defense_plot(epa_df, name):
    plt.style.use("ggplot")

    x = epa_df["defense_rush_epa/play"].values
    y = epa_df["defense_pass_epa/play"].values

    fig, ax = plt.subplots(figsize=(15, 15))

    ax.grid(alpha=0.5)
    # plot a vertical and horixontal line to create separate quadrants
    ax.vlines(0, -0.2, 0.2, color="#fcc331", alpha=0.7, lw=4, linestyles="dashed")
    ax.hlines(0, -0.2, 0.2, color="#fcc331", alpha=0.7, lw=4, linestyles="dashed")
    ax.set_ylim(-0.25, 0.25)
    ax.set_xlim(-0.25, 0.25)
    ax.set_xlabel("defense_rush_epa/play", fontsize=20)
    ax.set_ylabel("defense_pass_epa/play", fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    annot_styles = {
        "bbox": {
            "boxstyle": "round,pad=0.5",
            "facecolor": "none",
            "edgecolor": "#fcc331",
        },
        "fontsize": 20,
        "color": "#202f52",
    }

    # annotate the axis
    ax.annotate("Worse Passing Defense", xy=(0.09, 0.015), **annot_styles)
    ax.annotate("Better Passing Defense", xy=(-0.24, -0.015), **annot_styles)
    ax.annotate("Worse Rushing Defense", xy=(-0.07, 0.23), **annot_styles)
    ax.annotate("Better Rushing Defense", xy=(-0.07, -0.23), **annot_styles)

    team_colors = pd.read_csv(
        "https://raw.githubusercontent.com/guga31bb/nflfastR-data/master/teams_colors_logos.csv"
    )

    # annotate the points with team logos
    for idx, row in epa_df.iterrows():
        offense_epa = row["defense_rush_epa/play"]
        defense_epa = row["defense_pass_epa/play"]
        logo_src = team_colors[team_colors["team_abbr"] == idx][
            "team_logo_espn"
        ].values[0]
        res = requests.get(logo_src)
        img = plt.imread(BytesIO(res.content))
        ax.imshow(
            img,
            extent=[
                row["defense_rush_epa/play"] - 0.01,
                row["defense_rush_epa/play"] + 0.01,
                row["defense_pass_epa/play"] - 0.009,
                row["defense_pass_epa/play"] + 0.009,
            ],
            aspect="equal",
            zorder=1000,
        )

    ax.set_title("Defense Rushing and Passing EPA", fontsize=20)
    plt.savefig(find_in_data_folder(name))


def offense_plot(epa_df, name, columns=["offense_rush_epa/play", "offense_pass_epa/play"], annotations=["Better Rushing Offense", "Worse Rushing Offense", "Better Passing Offense", "Worse Passing Offense"]):
    plt.style.use("ggplot")

    #.3
    x = epa_df[columns[0]].values
    y = epa_df[columns[1]].values
    maximum = max(max(x), max(y))
    maximum += maximum/15

    fig, ax = plt.subplots(figsize=(15, 15))

    ax.grid(alpha=0.5)
    # plot a vertical and horixontal line to create separate quadrants
    ax.vlines(0, -maximum, maximum, color="#fcc331", alpha=0.7, lw=4, linestyles="dashed")
    ax.hlines(0, -maximum, maximum, color="#fcc331", alpha=0.7, lw=4, linestyles="dashed")
    ax.set_ylim(-maximum, maximum)
    ax.set_xlim(-maximum, maximum)
    ax.set_xlabel(columns[0], fontsize=20)
    ax.set_ylabel(columns[1], fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    annot_styles = {
        "bbox": {
            "boxstyle": "round,pad=0.5",
            "facecolor": "none",
            "edgecolor": "#fcc331",
        },
        "fontsize": 20,
        "color": "#202f52",
    }

    # annotate the axis
    ax.annotate(annotations[0], xy=(maximum/1.6, maximum/20), **annot_styles)
    ax.annotate(annotations[1], xy=(-maximum/1.04, -maximum/20), **annot_styles)
    ax.annotate(annotations[2], xy=(-maximum/4.2, (maximum-maximum/15)), **annot_styles)
    ax.annotate(annotations[3], xy=(-maximum/4.2, -(maximum-maximum/15)), **annot_styles)

    team_colors = pd.read_csv(
        "https://raw.githubusercontent.com/guga31bb/nflfastR-data/master/teams_colors_logos.csv"
    )

    # annotate the points with team logos
    for idx, row in epa_df.iterrows():
        offense_epa = row[columns[0]]
        defense_epa = row[columns[1]]
        logo_src = team_colors[team_colors["team_abbr"] == idx][
            "team_logo_espn"
        ].values[0]
        res = requests.get(logo_src)
        img = plt.imread(BytesIO(res.content))
        ax.imshow(
            img,
            extent=[
                row[columns[0]] - maximum/15, #.02
                row[columns[0]] + maximum/15,
                row[columns[1]] - maximum/16, #.019
                row[columns[1]] + maximum/16,
            ],
            aspect="equal",
            zorder=1000,
        )

    ax.set_title("Offense Rushing and Passing EPA", fontsize=20)
    plt.savefig(find_in_data_folder(name))


def make_all(years):
    main()
    epa_df = epa.get_rush_pass_epa(years)
    name = "EPA/epa_defense.png"
    defense_plot(epa_df, name)
    name = "EPA/epa_offense.png"
    offense_plot(epa_df, name)
    epa_df = epa.schedule_adjusted_epa(years)
    name = "EPA/sched_adj_epa_defense.png"
    defense_plot(epa_df, name)
    name = "EPA/sched_adj_epa_offense.png"
    offense_plot(epa_df, name)


if __name__ == "__main__":
    make_all(years=[2022])
