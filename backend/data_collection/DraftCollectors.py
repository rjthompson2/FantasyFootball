from WebScraper import WebScraper, DynamicWebScraper
from utils import clean_name, merge_list, update_chrome_driver, change_team_name, Positions
from selenium.common.exceptions import WebDriverException
from itertools import repeat
import pandas as pd
import multiprocessing
import re


class Collector():
    def __init__(self, ws, url, _id, tag):
        self.ws = ws
        self.url = url
        self.id = _id
        self.tag = tag

    def collect(self):
        self.ws.start(self.url, headless=True)
        df = ws.collect(self.id, self.tag)
        return df

    def clean_data(self, df):
        raise NotImplementedError

class ADPCollector(Collector):
    def clean_data(self, df):
        df = df[['Player Team (Bye)', 'POS', 'AVG']]
        df['PLAYER'] = df['Player Team (Bye)'].apply(lambda x: ' '.join(x.split()[:-2]) if x.split()[-1] != 'DST' else ' '.join(x.split()[:-1])) #removing the team and position
        df['POS'] = df['POS'].apply(lambda x: x[:1] if x[0] == "K" else ( x[:3] if x[:3] == "DST" else x[:2])) #removing the position rank
        df = df[['PLAYER', 'POS', 'AVG']].sort_values(by='AVG')
        return df

class ECRCollector(Collector):
    def clean_data(self, df):
        df[['PLAYER', 'ECR']] = df[['Player Name', 'AVG.']]
        df = df[['PLAYER', 'ECR']]
        df = df.dropna()
        df['PLAYER'] = df['PLAYER'].apply(lambda x: re.sub('\s\(.*', '', x))
        df = clean_name(df)
        return df


class MultiProssCollector():
    def __init__(self):
        self.input = None
        raise NotImplementedError

    def collect_data(self) -> list:
        #Aggregate all data from the sites
        callback_list = []
        try:
            with multiprocessing.Pool() as pool:
                df_list = pool.starmap_async(self.get_site_data, zip(self.input), callback=lambda x: callback_list.append(x))
                df_list = df_list.get()
                pool.close()
                pool.join()
                pool.terminate()
        except WebDriverException:
            update_chrome_driver()
            self.collect_data()

        return df_list
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

'''TODO add sites later
    self.reg_sites = [
        'https://fantasydata.com/nfl/fantasy-football-weekly-projections?season='+str(year)+'&seasontype=1&scope=1&scoringsystem=2&startweek=1&endweek=17'
    ]
    self.unique_sites = [
        'https://www.footballdiehards.com/fantasy-football-player-projections.cfm',
        'https://fantasy.espn.com/football/players/projections'
    ]'''
class FPTSDataCollector(MultiProssCollector):
    def __init__(self, aggr_sites: dict) -> None:
        self.input = aggr_sites
        
    def collect_data(self) -> pd.DataFrame:
        #Aggregate all data from the sites
        df_list = super().collect_data()
            
        #Merge the list into a single pandas dataframe
        df_dict = list_to_dict(df_list)

        return df_dict
    
    def get_site_data(self, site: str) -> dict:
        data =  self.input[site][0]
        _id = self.input[site][1]
        ws = WebScraper()
        df_dict = {data: {position.value: ws.new_collect(site.format(position=position.value.upper(), data, _id)) for position in Positions}}
        return df_dict

    def collect_data(self, df_dict: dict) -> pd.DataFrame:
        df = pd.DataFrame()
        df_list = []
        
        for data in df_dict.keys():
            temp = df_dict[data]
            if data == "TableBase-table":
                df_list.append([fpts_multi_index_output(temp[position.value]) for position in Positions]) #collect data with list comprehensions
            elif data == "projections":
                df_list.append([new_fpts_output(temp[position.value]) for position in Positions if position.value not in ['k', 'dst']])
            else:
                df_list.append([fpts_output(temp[position.value], ['k', 'dst'], 'FPTS') for position in Positions])
        
        df = pd.concat(df_list)
        df = final_df.sort_values(by='FPTS', ascending=False) #sort df in descending order on FPTS column
        return df
        
    def fpts_output(position:str, df:pd.DataFrame, check_array:List[str], ftps:str) -> pd.DataFrame:
        if position not in check_array:
            df.columns = df.columns.droplevel(level=0) #our data has a multi-level column index. The first column level is useless so let's drop it.
        df['PLAYER'] = df['Player'].apply(lambda x: re.sub("\.", "", ' '.join(x.split()[:-1]))) #fixing player name to not include team
        df['PLAYER'] = change_team_name(df['PLAYER'])
        df["FPTS"] = df[ftps]
        df['POS'] = position.upper() #add a position column
        df = df[['PLAYER', 'POS', 'FPTS']]
        return df

    def new_fpts_output(position:str, df:pd.DataFrame) -> pd.DataFrame:
        df['PLAYER'] = change_team_name(df[1]) #fixing player name to not include team
        df["FPTS"] = df[len(df.columns)-2]
        df['POS'] = position.upper() #add a position column
        df = df[['PLAYER', 'POS', 'FPTS']]
        return df

    def fpts_multi_index_output(position:str, df:pd.DataFrame) -> pd.DataFrame:
        df.columns = df.columns.droplevel(level=0)
        if position != 'dst':
            df["PLAYER"] = df['Player'].apply(lambda x: re.sub("\.", "", ' '.join(x.split()[4:6])))
        else:
            #TODO change names to long form
            df["PLAYER"] = change_team_name(df['Team'])
        df["POS"] = position.upper()
        df = df.loc[df['fpts  Fantasy Points'] != '—']
        df["FPTS"] = df['fpts  Fantasy Points'].apply(lambda x: float(x))
        df = df[['PLAYER', 'POS', 'FPTS']]
        df = df.sort_values(by='FPTS', ascending=False)
        return df

class InjuryDataCollector(MultiProssCollector):
    def __init__(self, url: str) -> None:
        self.input = url

    def collect_data(self) -> pd.DataFrame:
        #Aggregate all data from the sites
        df_list = super().collect_data()
            
        #Merge the list into a single pandas dataframe
        df = pd.concat(df_list, ignore_index=True)

        return df
    
    def get_site_data(self, position: str) -> pd.DataFrame:
        ws = DynamicWebScraper()
        ws.start(self.input.format(position=position.value), headless=True)
        df = dws.collect('class', 'sip-table')
        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(columns={'Player':'PLAYER', 'Career Injuries':'CI', 'Probability of Injury In the Season':'IJ%', 'Projected Games Missed':'PGM', 'Probability of Injury Per Game':'IPG%', 'Durability':'D'})
        df["PLAYER"] = df["PLAYER"].apply(lambda x: x.split(",")[0])
        df = clean_name(df)
        df.drop('Proj. Points', axis=1, inplace=True)
        return df