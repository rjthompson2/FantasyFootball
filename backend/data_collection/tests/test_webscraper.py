from backend.data_collection.WebScraper import DivScraper
from backend.data_collection.utils import update_chrome_driver
import selenium
import logging
import urllib


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
