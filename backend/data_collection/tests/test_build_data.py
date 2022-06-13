from backend.data_collection.Bootstrap import get_bootstrap, get_cf
from backend.data_collection.BuildData import build_players, fix_ecr
from backend.data_collection.Collectors import Collector, FPTSDataCollector
from backend.data_collection.Cleaners import ADPCleaner, ECRCleaner, FPTSCleaner
from backend.data_collection.utils import get_season_year
from backend.data_collection.WebScraper import WebScraper, DynamicWebScraper
import pytest
import logging


LOG = logging.getLogger(__name__)
YEAR = get_season_year()


class TestBuildData():
    def test_build_players(self):
        fdc = FPTSDataCollector(
            aggr_sites={
                'https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring=PPR&week=draft': ['data', 'id'], 
                'https://www.cbssports.com/fantasy/football/stats/{position}/'+str(YEAR)+'/restofseason/projections/ppr/': ['TableBase-table',  'class'],
                'https://eatdrinkandsleepfootball.com/fantasy/projections/{position}/': ['projections',  'class']
            }
        )

        fpts_df = fdc.collect_data()
        fpts_df = FPTSCleaner().clean_data(fpts_df)

        replacement_players, replacement_values = build_players(fpts_df)
        assert "TE" in list(replacement_values.keys())

    def test_build_players_full(self):
        fdc = FPTSDataCollector(
            aggr_sites={
                'https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring=PPR&week=draft': ['data', 'id'], 
                'https://www.cbssports.com/fantasy/football/stats/{position}/'+str(YEAR)+'/restofseason/projections/ppr/': ['TableBase-table',  'class'],
                'https://eatdrinkandsleepfootball.com/fantasy/projections/{position}/': ['projections',  'class']
            }
        )
        cleaner = FPTSCleaner()

        fpts_df = fdc.collect_data()
        fpts_df = cleaner.clean_data(fpts_df)

        data = get_bootstrap(fpts_df)
        cf_df = get_cf(data)
        pos_df = fpts_df[["PLAYER", "POS"]]
        cf_df = pos_df.drop_duplicates(subset=['PLAYER']).merge(cf_df, on="PLAYER", copy=False)
        all_positions = cf_df["POS"].unique()
        assert 'QB' in all_positions
        assert 'RB' in all_positions
        assert 'WR' in all_positions
        assert 'TE' in all_positions
        assert len(cf_df["PLAYER"].values) == len((cf_df["PLAYER"].unique()))

        replacement_players, replacement_values = build_players(cf_df)
        assert "TE" in list(replacement_values.keys())

    def test_fix_ecr(self):
        adp = Collector(ws=WebScraper(), url="https://www.fantasypros.com/nfl/adp/ppr-overall.php", _id='id', tag='data')
        adp_cleaner = ADPCleaner()
        ecr = Collector(ws=DynamicWebScraper(), url="https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php", _id='id', tag='ranking-table')
        ecr_cleaner = ECRCleaner()
        ecr_df = ecr.collect_data()
        adp_df = adp.collect_data()

        ecr_df = ecr_cleaner.clean_data(ecr_df)
        adp_df = adp_cleaner.clean_data(adp_df)

        ecr_df = fix_ecr(ecr_df, adp_df)
        assert set(ecr_df.columns) == set(["PLAYER", "ECR"])