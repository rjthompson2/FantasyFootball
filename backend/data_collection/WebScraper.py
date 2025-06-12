from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from abc import ABC
from itertools import repeat
import pandas as pd
import multiprocessing
import requests
import asyncio
import os
import csv
import urllib
import logging
import re
import time


LOG = logging.getLogger(__name__)


# asyncronous api collector
async def collect_api_data(url: str, headers=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            try:
                response = await resp.json()
                return response
            except aiohttp.client_exceptions.ContentTypeError:
                return {}


class Scraper(ABC):
    driver = None

    def start(self, url:str, params=None):
        """Gets a request for the url"""
        self.driver = requests.get(url, params=None)

    def collect(self):
        pass

    def new_collect(self, url, id, tag, params=None):
        self.start(url, params=params)
        return self.collect(id, tag)



class WebScraper(Scraper):
    """Generalized scraper for collecting data from static webpages"""

    def collect(self, id, tag)->pd.DataFrame:
        # df = pd.DataFrame()
        if self.driver == None or not self.driver.ok:
            print("Could not connect.")
            return pd.DataFrame()
        soup = BS(self.driver.content, features="lxml")
        table = soup.findAll("table", {id: tag})
        read_tables = pd.read_html(str(table))
        df = pd.concat(read_tables)
        # for read_table in read_tables:
        #     df = df.append(read_table) #DEPRECATED
        return df


class RegexWebScraper(Scraper):
    """Generalized scraper for collecting data from static webpages"""
    def collect(self, prune:list=None):
        soup = BS(self.driver.content, features="lxml")
        text = soup.get_text()
        values = text.split()
        if prune:
            start = prune[0]
            end = prune[1]
            values = values[start:end]
        return values

    def new_collect(self, url, params=None, prune:list=None):
        self.start(url, params=params)
        return self.collect(prune=prune)




class FilterWebScraper(Scraper):
    """Generalized scraper for collecting data from static webpages"""

    def collect(self, filters):
        df = pd.DataFrame()
        if self.driver == None or not self.driver.ok:
            print("Could not connect.")
            return pd.DataFrame()

        found_dict = {}
        for find in filters:
            soup = BS(self.driver.content, features="lxml")
            table = soup.findAll("span", {"class": find})
            if find == "player-name":
                table = table[1::2]
            found_dict.update({find: [x.text for x in table]})

        df = pd.DataFrame.from_dict(found_dict)

        return df

    def new_collect(self, url, filters):
        self.start(url)
        return self.collect(filters)


class DynamicScraper(ABC):
    """Generalized scraper for dynamic webpages"""

    driver = None

    def start(self, url, headless=False, debug=False):
        """Opens a chrome browser and connects to the url"""
        opts = Options()
        if headless:
            opts.add_argument("--headless")
        if debug:
            opts.add_experimental_option("detach", True)
        opts.add_argument("--incognito")
        self.driver = webdriver.Chrome(
            options=opts,
            service=Service(ChromeDriverManager().install()),
        )
        self.driver.get(url)

    def collect(self):
        pass


class DynamicWebScraper(DynamicScraper):
    """Generalized scraper for collecting data dynamic static webpages"""

    def collect(self, id, tag):
        if id == "id":
            df = pd.read_html(
                self.driver.find_element_by_id(tag).get_attribute("outerHTML")
            )[0]
        elif id == "class":
            columns = []
            heading = self.driver.find_elements(
                "xpath", 
                "//*[@class= '" + tag + "']/thead/tr/th"
            )
            for column in heading:
                columns.append(column.text)
            columns = [column for column in columns if column != ""]

            body = self.driver.find_elements(
                "xpath", 
                "//*[@class= '" + tag + "']/tbody/tr/td"
            )
            i = 1
            values = []
            dfs = []
            for value in body:
                if value.text != "" and value.text != "+ Show History »":
                    values.append(value.text)
                    if i >= len(columns):
                        i = 1
                        dfs.append(values)
                        values = []
                    else:
                        i += 1

            df = pd.DataFrame(data=dfs, columns=columns)
        return df


class DivScraper(DynamicScraper):
    def collect(self, _id, data):
        content = self.driver.page_source
        soup = BS(content, features="lxml")
        found_list = soup.findAll("div", {_id: data})
        return [x.text for x in found_list]


# class ECRScraper(DynamicWebScraper):
#     def collect(self, id, tag):
#         #class="select-advanced__button"
#         #class="select-advanced-content select-advanced-content--button"
#         #class="select-advanced__item"
#         # self.click("select-advanced__button", 0)
#         self.click("select-advanced__button", 4)

#         return super().collect(id, tag)

#     def click(self, _class: str, i = 0):
#         buttons = self.driver.find_elements_by_class_name(_class)

#         if len(buttons) <= 0:
#             raise RuntimeError("Unable to find the button.")

#         try:
#             buttons[i].click()
#         except ElementNotInteractableException:
#             return self.click(_class, i+1)

#         LOG.warning(i)

#         # [LOG.warning(button.location) for button in buttons]


class InjuryScraper(DynamicScraper):
    """NFL injury history dynamic scraper"""

    index = 0

    # TODO multiprocessing/better crawling
    def collect_all(self):
        df_list = []
        callback_list = []
        pages = []

        try:
            while not self.is_last():
                print(self.index)
                try:
                    df_list.append(
                        self.collect(self.driver.page_source, "datatable center")
                    )
                except Exception as e:
                    print(str(e))
                    print("Collection stopped")
                    break
                # time.sleep(3)
                self.next()
                self.index += 1
        except:
            print("Collection fully stopped")

        # i = 0
        # with multiprocessing.Pool() as pool:
        #     df = pool.starmap_async(self.collect, zip(repeat(pages), "datatable center"), callback=lambda x: callback_list.append(x))
        #     df_list = df.get()
        #     print(i)
        #     i+=1
        #     pool.close()
        #     pool.join()
        #     pool.terminate()

        self.quit()
        return df_list

    def collect(self, page_source, tag):
        """Collects the draft order data from the webpage"""
        df = pd.DataFrame()
        soup = BS(page_source, features="lxml")
        table = soup.findAll("table", {"class": tag})
        read_tables = pd.read_html(str(table))
        for read_table in read_tables:
            # df = df.append(read_table) #DEPRECATED
            df = pd.concat([df, read_table])
            df.columns = df.iloc[0]
            df = df.drop(index=0)
        return df

    def is_last(self):
        soup = BS(self.driver.page_source, features="lxml")
        final = soup.findAll('<p class="bodyCopy">Next</p>')
        return not final == []

    def next(self):
        self.driver.find_elements_by_xpath(
            "/html/body/div[4]/table[2]/tbody/tr/td[4]/p/a"
        )[0].click()

    def find(self, start):
        # time.sleep(3)
        self.index = start
        self.driver.find_elements_by_xpath(
            "/html/body/div[4]/table[2]/tbody/tr/td[3]/p/a"
        )[start].click()

    def quit(self):
        """Shuts down the browser"""
        self.driver.quit()
