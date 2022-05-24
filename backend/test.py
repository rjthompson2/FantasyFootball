from WebScraper import *
from datetime import date
import BuildData as bd
import re

    
ws = WebScraper()
ws.start("https://www.fantasypros.com/nfl/adp/dst.php?year=2021")
df = ws.collect('id', 'data')
print(df.to_string())