import backend.epa.test as epa
import pandas as pd
from backend.utils import find_in_data_folder

def main():
    year = 2022
    epa_df = epa.get_epa([2022])
    file_path = find_in_data_folder(f"EPA/epa_{year}.csv")
    epa_df.to_csv(file_path)

    pass_rush_epa = epa.get_rush_pass_epa([2022])
    file_path = find_in_data_folder(f"EPA/epa_pass_rush_{year}.csv")
    pass_rush_epa.to_csv(file_path)


if __name__ == "__main__":
    main()