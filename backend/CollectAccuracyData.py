from backend.data_collection.Connectors import AccuracyConnector
from backend.data_collection.utils import get_season_year

def main():
    dc = AccuracyConnector(get_season_year())
    dc.run()
    

if __name__ == "__main__":
    main()