from spedometer import spedometer
from backend.data_collection.Collectors import Collector, InjuryDataCollector, FPTSDataCollector
from backend.data_collection.WebScraper import WebScraper, DynamicWebScraper
from backend.data_collection.utils import get_season_year


def main():
    speed_test_adpcollector() #.31 great
    speed_test_ecrcollector() #17 slow #TODO make faster
    speed_test_idccollector() #2.8 good
    speed_test_fptscollector() #5.35 okay


def speed_test_adpcollector():
    adp = Collector(ws=WebScraper(), url="https://www.fantasypros.com/nfl/adp/ppr-overall.php", _id='id', tag='data')
    spedometer(adp.collect_data)()

def speed_test_ecrcollector():
    ecr = Collector(ws=DynamicWebScraper(), url="https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php", _id='id', tag='ranking-table')
    spedometer(ecr.collect_data)()

def speed_test_idccollector():
    idc = InjuryDataCollector(url="https://www.draftsharks.com/injury-predictor/{position}")
    spedometer(idc.collect_data)()

def speed_test_fptscollector():
    year = get_season_year()
    fdc = FPTSDataCollector(
        aggr_sites={
            'https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring=PPR&week=draft': ['data', 'id'], 
            'https://www.cbssports.com/fantasy/football/stats/{position}/'+str(year)+'/restofseason/projections/ppr/': ['TableBase-table',  'class'],
            # 'https://eatdrinkandsleepfootball.com/fantasy/projections/{position}/': ['projections',  'class'], #TODO website deprecated need to grab new data/deprecate
        }
    )
    spedometer(fdc.collect_data)()


if __name__ == "__main__":
    main()
