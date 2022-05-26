from DraftConnector import DraftConnector
from utils import get_season_year

def main():
    dc = DraftConnector(get_season_year())
    dc.run()
    

if __name__ == "__main__":
    main()