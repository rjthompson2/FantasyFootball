import pytest
import logging
import pandas as pd
from backend.data_collection.Collectors import (
    Collector,
    FPTSDataCollector,
    APICollector,
    InjuryDataCollector,
    CBSDataCollector,
)
from backend.data_collection.WebScraper import WebScraper, DynamicWebScraper
from backend.data_collection.Cleaners import (
    ADPCleaner,
    ECRCleaner,
    FPTSCleaner,
    InjuryCleaner,
    ESPNCleaner,
    CBSCleaner,
)
from backend.data_collection.utils import update_chrome_driver, get_season_year
from selenium.common.exceptions import WebDriverException


LOG = logging.getLogger(__name__)


class TestCollectors:
    def test_adp_collection(self):
        adp = Collector(
            ws=WebScraper(),
            url="https://www.fantasypros.com/nfl/adp/ppr-overall.php",
            _id="id",
            tag="data",
        )
        df = adp.collect_data()
        assert not df.empty
        new_df = ADPCleaner().clean_data(df)
        assert not new_df.equals(df)

    def test_ecr_collection(self):
        # original url: https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php
        year = get_season_year()
        headers = {
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
        api = APICollector(
            url="https://api.fantasypros.com/v2/json/nfl/"
            + str(year)
            + "/consensus-rankings?type=draft&scoring=PPR&position=ALL&week=0&experts=available",
            params=headers,
        )
        data = api.collect_data()

        assert data
        assert not data == {}
        df = ECRCleaner().clean_data(data)
        assert not df.empty

    def test_ftps_collection_individual(self):
        year = get_season_year()
        fdc = FPTSDataCollector(
            aggr_sites={
                "https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring=PPR&week=draft": [
                    "data",
                    "id",
                ],
                # "https://eatdrinkandsleepfootball.com/fantasy/projections/{position}/": [
                #     "projections",
                #     "class",
                # ], 
            }
        )

        try:
            df = fdc.get_site_data(
                "https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring=PPR&week=draft"
            )
        except WebDriverException:
            update_chrome_driver()
            df = fdc.collect_data()

        # LOG.warning(df)
        assert df
        assert not df == {}
        new_df = FPTSCleaner().clean_data(df)
        assert not new_df.equals(df)

        # df = None
        # try:
        #     df = fdc.get_site_data(
        #         "https://www.cbssports.com/fantasy/football/stats/{position}/"
        #         + str(year)
        #         + "/restofseason/projections/ppr/"
        #     )
        # except WebDriverException:
        #     update_chrome_driver()
        #     df = fdc.collect_data()

        # # LOG.warning(df)
        # assert df
        # assert not df == {} #DEPRECATED
        # new_df = FPTSCleaner().clean_data(df)
        # assert not new_df.equals(df)

        # df = None
        # try:
        #     df = fdc.get_site_data(
        #         "https://eatdrinkandsleepfootball.com/fantasy/projections/{position}/"
        #     )
        # except WebDriverException:
        #     update_chrome_driver()
        #     df = fdc.collect_data()

        # # LOG.warning(df)
        # assert df
        # assert not df == {}
        # new_df = FPTSCleaner().clean_data(df)
        # assert not new_df.equals(df)

    def test_ftps_collection(self):
        year = get_season_year()
        fdc = FPTSDataCollector(
            aggr_sites={
                "https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring=PPR&week=draft": [
                    "data",
                    "id",
                ],
                # "https://eatdrinkandsleepfootball.com/fantasy/projections/{position}/": [
                #     "projections",
                #     "class",
                # ], 
            }
        )

        try:
            df = fdc.collect_data()
        except WebDriverException:
            update_chrome_driver()
            df = fdc.collect_data()

        assert df
        new_df = FPTSCleaner().clean_data(df)
        assert not new_df.equals(df)
        # assert len(new_df.loc["PLAYER" == new_df.iloc[0]["PLAYER"]]) >= 3

    def test_cbs_collection(self):
        year = get_season_year()
        cbsc = CBSDataCollector(
            url="https://www.cbssports.com/fantasy/football/stats/{position}/"
                + str(year)
                + "/restofseason/projections/ppr/"
        )
        data = cbsc.collect_data()
        for value in data:
            assert value != []
        new_df = CBSCleaner().clean_data(data)
        print(1)
        assert type(new_df) == pd.DataFrame and not new_df.empty

    def test_espn_collection(self):
        # original url: https://fantasy.espn.com/football/players/projections
        year = get_season_year()
        headers = {
            "Host": "fantasy.espn.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Fantasy-Source": "kona",
            "X-Fantasy-Filter": '{"players":{"filterStatsForExternalIds":{"value":['
            + str(year - 1)
            + ","
            + str(year)
            + ']},"filterSlotIds":{"value":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,23,24]},"filterStatsForSourceIds":{"value":[0,1]},"useFullProjectionTable":{"value":true},"sortAppliedStatTotal":{"sortAsc":false,"sortPriority":3,"value":"102022"},"sortDraftRanks":{"sortPriority":2,"sortAsc":true,"value":"PPR"},"sortPercOwned":{"sortPriority":4,"sortAsc":false},"limit":1000,"filterRanksForSlotIds":{"value":[0,2,4,6,17,16]},"filterStatsForTopScoringPeriodIds":{"value":2,"additionalValue":["002022","102022","002021","022022"]}}}',
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

        api = APICollector(
            url="https://fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leaguedefaults/3?view=kona_player_info",
            # url = "https://fantasy.espn.com/football/players/projections",
            params=headers,
        )
        data = api.collect_data()
        assert data
        df = ESPNCleaner().clean_data(data)
        assert not df.empty

    def test_injury_collection(self):
        year = get_season_year()
        idc = InjuryDataCollector(
            url="https://www.draftsharks.com/injury-predictor/{position}"
        )

        try:
            df = idc.collect_data()
        except WebDriverException:
            update_chrome_driver()
            df = idc.collect_data()
        print(df)

        assert not df.empty
        new_df = InjuryCleaner().clean_data(df)
        assert not new_df.equals(df)
