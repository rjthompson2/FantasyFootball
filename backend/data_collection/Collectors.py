from backend.data_collection.WebScraper import (
    WebScraper,
    DynamicWebScraper,
    FilterWebScraper,
    RegexWebScraper,
)
from backend.data_collection.utils import (
    clean_name,
    merge_list,
    list_to_dict,
    update_chrome_driver,
    change_team_name,
    Positions,
    get_season_year,
)
from selenium.common.exceptions import WebDriverException
from itertools import repeat
from typing import List
import pandas as pd
import multiprocessing
import re
import pandas as pd
import requests
import logging


LOG = logging.getLogger(__name__)


class Collector:
    """Generic Collector template"""

    def __init__(self, ws, url, _id, tag):
        self.ws = ws
        self.url = url
        self.id = _id
        self.tag = tag

    def collect_data(self)-> pd.DataFrame:
        if isinstance(self.ws, DynamicWebScraper):
            self.ws.start(self.url, headless=True)
        else:
            self.ws.start(self.url)
        df = self.ws.collect(self.id, self.tag)
        return df


class MultiProssCollector:
    """Generic Collector template with multiprocessing"""

    def __init__(self):
        raise NotImplementedError

    def collect_data(self) -> list:
        # Aggregate all data from the sites
        callback_list = []
        try:
            with multiprocessing.Pool() as pool:
                df_list = pool.starmap_async(
                    self.get_site_data,
                    zip(self.input),
                    callback=lambda x: callback_list.append(x),
                )
                df_list = df_list.get()
                pool.close()
                pool.join()
                pool.terminate()
        except WebDriverException:
            update_chrome_driver()
            self.collect_data()

        return df_list


"""TODO add sites later
    self.reg_sites = [
        'https://fantasydata.com/nfl/fantasy-football-weekly-projections?season={year}&seasontype=1&scope=1&scoringsystem=2&startweek=1&endweek=17'
    ]
    self.unique_sites = [
        'https://www.footballdiehards.com/fantasy-football-player-projections.cfm',
        'https://fantasy.espn.com/football/players/projections'
    ]"""


class FPTSDataCollector(MultiProssCollector):
    """Collects the predicted Fantasy Points for each player"""

    def __init__(self, aggr_sites: dict) -> None:
        self.input = aggr_sites

    def collect_data(self) -> pd.DataFrame:
        # Aggregate all data from the sites
        df_list = super().collect_data()

        # Merge the list into a single pandas dataframe
        df_dict = list_to_dict(df_list)

        return df_dict

    def get_site_data(self, site: str) -> dict:
        year = get_season_year()
        data = self.input[site][0]
        _id = self.input[site][1]

        ws = WebScraper()
        df_dict = {
            data: {
                position.value: (
                    ws.new_collect(site.format(position=position.value), _id, data)
                )
                for position in Positions
            }
        }
        return df_dict

class CBSDataCollector(MultiProssCollector):
    def __init__(self, url: str) -> None:
        year = get_season_year()
        self.input = [position for position in Positions]
        self.site = url

    def collect_data(self) -> pd.DataFrame:
        # Aggregate all data from the sites
        return super().collect_data()

    def get_site_data(self, position: str) -> list:
        regex_schema = {
            "QB": r'<span class="CellPlayerName--long">.*?<a href="[^"]+".*?>([^<]+)<\/a>.*?<\/?span.*?>[\n\s ]* ([^\n]+)\n[ ]*<\/span><span.*?>\n *([^\n]+)\n[\n\s ]* .*[.]*?\n[\n\s \-A-z">]* ([0-9\.]+) [\s]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+)',
            "RB": r'<span class="CellPlayerName--long">.*?<a href="[^"]+".*?>([^<]+)<\/a>.*?<\/?span.*?>[\n\s ]* ([^\n]+)\n[ ]*<\/span><span.*?>\n *([^\n]+)\n[\n\s ]* .*[.]*?\n[\n\s \-A-z">]* ([0-9\.]+) [\s]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+)',
            "WR": r'<span class="CellPlayerName--long">.*?<a href="[^"]+".*?>([^<]+)<\/a>.*?<\/?span.*?>[\n\s ]* ([^\n]+)\n[ ]*<\/span><span.*?>\n *([^\n]+)\n[\n\s ]* .*[.]*?\n[\n\s \-A-z">]* ([0-9\.]+) [\s]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+)',
            "TE": r'<span class="CellPlayerName--long">.*?<a href="[^"]+".*?>([^<]+)<\/a>.*?<\/?span.*?>[\n\s ]* ([^\n]+)\n[ ]*<\/span><span.*?>\n *([^\n]+)\n[\n\s ]* .*[.]*?\n[\n\s \-A-z">]* ([0-9\.]+) [\s]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+)',
            "K": r'<span class="CellPlayerName--long">.*?<a href="[^"]+".*?>([^<]+)<\/a>.*?<\/?span.*?>[\n\s ]* ([^\n]+)\n[ ]*<\/span><span.*?>\n *([^\n]+)\n[\n\s ]* .*[.]*?\n[\n\s \-A-z">]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+) [\s]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.\—]+)',
            "DST": r'<div class="TeamLogoNameLockup-name">.*?<a href="[^"]+".*?>([^<]+)<\/a>.*?<\/?span.*?>[^\n]*\n[\n\s ]* [^\n]*\n[\n\s ]* ">[\n\s ]* ([0-9\.]+) [\s]*<\/td><td[^>]*>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+) [\n\s ]*<\/td><td[^>]*?>[\n\s ]* ([0-9\.]+)',
        }

        html = requests.get(self.site.format(position=position.value.upper())).text

        try:
            results = re.findall(regex_schema[position.value.upper()], html)
            results = [list(result) for result in results]
            return results
        except:
            f = open("backend/test.txt", "a")
            f.write(html + "\n\n\n{NEW LINE}" + position.value.upper() + "!!!!!!!!\n\n\n")
            f.close()
            return []



class InjuryDataCollector(MultiProssCollector):
    """Collects the injury statistics for each player"""

    def __init__(self, url: str) -> None:
        self.input = [
            position for position in Positions if position.value not in ["k", "dst"]
        ]
        self.site = url

    def collect_data(self) -> pd.DataFrame:
        # Aggregate all data from the sites
        df_list = super().collect_data()

        # Merge the list into a single pandas dataframe
        df = pd.concat(df_list, ignore_index=True)

        return df

    def get_site_data(self, position: str) -> pd.DataFrame:
        site = self.site.format(position=position.value)
        filters = [
            "player-name",
            "injury-count",
            "injury-percent",
            "proj-games-missed",
            "prob-injury-per-game",
            "durability-score",
        ]
        ws = FilterWebScraper()
        df = ws.new_collect(site, filters)
        return df


class WebCrawlerCollector:
    def __init__(self, url):
        self.input = url

    def collect_data(self):
        raise NotImplementedError


class APICollector:
    def __init__(self, url, params=None):
        self.input = url
        self.params = params

    def collect_data(self):
        response = requests.get(self.input, headers=self.params)
        return response.json()
