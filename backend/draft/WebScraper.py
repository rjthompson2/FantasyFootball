from backend.data_collection.WebScraper import DynamicScraper
from backend.utils import find_in_data_folder
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as BS
from typing import Tuple
import pandas as pd
import os
import time
import re
import pickle


class FantasyScraper(DynamicScraper):
    """Yahoo Fantasy Football dynamic scraper"""

    def __init__(self):
        self.username, self.password, self.user = self.get_user()

    def collect(self, tag: str) -> pd.DataFrame:
        """Collects the draft order data from the webpage"""
        df = pd.DataFrame()
        try:
            soup = BS(self.driver.page_source, features="lxml")
            table = soup.findAll("table", {"id": tag})
            read_tables = pd.read_html(str(table))
            for read_table in read_tables:
                df = pd.concat([df, read_table])
                df.columns = df.iloc[0]
                df = df.drop(index=0)
            return df
        except Exception:
            return pd.DataFrame()

    def check_login(self) -> None:
        """Checks to see if logged in and logs in if not"""
        soup_file = self.driver.page_source
        soup = BS(soup_file, features="lxml")
        if soup.find(text="Please sign in to your Yahoo account to draft") != None:
            self.login()

    def login(self) -> None:
        time.sleep(5)
        """Logs in given the information in UserInfo"""
        self.driver.find_element(
            "xpath", '//*[@id="connecting"]/div/div/div[2]/a'
        ).click()  # Clicks to be taken to the login

        # Enters the username
        username = WebDriverWait(self.driver, 200).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="login-username"]')))
        username.send_keys(self.username)
        self.driver.find_element("xpath", '//*[@id="login-signin"]').click()

        # Tries to enter the password
        password = WebDriverWait(self.driver, 200).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="login-passwd"]')))
        password.send_keys(self.password)
        self.driver.find_element("xpath", '//*[@id="login-signin"]').click()

        time.sleep(2)

        # Clicks out of the popup
        # try:
        #     element = WebDriverWait(self.driver, 30).until(
        #         EC.element_to_be_clickable((By.XPATH, '//*[@id="modalContent"]/div[1]/button'))
        #     )
        #     element.click() # Clicks out of the popup
        # except:
        #     print("Automation not working. Need to manually exit the tiny X next time")

    def get_cookies(self):
        # Save the cookie if applicable
        with open(os.getcwd()+"/backend/draft/cookies/cookies.pkl", 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)
    
    def load_cookies(self):
        # Loads the cookies
        cookies = pickle.load(open(os.getcwd()+"/backend/draft/cookies/cookies.pkl", "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()

    def get_user(self) -> str:
        """Gets the username and password from UserInfo"""
        f = open(find_in_data_folder("UserInfo.txt"), "r")
        words = f.read().split()
        return (
            words[2].translate({ord('"'): None}),
            words[5].translate({ord('"'): None}),
            words[8].translate({ord('"'): None}),
        )

    def quit(self) -> None:
        """Shuts down the browser"""
        self.driver.quit()

    def find_round(self) -> int:
        """gets the current round"""
        found_list = []
        while len(found_list) <= 0:
            soup = BS(self.driver.page_source, features="lxml")
            found_list = soup.findAll(
                "li", {"class": "W-100 Py-6 Ta-c Fz-s Fw-b ys-order-round"}
            )
        current_round = re.sub("<.*?>", "", str(found_list[0]))
        current_round = re.sub("Round ", "", str(current_round))
        return int(current_round)

    def find_order(self) -> list:
        """gets the names of every player in draft order"""
        soup = BS(self.driver.page_source, features="lxml")
        players = soup.findAll("div", 
            {"class": "Grid-U Va-m Fz-s Ell"}
        )
        players = [re.sub("<.*?>", "", str(player)) for player in set(players)]
        return players
    
    def navigate_to_data(self):
        try:
            self.driver.find_element(By.XPATH, '//*[@id="draft"]/div[4]/div/div/ul/li[3]/button').click()
        except Exception as e:
            print(e)
            return

    def draft_player(self, player_name:str) -> None:
        success = True
        try:
            #Click the Players tab
            self.driver.find_element(By.XPATH, '//*[@id="draft"]/div[4]/div/div/ul/li[1]/button').click()

            #Enter player name into search bar
            self.driver.find_element(By.XPATH, '//*[@id="search"]').send_keys(player_name)
            self.driver.find_element(By.XPATH, '//*[@id="player-details"]/div[2]/div[2]/button[1]').click()
        except Exception as e:
            success = False
            print(e)

        self.navigate_to_data
        return success