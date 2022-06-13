from backend.data_collection.utils import get_season_year
from backend.draft.Draft import draft
from backend.utils import find_in_data_folder
from backend.draft.WebScraper import FantasyScraper
import BuildData as bd
import time

def main(args: list):
    if args == None or len(args) < 3:
        total_teams = int(input("Enter total number of teams: "))
        pos = int(input("Enter draft position: "))
        url = input("Enter draft url: ")
    else:
        total_teams = args[0]
        pos = args[1]
        url = args[2]
    year = get_season_year()
    file_path = find_in_data_folder(f'draft_order_{year}.csv')
    drft = Draft(pd.read_csv(file_path), total_teams)
    current_round = 1

    wp = FantasyScraper()
    wp.start(url)
    wp.check_login()
    if pos == 1:
        drft.recommend()
        time.sleep(30)
    while current_round < total_teams * 15:
        if drft.current_team + drft.increment == pos:
            drft.recommend()
            time.sleep(30)
        df = wp.collect('results-by-round')
        if len(df.index) != 0:
            df = bd.build_drafting_data(df)
            drft.automated_draft(df, pos)
            file_path = find_in_data_folder(f'league_draft_{year}.csv')
            pd.DataFrame(drft.draft).to_csv(file_path, index = True, header=True)
            current_round = drft.current_round
    wp.quit()

if __name__ == '__main__':
    total_teams = int(input("Enter total number of teams: "))
    pos = int(input("Enter draft position: "))
    url = input("Enter draft url: ")
    args = [
        total_teams,
        pos,
        url
    ]
    main(args)