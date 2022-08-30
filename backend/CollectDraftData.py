from backend.data_collection.Connectors import DraftConnector
from backend.data_collection.utils import get_season_year


def main(year):
    dc = DraftConnector(year)
    dc.run()


if __name__ == "__main__":
    main(get_season_year())
