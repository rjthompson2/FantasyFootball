from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
from abc import ABC
from itertools import repeat
import pandas as pd
import multiprocessing
import requests
import asyncio
import os

#TODO collect Data using AsyncIO
class Scraper(ABC):
    driver = None

    def start(self, url):
        '''Gets a request for the url'''
        self.driver = requests.get(url)

    
    def collect(self):
        pass

    def new_collect(self, url, id, tag):
        self.start(url)
        return self.collect(id, tag)

#TODO WIP
class AsyncWebScraper(Scraper):
    '''Generalized scraper for asyncronously collecting data from static webpages'''
    def collect(self, id, tag):
        df = pd.DataFrame()
        if self.driver == None or not self.driver.ok:
            print("Could not connect.")
            return pd.DataFrame()
        soup = BS(self.driver.content, features='lxml')
        table = soup.findAll('table', {id: tag})
        read_tables = pd.read_html(str(table))
        for read_table in read_tables:
            df = df.append(read_table)
        return df

class WebScraper(Scraper):
    '''Generalized scraper for collecting data from static webpages'''
    def collect(self, id, tag):
        df = pd.DataFrame()
        if self.driver == None or not self.driver.ok:
            print("Could not connect.")
            return pd.DataFrame()
        soup = BS(self.driver.content, features='lxml')
        table = soup.findAll('table', {id: tag})
        read_tables = pd.read_html(str(table))
        for read_table in read_tables:
            df = df.append(read_table)
        return df

class DynamicScraper(ABC):
    '''Generalized scraper for dynamic webpages'''
    driver = None
        
    def start(self, url, headless=False):
        '''Opens a chrome browser and connects to the url'''
        opts = Options()
        if headless:
            opts.add_argument("--headless")
        chrome_driver = os.getcwd() + "/chromedriver"
        self.driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)
        self.driver.get(url)
        

    def collect(self):
        pass

class DynamicWebScraper(DynamicScraper):
    '''Generalized scraper for collecting data dynamic static webpages'''
    def collect(self, id, tag):
        if id == 'id':
            df = pd.read_html(self.driver.find_element_by_id(tag).get_attribute('outerHTML'))[0]
        elif id == 'class':
            columns = []
            heading = self.driver.find_elements_by_xpath ("//*[@class= '"+tag+"']/thead/tr/th")
            for column in heading:
                columns.append(column.text)
            columns = [column for column in columns if column != ""]
            
            body = self.driver.find_elements_by_xpath ("//*[@class= '"+tag+"']/tbody/tr/td")
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

class FantasyScraper(DynamicScraper):
    '''Yahoo Fantasy Football dynamic scraper'''
    def __init__(self):
        self.username, self.password = self.get_user()

    def collect(self, tag):
        '''Collects the draft order data from the webpage'''
        df = pd.DataFrame()
        try:
            soup = BS(self.driver.page_source, features='lxml')
            table = soup.findAll('table', {'id': tag})
            read_tables = pd.read_html(str(table))
            for read_table in read_tables:
                df = df.append(read_table)
            return df
        except Exception:
            return pd.DataFrame()
    
    def check_login(self):
        '''Checks to see if logged in and logs in if not'''
        soup_file = self.driver.page_source
        soup = BS(soup_file, features="lxml")
        if soup.find(text="Please sign in to your Yahoo account to draft") != None:
            self.login()

    def login(self):
        '''Logs in given the information in UserInfo'''
        self.driver.find_elements_by_xpath('//*[@id="connecting"]/div/div/div[2]/div[3]/a')[0].click() #Clicks to be taken to the login

        #Enters the username
        username = self.driver.find_elements_by_xpath('//*[@id="login-username"]')
        username[0].send_keys(self.username)
        self.driver.find_elements_by_xpath('//*[@id="login-signin"]')[0].click()
        
        time.sleep(1)
        #Tries to enter the password, catches the exception thrown when the captcha appears so the user can complete it and return to the program
        try:
            password = self.driver.find_elements_by_xpath('//*[@id="login-passwd"]')
            password[0].send_keys(self.password)
            self.driver.find_elements_by_xpath('//*[@id="login-signin"]')[0].click()
        except Exception:
            input("Press return after completing the Captcha")
            password = self.driver.find_elements_by_xpath('//*[@id="login-passwd"]')
            password[0].send_keys(self.password)
            self.driver.find_elements_by_xpath('//*[@id="login-signin"]')[0].click()

        time.sleep(5)
        self.driver.find_elements_by_xpath('//*[@id="modalContent"]/a')[0].click() #Clicks out of the popup
    
    def get_user(self):
        '''Gets the username and password from UserInfo'''
        f = open("data/UserInfo.txt", "r")
        words = f.read().split() 
        return words[2].translate({ord('"'): None}), words[5].translate({ord('"'): None})
        
    def quit(self):
        '''Shuts down the browser'''
        self.driver.quit()

class InjuryScraper(DynamicScraper):
    '''NFL injury history dynamic scraper'''
    index = 0

    #TODO multiprocessing/better crawling
    def collect_all(self):
        df_list = []
        callback_list = []
        pages = []

        try:
            while not self.is_last():
                print(self.index)
                try:
                    df_list.append(self.collect(self.driver.page_source, "datatable center"))
                except Exception as e:
                    print(str(e))
                    print("Collection stopped")
                    break
                # time.sleep(3)
                self.next()
                self.index+=1
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
        '''Collects the draft order data from the webpage'''
        df = pd.DataFrame()
        soup = BS(page_source, features='lxml')
        table = soup.findAll('table', {'class': tag})
        read_tables = pd.read_html(str(table))
        for read_table in read_tables:
            df = df.append(read_table)
            df.columns = df.iloc[0]
            df = df.drop(index=0)
        return df
    
    def is_last(self):
        soup = BS(self.driver.page_source, features='lxml')
        final = soup.findAll('<p class="bodyCopy">Next</p>')
        return not final == []

    def next(self):
        self.driver.find_elements_by_xpath('/html/body/div[4]/table[2]/tbody/tr/td[4]/p/a')[0].click()

    def find(self, start):
        # time.sleep(3)
        self.index = start
        self.driver.find_elements_by_xpath('/html/body/div[4]/table[2]/tbody/tr/td[3]/p/a')[start].click()

    def quit(self):
        '''Shuts down the browser'''
        self.driver.quit()


#TODO Cookie-based webscraper
class CookieScraper(ABC):
    pass