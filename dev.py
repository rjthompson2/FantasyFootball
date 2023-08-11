import pytest
import logging
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

def test_ftps_collection():
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

    print(cbs_df)
    print(fpts_df)


if __name__ == '__main__':
    test_ftps_collection()