from backend.data_collection.Bootstrap import get_bootstrap, get_cf
from backend.data_collection.BuildData import build_players
from backend.data_collection.Collectors import Collector, FPTSDataCollector, CBSDataCollector
from backend.data_collection.Cleaners import ADPCleaner, ECRCleaner, FPTSCleaner, CBSCleaner
from backend.data_collection.utils import get_season_year
from backend.data_collection.WebScraper import WebScraper, DynamicWebScraper
import pytest
import logging


LOG = logging.getLogger(__name__)
YEAR = get_season_year()


class TestBuildData:

    def test_build_players_combine(self):
        fdc = FPTSDataCollector(
            aggr_sites={
                "https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring=PPR&week=draft": [
                    "data",
                    "id",
                ]
            }
        )
        fpts_df = fdc.collect_data()
        fpts_df = FPTSCleaner().clean_data(fpts_df)


        year = get_season_year()
        cbsc = CBSDataCollector(
            url="https://www.cbssports.com/fantasy/football/stats/{position}/"
                + str(year)
                + "/restofseason/projections/ppr/"
        )
        cbs_data = cbsc.collect_data()
        cbs_df = CBSCleaner().clean_data(cbs_data)

        df_list = [fpts_df, cbs_df]



    def test_build_players(self):
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

        fpts_df = fdc.collect_data()
        fpts_df = FPTSCleaner().clean_data(fpts_df)

        replacement_players, replacement_values = build_players(fpts_df)
        assert "TE" in list(replacement_values.keys())

    def test_build_players_full(self):
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
        cleaner = FPTSCleaner()

        fpts_df = fdc.collect_data()
        fpts_df = cleaner.clean_data(fpts_df)

        data = get_bootstrap(fpts_df)
        cf_df = get_cf(data)
        pos_df = fpts_df[["PLAYER", "POS"]]
        cf_df = pos_df.drop_duplicates(subset=["PLAYER"]).merge(
            cf_df, on="PLAYER", copy=False
        )
        all_positions = cf_df["POS"].unique()
        assert "QB" in all_positions
        assert "RB" in all_positions
        assert "WR" in all_positions
        assert "TE" in all_positions
        assert len(cf_df["PLAYER"].values) == len((cf_df["PLAYER"].unique()))

        replacement_players, replacement_values = build_players(cf_df)
        assert "TE" in list(replacement_values.keys())
