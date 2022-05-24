from Draft import *
from WebScraper import *
import BuildData as bd
import time

def main(args:list):
    if args == None or len(args) < 3:
        total_teams = int(input("Enter total number of teams: "))
        pos = int(input("Enter draft position: "))
        url = input("Enter draft url: ")
    else:
        total_teams = arg[0]
        pos = arg[1]
        url = arg[2]
    drft = Draft(pd.read_csv(r'draft_order.csv'), total_teams)
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
            pd.DataFrame(drft.draft).to_csv(r'league_draft.csv', index = True, header=True)
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