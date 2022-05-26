import pandas as pd
import requests
import wget
import zipfile
import os
import re
from os.path import join


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


def update_chrome_driver() -> None:
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