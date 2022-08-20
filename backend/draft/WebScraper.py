from backend.data_collection.WebScraper import DynamicScraper
from backend.utils import find_in_data_folder
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as BS
from typing import Tuple
import pandas as pd
import os
import time
import re

class FantasyScraper(DynamicScraper):
    '''Yahoo Fantasy Football dynamic scraper'''
    def __init__(self):
        self.username, self.password, self.user = self.get_user()

    def collect(self, tag:str) -> pd.DataFrame:
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
    
    def check_login(self) -> None:
        '''Checks to see if logged in and logs in if not'''
        soup_file = self.driver.page_source
        soup = BS(soup_file, features="lxml")
        if soup.find(text="Please sign in to your Yahoo account to draft") != None:
            self.login()

    def login(self) -> None:
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
    
    def get_user(self) -> str:
        '''Gets the username and password from UserInfo'''
        f = open(find_in_data_folder("UserInfo.txt"), "r")
        words = f.read().split() 
        return words[2].translate({ord('"'): None}), words[5].translate({ord('"'): None}), words[8].translate({ord('"'): None})
        
    def quit(self) -> None:
        '''Shuts down the browser'''
        self.driver.quit()

    def find_round(self) -> int:
        '''gets the current round'''
        soup = BS(self.driver.page_source, features='lxml')
        found_list = soup.findAll('li', {'class': 'W-100 Py-6 Ta-c Fz-s Fw-b ys-order-round'})
        current_round = re.sub('<.*?>', "", str(found_list[0]))
        current_round = re.sub('Round ', "", str(current_round))
        return int(current_round)
    
    def find_order(self) -> list:
        '''gets the names of every player in draft order'''
        self.driver.find_elements_by_xpath('//*[@id="draft"]/div[5]/ul/li[2]')[0].click()
        soup = BS(self.driver.page_source, features='lxml')
        players = soup.findAll('option')
        self.driver.find_elements_by_xpath('//*[@id="draft"]/div[5]/ul/li[3]')[0].click()
        players = [re.sub('<.*?>', "", str(player)) for player in players]
        return players