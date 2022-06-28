from backend.data_collection.WebScraper import DivScraper
import logging


LOG = logging.getLogger(__name__)


class TestWebscrapers():
    def test_divscraper(self):
        ws = DivScraper()
        ws.start(f"https://fantasy.espn.com/football/players/projections", headless=True)
        
        fpts = ws.collect("class", "jsx-2810852873 table--cell tar")
        assert fpts != [] or fpts != None