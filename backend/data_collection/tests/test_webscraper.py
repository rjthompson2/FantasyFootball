from backend.data_collection.WebScraper import DivScraper, RegexWebScraper, DynamicScraper
from backend.data_collection.utils import update_chrome_driver
from backend.data_collection.utils import get_season_year
from backend.data_collection.utils import Positions
import selenium
import logging
import urllib
import pytest


LOG = logging.getLogger(__name__)


class TestWebscrapers:
    def test_divscraper(self):
        try:
            ws = DivScraper()
            ws.start(
                f"https://fantasy.espn.com/football/players/projections", headless=True
            )
            fpts = ws.collect("class", "jsx-2810852873 table--cell tar")
        except selenium.common.exceptions.SessionNotCreatedException:
            update_chrome_driver()
            ws = DivScraper()
            ws.start(
                f"https://fantasy.espn.com/football/players/projections", headless=True
            )
            fpts = ws.collect("class", "jsx-2810852873 table--cell tar")
        assert fpts != [] or fpts != None

    def test_cbs(self):
        year = get_season_year()
        site = "https://www.cbssports.com/fantasy/football/stats/{position}/" + str(year) + "/restofseason/projections/ppr/"
        fpts = []
        ws = RegexWebScraper()
        for position in Positions:
            # print(site.format(position=position.value.upper()))
            data = ws.new_collect(site.format(position=position.value.upper()), prune=[354,-61])
            fpts.append(data)
        assert fpts != [] and fpts != None

    def test_dynamicscraper(self):
        try:
            ws = DynamicScraper()
            ws.start(
                f"https://fantasy.espn.com/football/players/projections", headless=True
            )
            fpts = ws.collect("class", "jsx-2810852873 table--cell tar")
        except selenium.common.exceptions.SessionNotCreatedException:
            update_chrome_driver()
            ws = DivScraper()
            ws.start(
                f"https://fantasy.espn.com/football/players/projections", headless=True
            )
            fpts = ws.collect("class", "jsx-2810852873 table--cell tar")
        assert fpts != [] or fpts != None

