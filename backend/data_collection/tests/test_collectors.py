import pytest
import logging
from backend.data_collection.Collectors import Collector, FPTSDataCollector, InjuryDataCollector
from backend.data_collection.WebScraper import WebScraper, DynamicWebScraper
from backend.data_collection.Cleaners import ADPCleaner, ECRCleaner, FPTSCleaner, InjuryCleaner
from backend.data_collection.utils import update_chrome_driver, get_season_year
from selenium.common.exceptions import WebDriverException


LOG = logging.getLogger(__name__)


class TestCollectors():
    def test_adp_collection(self):
        adp = Collector(ws=WebScraper(), url="https://www.fantasypros.com/nfl/adp/ppr-overall.php", _id='id', tag='data')
        df = adp.collect_data()
        assert not df.empty
        new_df = ADPCleaner().clean_data(df)
        assert not new_df.equals(df)

    def test_ecr_collection(self):
        ecr = Collector(ws=DynamicWebScraper(), url="https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php", _id='id', tag='ranking-table')
        
        try:
            df = ecr.collect_data()
        except WebDriverException:
            update_chrome_driver()
            df = ecr.collect_data()

        assert not df.empty
        new_df = ECRCleaner().clean_data(df)
        assert not new_df.equals(df)

    def test_ftps_collection_individual(self):
        year = get_season_year()
        fdc = FPTSDataCollector(
            aggr_sites={
                'https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring=PPR&week=draft': ['data', 'id'], 
                'https://www.cbssports.com/fantasy/football/stats/{position}/'+str(year)+'/restofseason/projections/ppr/': ['TableBase-table',  'class'],
                'https://eatdrinkandsleepfootball.com/fantasy/projections/{position}/': ['projections',  'class']
            }
        )

        try:
            df = fdc.get_site_data('https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring=PPR&week=draft')
        except WebDriverException:
            update_chrome_driver()
            df = fdc.collect_data()

        # LOG.warning(df)
        assert df
        assert not df == {}
        new_df = FPTSCleaner().clean_data(df)
        assert not new_df.equals(df)

        df = None
        try:
            df = fdc.get_site_data('https://www.cbssports.com/fantasy/football/stats/{position}/'+str(year)+'/restofseason/projections/ppr/')
        except WebDriverException:
            update_chrome_driver()
            df = fdc.collect_data()

        # LOG.warning(df)
        assert df
        assert not df == {}
        new_df = FPTSCleaner().clean_data(df)
        assert not new_df.equals(df)

        df = None
        try:
            df = fdc.get_site_data('https://eatdrinkandsleepfootball.com/fantasy/projections/{position}/')
        except WebDriverException:
            update_chrome_driver()
            df = fdc.collect_data()

        # LOG.warning(df)
        assert df
        assert not df == {}
        new_df = FPTSCleaner().clean_data(df)
        assert not new_df.equals(df)

    def test_ftps_collection(self):
        year = get_season_year()
        fdc = FPTSDataCollector(
            aggr_sites={
                'https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring=PPR&week=draft': ['data', 'id'], 
                'https://www.cbssports.com/fantasy/football/stats/{position}/'+str(year)+'/restofseason/projections/ppr/': ['TableBase-table',  'class'],
                'https://eatdrinkandsleepfootball.com/fantasy/projections/{position}/': ['projections',  'class']
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
    
    def test_espn_collection(self):
        assert False

    def test_injury_collection(self):
        year = get_season_year()
        idc = InjuryDataCollector(url="https://www.draftsharks.com/injury-predictor/{position}")

        try:
            df = idc.collect_data()
        except WebDriverException:
            update_chrome_driver()
            df = idc.collect_data()
        
        assert not df.empty
        new_df = InjuryCleaner().clean_data(df)
        assert not new_df.equals(df)