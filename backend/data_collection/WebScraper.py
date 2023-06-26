from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
from selenium.common.exceptions import ElementNotInteractableException
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


LOG = logging.getLogger(__name__)


# TODO collect Data using AsyncIO
class Scraper(ABC):
    driver = None

    def start(self, url):
        """Gets a request for the url"""
        self.driver = requests.get(url)

    def collect(self):
        pass

    def new_collect(self, url, id, tag):
        self.start(url)
        return self.collect(id, tag)


# TODO WIP
class AsyncWebScraper(Scraper):
    """Generalized scraper for asyncronously collecting data from static webpages"""

    def collect(self, id, tag):
        if self.driver == None or not self.driver.ok:
            print("Could not connect.")
            return pd.DataFrame()
        soup = BS(self.driver.content, features="lxml")
        table = soup.findAll("table", {id: tag})
        read_tables = pd.read_html(str(table))
        #TODO double check might just be able to return read tables??
        # df = pd.concat([read_table for read_table in read_tables])
        # for read_table in read_tables:
        #     df = df.append(read_table) #DEPRECATED
        return read_tables


class WebScraper(Scraper):
    """Generalized scraper for collecting data from static webpages"""

    def collect(self, id, tag):
        # df = pd.DataFrame()
        if self.driver == None or not self.driver.ok:
            print("Could not connect.")
            return pd.DataFrame()
        soup = BS(self.driver.content, features="lxml")
        table = soup.findAll("table", {id: tag})
        read_tables = pd.read_html(str(table))

        # df = pd.concat([read_table])
        # for read_table in read_tables:
        #     df = df.append(read_table)
        return read_tables


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

    def start(self, url, headless=False):
        """Opens a chrome browser and connects to the url"""
        opts = Options()
        if headless:
            opts.add_argument("--headless")
        chrome_driver = os.getcwd() + "/chromedriver"
        self.driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)
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
            heading = self.driver.find_elements_by_xpath(
                "//*[@class= '" + tag + "']/thead/tr/th"
            )
            for column in heading:
                columns.append(column.text)
            columns = [column for column in columns if column != ""]

            body = self.driver.find_elements_by_xpath(
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
        soup = BS(content)
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
