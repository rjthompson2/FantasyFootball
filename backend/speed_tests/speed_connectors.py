from spedometer import spedometer
from backend.data_collection.Connectors import DraftConnector
from backend.data_collection.utils import get_season_year


def main():
    speed_test_connector()


def speed_test_connector():
    dc = DraftConnector(get_season_year())
    spedometer(dc.run)()


if __name__ == "__main__":
    main()
