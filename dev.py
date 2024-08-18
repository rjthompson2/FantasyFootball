from backend.data_collection.WebScraper import DivScraper, RegexWebScraper, DynamicScraper
from backend.data_collection.utils import update_chrome_driver
from backend.data_collection.utils import get_season_year
from backend.data_collection.utils import Positions
from backend.data_collection.Cleaners import CBSCleaner
import selenium
import logging
import urllib

year = get_season_year()
site = "https://www.cbssports.com/fantasy/football/stats/{position}/" + str(year) + "/restofseason/projections/ppr/"
fpts = []
ws = RegexWebScraper()
for position in Positions:
    if position.value == "qb":
        data = ws.new_collect(site.format(position=position.value.upper()), prune=[410,-122])
        f = open("dev.txt", "w")
        for value in data:
            f.write(value+"\n")
        f.close()
        fpts.append(data)
        # exit()
cleaner = CBSCleaner()
final = cleaner.clean_data(fpts)
# print(fpts)
print(final)