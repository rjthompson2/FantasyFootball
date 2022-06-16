from backend.data_collection.BuildData import build_players, calculate_VOR, fix_ecr
from backend.data_collection.Collectors import Collector, FPTSDataCollector, InjuryDataCollector
from backend.data_collection.WebScraper import WebScraper, DynamicWebScraper
from backend.data_collection.utils import merge_list
from backend.data_collection.Cleaners import ADPCleaner, ECRCleaner, FPTSCleaner, InjuryCleaner
from backend.data_collection.Bootstrap import get_bootstrap, get_cf
from backend.utils import find_in_data_folder
from typing import Tuple
import time
import pandas as pd
import logging


LOG = logging.getLogger(__name__)

class DraftConnector():
    def __init__(self, year: int):
        self.year = year
        self.adp = Collector(ws=WebScraper(), url="https://www.fantasypros.com/nfl/adp/ppr-overall.php", _id='id', tag='data')
        self.adp_cleaner = ADPCleaner()
        self.ecr = Collector(ws=DynamicWebScraper(), url="https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php", _id='id', tag='ranking-table')
        self.ecr_cleaner = ECRCleaner()
        self.idc = InjuryDataCollector(url="https://www.draftsharks.com/injury-predictor/{position}")
        self.injury_cleaner = InjuryCleaner()
        self.fdc = FPTSDataCollector(
            aggr_sites={
                'https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring=PPR&week=draft': ['data', 'id'], 
                'https://www.cbssports.com/fantasy/football/stats/{position}/'str(year)+'/restofseason/projections/ppr/': ['TableBase-table',  'class'],
                # 'https://eatdrinkandsleepfootball.com/fantasy/projections/{position}/': ['projections',  'class'], #TODO website deprecated need to grab new data/deprecate
            }
        )
        self.fpts_cleaner = FPTSCleaner()

    def collect_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        adp_df = self.adp.collect_data()
        ecr_df = self.ecr.collect_data()
        injury_df = self.idc.collect_data()
        fpts_df = self.fdc.collect_data()
        return adp_df, ecr_df, injury_df, fpts_df

    def run(self) -> None:
        adp_df, ecr_df, injury_df, fpts_df = self.collect_data()

        #Gets all data
        adp_df = self.adp_cleaner.clean_data(adp_df)
        ecr_df = self.ecr_cleaner.clean_data(ecr_df)
        fpts_df = self.fpts_cleaner.clean_data(fpts_df)
        injury_df = self.injury_cleaner.clean_data(injury_df)

        #Get a list of dictionaries with the player, mean, ceiling, floor, and standard deviation
        data = get_bootstrap(fpts_df)

        #Merge the list into a single pandas dataframe
        cf_df = get_cf(data)
        pos_df = fpts_df[["PLAYER", "POS"]]
        cf_df = pos_df.drop_duplicates(subset=['PLAYER']).merge(cf_df, on="PLAYER", copy=False) # Ensures no duplicate players

        #Get the replacemnet players and values for each position
        replacement_players, replacement_values = build_players(cf_df)

        #Calculate the ADP, VOR, and SleeperScore
        df = calculate_VOR(cf_df, adp_df, replacement_values)
        
        #Adds ECR from Fantasy Pros to data
        ecr_df = fix_ecr(ecr_df, df)
        df = df.merge(ecr_df, on='PLAYER', how='outer')

        df = df.merge(injury_df, on='PLAYER', how='outer')

        self.load(df)

    def load(self, df:pd.DataFrame) -> None:
        file_path = find_in_data_folder(f'draft_order_{self.year}.csv')
        df = df.dropna(how='all')
        df = df.dropna(subset=["POS"])
        df.to_csv(file_path, index = False, header=True)