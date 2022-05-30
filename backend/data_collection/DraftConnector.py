import pandas as pd
from BuildData.BootstrapAnalysis import get_bootstrap, get_cf
from BuildData import build_players, calculate_VOR
from CollectData import ADPCollector, ECRCollector, FPTSDataCollector, InjuryDataCollector
from utils import merge_list

class DraftConnector():
    self __init__(self, year: int):
        self.year = year
        self.adp = ADPCollector(ws=WebScraper(), url="https://www.fantasypros.com/nfl/adp/ppr-overall.php", _id='id', tag='data')
        self.ecr = ECRCollector(ws=DynamicWebScraper(), url="https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php", _id='id', tag='ranking-table')
        self.idc = InjuryDataCollector(url="https://www.draftsharks.com/injury-predictor/{position}")
        self.fdc = FPTSDataCollector(
            aggr_sites={
                'https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring=PPR&week=draft': ['data', 'id'], 
                'https://www.cbssports.com/fantasy/football/stats/{position}/'+str(year)+'/restofseason/projections/ppr/': ['TableBase-table',  'class'],
                'https://eatdrinkandsleepfootball.com/fantasy/projections/{position}/': ['projections',  'class']
            }
        )

    def collect(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        #Gets all data
        df = self.adp.collect()
        ecr_df = self.ecr.collect()
        injury_df = self.idc.collect_data()
        fpts_df = self.fdc.collect_data()
        return df, ecr, injury_df, fpts_df

    def run(self) -> None:
        start_time = time.time()
        total_time = time.time()
        df, ecr_df, injury_df, fpts_df = self.collect()
        print("Collected Data--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

        df = self.adp.clean_data(df)
        ecr_df = self.ecr.clean_data(ecr_df)
        fpts_df = self.fdc.clean_data(fpts_df)
        injury_df = self.idc.clean_data(injury_df)
        print("Clean Data--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

        #Get a list of dictionaries with the player, mean, ceiling, floor, and standard deviation
        data = get_bootstrap(fpts_df)
        print("Bootstrap--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

        #Merge the list into a single pandas dataframe
        cf_df = get_cf(data)
        pos_df = fpts_df[["PLAYER", "POS"]]
        cf_df = pos_df.merge(cf_df, on="PLAYER")
        print("CF--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

        #Get the replacemnet players and values for each position
        replacement_players, replacement_values = build_players(cf_df)
        print("BuildPlayers--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

        #Calculate the ADP, VOR, and SleeperScore
        df = calculate_VOR(cf_df, df, replacement_values)
        print("VOR--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()
        
        #Adds ECR from Fantasy Pros to data
        df = df.merge(ecr_df, on='PLAYER', how='outer')
        print("ECR--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

        df = df.merge(injury_df, on='PLAYER', how='outer')
        print("Injury--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

        # self.load(df)
        print("Total--- %s seconds ---" % (time.time() - total_time))

    def load(self, df:pd.DataFrame) -> None:
        df.to_csv(r'data/draft_order_'+str(self.year)+'.csv', index = False, header=True)