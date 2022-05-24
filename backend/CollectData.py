from os.path import exists
from datetime import date
import time
import CollectDraftData as drft
import CollectPlayerData as plyr
import CollectPlayerDataTimeSeries as weeklyData
import CorrelationMap as cm
import PlotTeams as plotWeeklyData
from enum import Enum
from functools import partial

today = date.today()
year = today.year
if(today.month < 8 and today.month > 1):
    year -= 1

class Functions(Enum):
    draft = lambda: drft.get_draft_data(year) if not exists("data/draft_order_"+str(year)+".csv") else next(),
    player = lambda: plyr.get_player_data(year),
    corr_map = lambda: cm.main(2002, year),
    weekly = lambda: weeklyData.main(year),
    plot = lambda: plotWeeklyData.main(year),

class Names(Enum):
    draft = "Draft Data"
    player = "Player Data"
    corr_map = "Correlation Matrix"
    weekly = "Weekly Data"
    plot = "Plot Weekly Data"

enums = [
    'draft',
    'player', 
    'corr_map', 
    'weekly', 
    'plot'
    ]


def main(args) -> None:
    total_time = time.time()

    for enum in enums:
        start_time = time.time()
        Functions[enum].value[0]()
        print(Names[enum].value+"--- %s seconds ---" % (time.time() - start_time))

    print("Total--- %s seconds ---" % (time.time() - total_time))


def next() -> None: #This function does nothing allowing the loop to continue
    pass
    

if __name__ == '__main__':
    main(None)