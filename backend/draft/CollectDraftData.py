from WebScraper import Scraper
from itertools import repeat
from datetime import date
import pandas as pd
import BuildData as bd
import ml.Bootstrap as bs
import time
import multiprocessing
import re

def get_draft_data(year:int) -> None:
    start_time = time.time()
    total_time = time.time()
    
    #Gets all data
    dfs = collect_data()
    df =  dfs[0]
    injury_df = dfs[1]
    fpts_df = dfs[2]
    ecr_df = dfs[3]
    print("Sites--- %s seconds ---" % (time.time() - start_time))
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
    replacement_players, replacement_values = bd.build_players(cf_df)
    print("BuildPlayers--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    #Calculate the ADP, VOR, and SleeperScore
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    df = bd.calculate_VOR(cf_df, df, replacement_values)
    print("VOR--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    
    #Adds ECR from Fantasy Pros to data
    df = df.merge(ecr_df, on='PLAYER', how='outer')
    print("ECR--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    df = df.merge(injury_df, on='PLAYER', how='outer')
    print("Injury--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    df.to_csv(r'data/draft_order_'+str(year)+'.csv', index = False, header=True)

    print("Total--- %s seconds ---" % (time.time() - total_time))

def merge(df_list:list) -> pd.DataFrame:
    df = pd.DataFrame()

    for i in range(len(df_list)):
        df_list[i] = clean_name(df_list[i])
        if i == 0:
            df = df_list[i]
        else:
            df = df.merge(df_list[i], how='left', on=['PLAYER', 'POS'])
    return df

def clean_name(df:pd.DataFrame) -> pd.DataFrame:
    df["PLAYER"] = df["PLAYER"].apply(lambda x: re.sub("\s[IVX]*$", "", x))
    df["PLAYER"] = df["PLAYER"].apply(lambda x: re.sub("\s[JS]r\.?$", "", x))
    df['PLAYER'] = df['PLAYER'].apply(lambda x: re.sub("\.", "", x))
    return df

def get_bootstrap(fpts_df:pd.DataFrame):
    data = []
    players = fpts_df["PLAYER"].values
    with multiprocessing.Pool() as pool:
        data = pool.starmap(mp_bootstrap, zip(players, repeat(fpts_df)))
        pool.close()
        pool.join()
        pool.terminate()
    return data

def mp_bootstrap(player:str, fpts_df:pd.DataFrame):
    new_df = fpts_df.loc[fpts_df["PLAYER"] == player]
    new_df = new_df.drop(columns=["PLAYER", "POS"])
    new_df = new_df.dropna(axis=1, how='all').dropna()
    if(len(new_df.columns) > 1):
        new_list = new_df.values
        output = bs.calculate_ceiling_floor(arrays=new_list, player_names=[player], stdout=False)
        return output
    return None

def get_cf(data:list) -> pd.DataFrame:
    temp_df = []
    cf_df = pd.DataFrame()
    for dictionary in data:
        if dictionary != None:
            values = [dictionary["player"], dictionary["mean"], dictionary["ceiling"], dictionary["floor"], dictionary["std"]]
            temp_df.append(pd.DataFrame([values], columns=["PLAYER", "FPTS", "C", "F", "STD"]))
    cf_df = pd.concat(temp_df)
    return cf_df

def collect_data() -> list:
    aggr_sites = {
        'https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring=PPR&week=draft': ['data', 'id'], 
        'https://www.cbssports.com/fantasy/football/stats/{position}/'+str(year)+'/restofseason/projections/ppr/': ['TableBase-table',  'class'],
        'https://eatdrinkandsleepfootball.com/fantasy/projections/{position}/': ['projections',  'class']
    }
    reg_sites = [
        'https://fantasydata.com/nfl/fantasy-football-weekly-projections?season='+str(year)+'&seasontype=1&scope=1&scoringsystem=2&startweek=1&endweek=17'
    ]
    unique_sites = [
        'https://www.footballdiehards.com/fantasy-football-player-projections.cfm',
        'https://fantasy.espn.com/football/players/projections'
    ]
    position = ['qb', 'rb', 'wr', 'te']

    #Aggregate all data from the sites
    callback_list = []
    with multiprocessing.Pool() as pool:
        injury_df_list = pool.starmap_async(get_injury_data, zip(position), callback=lambda x: callback_list.append(x))
        df_list = pool.starmap_async(get_site_data, zip(repeat(aggr_sites), aggr_sites), callback=lambda x: callback_list.append(x))
        ecr_df = pool.apply_async(get_ecr_data)
        df = pool.apply_async(get_adp_data)
        df = df.get()
        ecr_df = ecr_df.get()
        injury_df_list = injury_df_list.get()
        df_list = df_list.get()
        pool.close()
        pool.join()
        pool.terminate()
        
    #Merge the list into a single pandas dataframe
    fpts_df = merge(df_list)
    injury_df = pd.concat(injury_df_list, ignore_index=True)

    return [df, injury_df, fpts_df, ecr_df]

def get_site_data(aggr_sites, site):
    return bd.prediction(site, aggr_sites[site][0], aggr_sites[site][1])

def get_adp_data() -> pd.DataFrame:
    ws = WebScraper()
    ws.start("https://www.fantasypros.com/nfl/adp/ppr-overall.php")
    df = bd.adp_output(ws.collect('id', 'data'))
    return df

def get_injury_data(position:str) -> pd.DataFrame:
    dws = DynamicWebScraper()
    dws.start("https://www.draftsharks.com/injury-predictor/"+position, headless=True)
    injury_df = dws.collect('class', 'sip-table')
    injury_df = injury_df.rename(columns={'Player':'PLAYER', 'Career Injuries':'CI', 'Probability of Injury In the Season':'IJ%', 'Projected Games Missed':'PGM', 'Probability of Injury Per Game':'IPG%', 'Durability':'D'})
    injury_df["PLAYER"] = injury_df["PLAYER"].apply(lambda x: x.split(",")[0])
    injury_df = clean_name(injury_df)
    injury_df.drop('Proj. Points', axis=1, inplace=True)
    return injury_df

def get_ecr_data() -> pd.DataFrame:
    dws = DynamicWebScraper()
    dws.start("https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php", headless=True)
    ecr_df = dws.collect('id', 'ranking-table')
    ecr_df[['PLAYER', 'ECR']] = ecr_df[['Player Name', 'AVG.']]
    ecr_df = ecr_df[['PLAYER', 'ECR']]
    ecr_df = ecr_df.dropna()
    ecr_df['PLAYER'] = ecr_df['PLAYER'].apply(lambda x: re.sub('\s\(.*', '', x))
    ecr_df = clean_name(ecr_df)
    return ecr_df


if __name__ == '__main__':
    today = date.today()
    year = today.year
    if(today.month == 1):
        year -= 1
    get_draft_data(year)