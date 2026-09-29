import requests
import json

LEAGUE_IDS = [
    1258617628876873728,
    1389705952185294848,
]

YEARS = {
    1258617628876873728: 2025,
    1389705952185294848: 2026,
}

def get_all_drafts():
    seasons = []
    for league_id in LEAGUE_IDS:
        response = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/drafts')
        draft_json = json.loads(response.text)
        for draft in draft_json:
            year = draft['season']
            draft_id = draft['draft_id']
            response = requests.get(f'https://api.sleeper.app/v1/draft/{draft_id}/picks')
            picks_json = json.loads(response.text)
            seasons.append({'season': year, 'data': picks_json})
    return seasons

def get_all_transactions():
    transactions = []
    for league_id in LEAGUE_IDS:
        season = YEARS[league_id]
        for round in range(1, 18):
            response = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/transactions/{round}')
            transaction = json.loads(response.text)
            transactions.append({'season': season, 'round': round, 'data': transaction})
    return transactions
