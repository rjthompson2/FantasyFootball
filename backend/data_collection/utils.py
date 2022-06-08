import pandas as pd
import requests
import wget
import zipfile
import os
import re
from datetime import date
from os.path import join
from enum import Enum


#TODO changes to an Enum?
team_name_changes = {
    'Miami': 'Miami Dolphins', 
    'Dallas': 'Dallas Cowboys', 
    'Philadelphia': 'Philadelphia Eagles', 
    'Tampa Bay': 'Tampa Bay Buccaneers', 
    'Green Bay': 'Green Bay Packers', 
    'Kansas City': 'Kansas City Chiefs', 
    'Las Vegas': 'Las Vegas Raiders', 
    'L.A. Rams': 'Los Angeles Rams', 
    'Houston': 'Houston Texans', 
    'Denver': 'Denver Broncos', 
    'Detroit': 'Detroit Lions', 
    'N.Y. Jets': 'New York Jets', 
    'New Orleans': 'New Orleans Saints', 
    'San Francisco': 'San Francisco 49ers', 
    'Tennessee': 'Tennessee Titans', 
    'Buffalo': 'Buffalo Bills', 
    'Atlanta': 'Atlanta Falcons', 
    'Minnesota': 'Minnesota Vikings', 
    'Indianapolis': 'Indianapolis Colts', 
    'Seattle': 'Seattle Seahawks', 
    'Cincinnati': 'Cincinnati Bengals', 
    'Chicago': 'Chicago Bears', 
    'Arizona': 'Arizona Cardinals', 
    'Baltimore': 'Baltimore Ravens', 
    'Jacksonville': 'Jacksonville Jaguars', 
    'Washington': 'Washington Commanders', 
    'Pittsburgh': 'Pittsburgh Steelers', 
    'Cleveland': 'Cleveland Browns', 
    'L.A. Chargers': 'Los Angeles Chargers', 
    'N.Y. Giants': 'New York Giants', 
    'Carolina': 'Carolina Panthers', 
    'New England': 'New England Patriots'
}


def get_season_year() -> int:
    '''Gets the current year of the season'''
    today = date.today()
    year = today.year
    if(today.month == 1):
        year -= 1
    return year

def clean_name(df:pd.DataFrame) -> pd.DataFrame:
    df["PLAYER"] = df["PLAYER"].apply(lambda x: re.sub("\s[IVX]*$", "", x))
    df["PLAYER"] = df["PLAYER"].apply(lambda x: re.sub("\s[JS]r\.?$", "", x))
    df['PLAYER'] = df['PLAYER'].apply(lambda x: re.sub("\.", "", x))
    return df


def merge_list(df_list:list, how='left', on=['PLAYER', 'POS']) -> pd.DataFrame:
    df = pd.DataFrame(clean_name(df_list.pop(0)))
    for new_df in df_list:
        df = df.merge(clean_name(new_df), how=how, on=on) 
    return df

def list_to_dict(_list:list) -> dict:
    _dict = {}
    for list_value in _list:
        if isinstance(list_value, dict):
            _dict.update(list_value)
    return _dict


def update_chrome_driver() -> None:
    '''Updates the chrome driver to ensure there are no issues with outdated versions'''
    # get the latest chrome driver version number
    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    response = requests.get(url)
    version_number = response.text

    # build the donwload url
    download_url = "https://chromedriver.storage.googleapis.com/" + version_number +"/chromedriver_mac64_m1.zip"

    # download the zip file using the url built above
    latest_driver_zip = wget.download(download_url,'chromedriver.zip')

    # extract the zip file
    with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd()) # you can specify the destination folder path here
    # delete the zip file downloaded above
    os.remove(latest_driver_zip)

    os.chmod(join(os.getcwd(), 'chromedriver'), 0o755)

def change_team_name(df_series:pd.Series) -> pd.Series:
    '''Changes the team name so all data has the same values for teams'''
    return df_series.apply(lambda x: team_name_changes[x] if x in team_name_changes else x)

class Positions(Enum):
    RB = 'rb'
    QB = 'qb'
    TE = 'te'
    WR = 'wr'
    K = 'k'
    DST = 'dst'

    def __repr__(self):
        return self.value

    @classmethod
    def has_value(cls, value: str):
        return value in cls._value2member_map_ 