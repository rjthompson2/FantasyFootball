from backend.data_collection.utils import get_season_year
from backend.draft.Draft import Draft
from backend.draft.WebScraper import FantasyScraper
from backend.utils import find_in_data_folder
from backend.data_collection.utils import update_chrome_driver
from selenium.common.exceptions import WebDriverException
import backend.data_collection.BuildData as bd
import pandas as pd
import time
import logging


LOG = logging.getLogger(__name__)


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
    try:
        wp.start(url)
    except WebDriverException:
        update_chrome_driver()
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


def rundraft_webapp(url:str, wait_time=30) -> None:
    #TODO need to change up the values to autofill position in the draft and total teams, and run the draft smoothly
    # Loading from the webpage
    wp = FantasyScraper()
    try:
        wp.start(url)
    except WebDriverException:
        update_chrome_driver()
        wp.start(url)
    except selenium.common.exceptions.InvalidArgumentException:
        wp.quit()
        raise selenium.common.exceptions.InvalidArgumentException
    wp.check_login()
    LOG.warning("DONE")
    
    # Initializes all the values
    year = get_season_year()
    total_teams, names = wp.get_total_teams()
    draft_round = wp.find_round()
    #TODO make find_pos more general
    pos = find_pos(names, 'Riley', draft_round)
    file_path = find_in_data_folder(f'draft_order_{year}.csv')
    drft = Draft(pd.read_csv(file_path), total_teams)
    current_round = 1
    LOG.warning("END")

    #TODO work on getting the drafter to work
    # Run the draft
    if pos == 1:
        drft.recommend()
        time.sleep(wait_time)
    while current_round < total_teams * 15:
        if drft.current_team + drft.increment == pos:
            drft.recommend()
            time.sleep(wait_time)
        df = wp.collect('results-by-round')
        if len(df.index) != 0:
            df = bd.build_drafting_data(df)
            drft.automated_draft(df, pos)
            file_path = find_in_data_folder(f'league_draft_{year}.csv')
            pd.DataFrame(drft.draft).to_csv(file_path, index = True, header=True)
            current_round = drft.current_round
    wp.quit()

def find_pos(names:list, you:str, draft_round:int):
    'Gets the current position from the current round and where you are drafting from'
    if draft_round%2 != 0:
        return names.index(you)
    else:
        return len(names) - names.index(you) + 1


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

