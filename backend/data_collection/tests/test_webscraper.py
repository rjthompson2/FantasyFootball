from backend.data_collection.WebScraper import DivScraper, WebScraper
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
        _id = "class"
        data = "TableBase-table"
        fpts = []
        ws = WebScraper()
        for position in Positions:
            print(site.format(position=position.value.upper()))
            try:
                ws.start(site.format(position=position.value.upper()))
                data = ws.collect(_id, data)
            except selenium.common.exceptions.SessionNotCreatedException:
                update_chrome_driver()
                data = ws.new_collect(site.format(position=position.value.upper()), _id, data)
            fpts.append(data)
        assert fpts != [] or fpts != None
