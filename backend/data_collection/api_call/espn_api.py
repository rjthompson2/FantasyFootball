import requests
import json

response = requests.get('https://sports.core.api.espn.com/v2/sports/football/leagues/nfl')
print(response.text)