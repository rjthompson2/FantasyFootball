from backend.data_collection.WebScraper import DynamicScraper


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