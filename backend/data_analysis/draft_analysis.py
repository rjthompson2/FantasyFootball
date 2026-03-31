# The idea is that players drafted are like mystery boxes or assets. 
# I need to get the normal distribution of round picks

import matplotlib.pyplot as plt
import nfl_data_py as nfl
import pandas as pd
import numpy as np
from backend.data_collection.Collectors import (
    Collector,
)
from backend.data_collection.WebScraper import WebScraper
from backend.data_collection.Cleaners import ADPCleaner, PPRCleaner
from backend.data_collection.BuildData import build_players, calculate_VOR

def get_player_rankings(years):
    df_list = []
    for year in years:
        adp = Collector(
            ws=WebScraper(),
            url="https://www.fantasypros.com/nfl/adp/ppr-overall.php",
            _id="id",
            tag="data",
        )
        adp_cleaner = ADPCleaner()

        adp_df = adp.collect_data()
        adp_df = adp_cleaner.clean_data(adp_df)
        df_list.append(adp_df)
    return df_list

def get_player_points(years):
    df_list = []
    for year in years:
        ppr_df = nfl.import_seasonal_data([year], "ALL")
        ppr_df = ppr_df[["player_id", "fantasy_points_ppr", "games"]]
        names_df = nfl.import_depth_charts(years)
        names_df = names_df[["full_name", "gsis_id"]]
        names_df = names_df.rename(columns={
            "full_name": "PLAYER",
            "gsis_id": "player_id"
        })
        df = names_df.merge(ppr_df, how="outer", on="player_id")
        df = df.drop_duplicates()
        df = df.dropna()
        df = df.rename(columns={
            "fantasy_points_ppr": "PPR",
            "games": "G",
            'position': "POS"
        })
        df["AVG_PPR"] = round(df["PPR"]/df["G"], 2)
        df = df[["PLAYER", "PPR", "AVG_PPR"]]
        df_list.append(df)
    return df_list




def merge(ranking_list, points_list):
    df_list = []
    for i, ranking_df in enumerate(ranking_list):
        points_df = points_list[i]
        points_df = points_df[["PLAYER", "PPR", "AVG_PPR"]]
        df = ranking_df.merge(points_df, how='outer', on="PLAYER")
        df = df.dropna()
        df = df[~df["POS"].isin(["DT", "LB", "K"])]


        replacement_players, replacement_values = build_players(df)
        vor = calculate_VOR(df, ranking_df, replacement_values, on="PPR")
        vor = vor[["PLAYER", "POS", "AVG_x", "PPR", "AVG_PPR", "VOR", "VALUERANK", "ADPRANK", "SLEEPERSCORE"]]
        vor = vor.rename(columns = {
            "AVG_x": "ADP"
        })
        df_list.append(vor)
    return df_list


def generate_histograms(df_list, values=["vor", "avg", "total", "round", "pos", "posround"], show=True):
    for df in df_list:
        df["ROUND"] = df["ADP"]//12 + 1
    df = pd.concat(df_list)
    df = df[df["ROUND"] <= 20]


    if "vor" in values and "pos" in values:
        df.boxplot(column='VOR', by='POS', figsize=(8, 6))
        plt.title('VOR by Position')
        plt.suptitle('') 
        plt.savefig('backend/data/BoxPlot/vor_pos.png')
        if show:
            plt.show()

    if "avg" in values and "pos" in values:
        df.boxplot(column='AVG_PPR', by='POS', figsize=(8, 6))
        plt.title('Points by Position')
        plt.suptitle('') 
        plt.savefig('backend/data/BoxPlot/ppr_pos.png')
        if show:
            plt.show()
        
    if "total" in values and "pos" in values:
        df.boxplot(column='PPR', by='POS', figsize=(8, 6))
        plt.title('Points by Position')
        plt.suptitle('') 
        plt.savefig('backend/data/BoxPlot/tot_pos.png')
        if show:
            plt.show()

    if "vor" in values and "round" in values:
        df.boxplot(column='VOR', by='ROUND', figsize=(8, 6))
        plt.title('VOR by Round')
        plt.suptitle('') 
        plt.savefig('backend/data/BoxPlot/vor_round.png')
        if show:
            plt.show()

    if "avg" in values and "round" in values:
        df.boxplot(column='AVG_PPR', by='ROUND', figsize=(8, 6))
        plt.title('Points by Round')
        plt.savefig('backend/data/BoxPlot/ppr_round.png')
        plt.suptitle('') 
        if show:
            plt.show()

    if "total" in values and "round" in values:
        df.boxplot(column='PPR', by='ROUND', figsize=(8, 6))
        plt.title('Points by Round')
        plt.savefig('backend/data/BoxPlot/tot_round.png')
        plt.suptitle('') 
        if show:
            plt.show()

    if "vor" in values and "posround" in values:
        for pos in df["POS"].unique():
            temp_df = df[df["POS"] == pos]
            temp_df.boxplot(column='VOR', by='ROUND', figsize=(8, 6))
            plt.title(f'VOR by Position {pos} and Round')
            plt.suptitle('') 
            plt.savefig(f'backend/data/BoxPlot/vor_{pos}.png')
            if show:
                plt.show()

    if "avg" in values and "posround" in values:
        for pos in df["POS"].unique():
            temp_df = df[df["POS"] == pos]
            temp_df.boxplot(column='AVG_PPR', by='ROUND', figsize=(8, 6))
            plt.title(f'Points by Position {pos} and Round')
            plt.savefig(f'backend/data/BoxPlot/ppr_{pos}.png')
            plt.suptitle('') 
            if show:
                plt.show()


    if "total" in values and "posround" in values:
        for pos in df["POS"].unique():
            temp_df = df[df["POS"] == pos]
            temp_df.boxplot(column='PPR', by='ROUND', figsize=(8, 6))
            plt.title(f'Points by Position {pos} and Round')
            plt.savefig(f'backend/data/BoxPlot/tot_{pos}.png')
            plt.suptitle('') 
            if show:
                plt.show()

def distribution_visualization(df):
    # 3 criteria
    # 1. Average round

    round_df = df.groupby(df.index // 12).mean()

    # plt.plot(round_df["AVG_PPR"])

    # plt.show()

    # 2. Average position
    position_df = df.groupby(df["POS"]).mean()

    # plt.plot(position_df["AVG_PPR"])

    # plt.show()

    # 3. Average position/round
    round_position_df = df.sort_values(by='POS').reset_index(drop=True)
    round_position_df = round_position_df.groupby(['POS', df.index // 12])['AVG_PPR'].mean().reset_index()
    round_position_df = round_position_df.sort_values(by='AVG_PPR')

    plt.plot(round_position_df["POS"], round_position_df["AVG_PPR"])

    plt.show()


def generate_years(year, backwards=0):
    years = [year]
    backwards-=1
    while backwards > 0:
        year-=1
        backwards-=1
        years.append(year)
    return years



years = generate_years(2024, 5)
adp_list = get_player_rankings(years)
ppr_list = get_player_points(years)
df = merge(adp_list, ppr_list)
generate_histograms(df, show=False) 
# distribution_visualization(df)