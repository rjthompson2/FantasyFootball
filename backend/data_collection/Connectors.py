from backend.data_collection.BuildData import build_players, calculate_VOR
from backend.data_collection.Collectors import Collector, FPTSDataCollector, InjuryDataCollector, APICollector
from backend.data_collection.WebScraper import WebScraper, DynamicWebScraper
from backend.data_collection.utils import merge_list
from backend.data_collection.Cleaners import ADPCleaner, ECRCleaner, FPTSCleaner, InjuryCleaner, ESPNCleaner
from backend.data_collection.Bootstrap import get_bootstrap, get_cf
from backend.data_analysis.accuracy import *
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
        self.ecr = Collector(ws=DynamicWebScraper(), url="https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php", _id='id', tag='ranking-table') #TODO have a version that collects it with a WebScraper
        self.ecr_cleaner = ECRCleaner()
        self.idc = InjuryDataCollector(url="https://www.draftsharks.com/injury-predictor/{position}")
        self.injury_cleaner = InjuryCleaner()
        self.fdc = FPTSDataCollector(
            aggr_sites={
                'https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring=PPR&week=draft': ['data', 'id'], 
                'https://www.cbssports.com/fantasy/football/stats/{position}/'+str(year)+'/restofseason/projections/ppr/': ['TableBase-table',  'class'],
                # 'https://eatdrinkandsleepfootball.com/fantasy/projections/{position}/': ['projections',  'class'], #TODO website deprecated need to grab new data/deprecate
            }
        )
        self.fpts_cleaner = FPTSCleaner()

        headers = {
            "Host": "fantasy.espn.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Fantasy-Source": "kona",
            "X-Fantasy-Filter": '{"players":{"filterStatsForExternalIds":{"value":['+str(year-1)+','+str(year)+']},"filterSlotIds":{"value":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,23,24]},"filterStatsForSourceIds":{"value":[0,1]},"useFullProjectionTable":{"value":true},"sortAppliedStatTotal":{"sortAsc":false,"sortPriority":3,"value":"102022"},"sortDraftRanks":{"sortPriority":2,"sortAsc":true,"value":"PPR"},"sortPercOwned":{"sortPriority":4,"sortAsc":false},"limit":1000,"filterRanksForSlotIds":{"value":[0,2,4,6,17,16]},"filterStatsForTopScoringPeriodIds":{"value":2,"additionalValue":["002022","102022","002021","022022"]}}}',
            "X-Fantasy-Platform": "kona-PROD-6daa0c838b3e2ff0192c0d7d1d24be52e5811609",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://fantasy.espn.com/football/players/projections",
            "Cookie": "region=ccpa; _dcf=1; SWID=fd942b9e-091c-4601-94fe-d4adb5d81803; UNID=7fc05b27-5071-4006-9a34-e03d4b7561ce; UNID=7fc05b27-5071-4006-9a34-e03d4b7561ce",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "If-None-Match": 'W/"0e4940690e8c2869b89702c401e93ff75"',
        }

        self.espn = APICollector(url='https://fantasy.espn.com/apis/v3/games/ffl/seasons/2022/segments/0/leaguedefaults/3?view=kona_player_info', params=headers)
        self.espn_cleaner = ESPNCleaner()


    def collect_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        adp_df = self.adp.collect_data()
        ecr_df = self.ecr.collect_data()
        injury_df = self.idc.collect_data()
        fpts_df = self.fdc.collect_data()
        espn_data = self.espn.collect_data()
        return adp_df, ecr_df, injury_df, fpts_df, espn_data

    def run(self) -> None:
        #Gets all data
        adp_df, ecr_df, injury_df, fpts_df, espn_data = self.collect_data()

        #Cleans all data
        adp_df = self.adp_cleaner.clean_data(adp_df)
        ecr_df = self.ecr_cleaner.clean_data(ecr_df)
        fpts_df = self.fpts_cleaner.clean_data(fpts_df)
        injury_df = self.injury_cleaner.clean_data(injury_df)
        espn_df = self.espn_cleaner.clean_data(espn_data)

        #Merges fantasy point prediction data into singular df
        fpts_df = fpts_df.append(espn_df)

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
        df = df.merge(ecr_df, on='PLAYER', how='outer')

        #Adds injury data to the final dataframe
        df = df.merge(injury_df, on='PLAYER', how='outer')

        self.load(df)

    def load(self, df:pd.DataFrame) -> None:
        file_path = find_in_data_folder(f'draft_order_{self.year}.csv')
        df = df.dropna(how='all')
        df = df.dropna(subset=["POS"])
        df.to_csv(file_path, index = False, header=True)

class AccuracyConnector():
    def __init__(self, year: int):
        self.year = year

    def collect_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        prediction = pd.read_csv(find_in_data_folder(f'draft_order_{self.year-1}.csv'))
        actual = None
        return prediction, actual

    def run(self) -> None:
        #Gets all data
        prediction, actual = self.collect_data()

        #Calculates average error in predicted points # % and std
        accuracy.error_calculator(prediction, actual, on="FPTS")

        #TODO need some metric for ranking ECR, ADP, and VOR based on how close they were to actual best draft order

        self.load(df)

    def load(self, df:pd.DataFrame) -> None:
        file_path = find_in_data_folder(f'accuracy_{self.year}.csv')
        df = df.dropna(how='all')
        df = df.dropna(subset=["POS"])
        df.to_csv(file_path, index = False, header=True)