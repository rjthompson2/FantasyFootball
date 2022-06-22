from backend.data_collection.WebScraper import DivScraper, ESPNScraper
import logging


LOG = logging.getLogger(__name__)


class TestWebscrapers():
    def test_divscraper(self):
        ws = DivScraper()
        ws.start(f"https://fantasy.espn.com/football/players/projections", headless=True)
        
        fpts = ws.collect("class", "jsx-2810852873 table--cell tar")
        assert fpts != [] or fpts != None

    def test_espnscraper(self):
        ws = ESPNScraper()
        ws.start(f"https://fantasy.espn.com/football/players/projections", headless=True)
        ws.collect_page(1)
        last = ws.get_last()
        assert last == 22

    
    def test_espnscraper_next(self):
        ws = ESPNScraper()
        ws.start(f"https://fantasy.espn.com/football/players/projections", headless=True)
        first = ws.collect_page(1)
        second = ws.collect_page(2)
        assert not second.empty()
        assert first.values() != second.values()