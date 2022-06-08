from backend.data_collection.Bootstrap import get_bootstrap, get_cf
from backend.data_collection.BuildData import build_players
from backend.data_collection.Collectors import FPTSDataCollector
from backend.data_collection.Cleaners import FPTSCleaner
from backend.data_collection.utils import get_season_year
import pytest


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
        assert "TE" in replacement_values.keys()

    def test_build_players_full(self):
        fdc = FPTSDataCollector(
            aggr_sites={
                'https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring=PPR&week=draft': ['data', 'id'], 
                'https://www.cbssports.com/fantasy/football/stats/{position}/'+str(YEAR)+'/restofseason/projections/ppr/': ['TableBase-table',  'class'],
                'https://eatdrinkandsleepfootball.com/fantasy/projections/{position}/': ['projections',  'class']
            }
        )

        fpts_df = fdc.collect_data()
        fpts_df = FPTSCleaner().clean_data(fpts_df)

        data = get_bootstrap(fpts_df)
        cf_df = get_cf(data)
        pos_df = fpts_df[["PLAYER", "POS"]]
        cf_df = pos_df.merge(cf_df, on="PLAYER")

        replacement_players, replacement_values = build_players(cf_df)
        assert "TE" in replacement_values.keys()
