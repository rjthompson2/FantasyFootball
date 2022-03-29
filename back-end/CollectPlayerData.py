from WebScraper import *
from datetime import date
import BuildData as bd
import nflfastpy as nfl
import multiprocessing
import time

#Collects player data for each position using multiprocessing
def get_player_data(year):
    total_time = time.time()
    with multiprocessing.Pool() as pool:
        pool.apply_async(qb_data(year))
        pool.apply_async(flex_data(year))
        pool.apply_async(flex_adv_data(year))
        pool.apply_async(rb_data(year))
        pool.apply_async(rb_adv_data(year))
        pool.close()
        pool.join()
        pool.terminate()
    print("Toal--- %s seconds ---" % (time.time() - total_time))


#Collects qb data for a specific year
def qb_data(year):
    start_time = time.time()
    ws = WebScraper()
    qb_df = bd.player_data("https://www.fantasypros.com/nfl/stats/{position}.php?year="+str(year)+"&scoring=PPR", 'data', ws, ['qb'])
    qb_df.to_csv(r'data/HistoricData/qb_data_'+str(year)+'.csv', index = False, header=True)
    print("QB--- %s seconds ---" % (time.time() - start_time))


#Collects wr and te data for a specific year
def flex_data(year):
    start_time = time.time()
    ws = WebScraper()
    flex_df = bd.player_data("https://www.fantasypros.com/nfl/stats/{position}.php?year="+str(year)+"&scoring=PPR", 'data', ws, ['wr', 'te'])
    flex_df.to_csv(r'data/HistoricData/wr-te_data_'+str(year)+'.csv', index = False, header=True)
    flex_df = bd.opportunity(flex_df)
    flex_df.to_csv(r'data/HistoricData/wr-te_opportunity_'+str(year)+'.csv', index = False, header=True)
    print("Flex--- %s seconds ---" % (time.time() - start_time))

#Collects adv data wr and te
def flex_adv_data(year):
    start_time = time.time()
    flex_df = bd.flex_wopr(nfl.load_pbp_data(year))
    flex_df.to_csv(r'data/HistoricData/wr-te_wopr_'+str(year)+'.csv', index = False, header=True)
    print("Flex Adv--- %s seconds ---" % (time.time() - start_time))

#Collects rb data for a specific year
def rb_data(year):
    start_time = time.time()
    ws = WebScraper()
    rb_df = bd.player_data("https://www.fantasypros.com/nfl/stats/{position}.php?year="+str(year)+"&scoring=PPR", 'data', ws, ['rb'])
    rb_df['IT'] = rb_df['RUSHING ATT'] + rb_df['TGT']
    rb_df['IT/G'] = rb_df['IT']/rb_df['G']
    rb_df.to_csv(r'data/HistoricData/rb_data_'+str(year)+'.csv', index = False, header=True)
    rb_df = bd.opportunity(rb_df)
    rb_df.to_csv(r'data/HistoricData/rb_opportunity_'+str(year)+'.csv', index = False, header=True)
    print("RB--- %s seconds ---" % (time.time() - start_time))

#Collects adv data rb
def rb_adv_data(year):
    start_time = time.time()
    rb_df = bd.rb_share(nfl.load_pbp_data(year))
    rb_df.to_csv(r'data/HistoricData/rb_share_'+str(year)+'.csv', index = False, header=True)
    print("RB Adv--- %s seconds ---" % (time.time() - start_time))

#Collects all data from a start year and an end year
def collect_all_data(start, end):
    for year in range(start, end+1):
        get_player_data(year)

if __name__ == '__main__':
    today = date.today()
    year = today.year
    if(today.month == 1):
        year -= 1
    get_player_data(year)