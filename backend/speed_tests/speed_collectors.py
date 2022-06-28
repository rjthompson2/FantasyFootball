from spedometer import spedometer
from backend.data_collection.Collectors import Collector, InjuryDataCollector, FPTSDataCollector, APICollector
from backend.data_collection.WebScraper import WebScraper, DynamicWebScraper
from backend.data_collection.utils import get_season_year


def main():
    speed_test_adpcollector() #.39 great
    speed_test_ecrcollector() #17.29 slow #TODO make faster
    speed_test_idccollector() #3.01 good
    speed_test_fptscollector() #4.18 okay
    speed_test_espncollector() #.40 great


def speed_test_adpcollector():
    adp = Collector(ws=WebScraper(), url="https://www.fantasypros.com/nfl/adp/ppr-overall.php", _id='id', tag='data')
    spedometer(adp.collect_data)()

def speed_test_ecrcollector():
    ecr_headers = {
        "Host": "api.fantasypros.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "x-api-key": "zjxN52G3lP4fORpHRftGI2mTU8cTwxVNvkjByM3j",
        "Origin": "https://www.fantasypros.com",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://www.fantasypros.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
    }
    ecr = APICollector(url="https://api.fantasypros.com/v2/json/nfl/2022/consensus-rankings?type=draft&scoring=PPR&position=ALL&week=0&experts=available", params=ecr_headers)
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

def speed_test_espncollector():
        year = get_season_year()
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

        api = APICollector(url='https://fantasy.espn.com/apis/v3/games/ffl/seasons/2022/segments/0/leaguedefaults/3?view=kona_player_info', params=headers)
    
        spedometer(api.collect_data)()


if __name__ == "__main__":
    main()
