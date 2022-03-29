import CollectPlayerData as cpd
from WebScraper import *
from os.path import exists
from datetime import date

today = date.today()
year = today.year
if(today.month == 1):
    year -= 1

URL="https://www.prosportstransactions.com/football/Search/SearchResults.php?Player=&Team=&BeginDate=1900-01-01&EndDate=2022-03-11&ILChkBx=yes&submit=Search&start=0"

#TODO WIP
def gather_injury_data():
    ws = InjuryScraper()
    ws.start(url=URL, headless=True)
    if exists("data/injury_data.csv"):
        old_df = pd.read_csv("data/injury_data.csv")
        df = None
        i = (len(old_df)//25)
        print(i)
        try:
            ws.find(i)
        except:
            df = old_df
        if df == None:
            df_list = ws.collect_all()
            df = pd.concat(df_list)
            df = old_df.append(df)
    else:
        df_list = ws.collect_all()
        df = pd.concat(df_list)
    df = df.drop_duplicates()
    df.to_csv(r'data/injury_data.csv', index = False, header=True)
    # #TODO split into Offense and DST+K
    
    # #TODO suggest what player to trade for and who to trade to get the player
    # if (not exists("data/wr-te_wopr_"+str(date.today())+".csv")):
    #     cpd.get_player_data()
    # wopr_df.read_csv('data/wr-te_wopr_'+str(date.today())+'.csv')
    # rb_adv_df.read_csv('data/rb_share_'+str(date.today())+'.csv')

def clean_injury_data():
    injury_df = pd.read_csv("data/injury_data.csv")
    pd.set_option('display.max_columns', None)
    # print(injury_df.head())
    df = pd.DataFrame()
    df = injury_df["Acquired"]
    print(df.head())
    # df['Name'] = injury_df.loc[["Acquired", "Relinquished"] != None]

if __name__ == '__main__':
    # gather_injury_data()
    clean_injury_data()