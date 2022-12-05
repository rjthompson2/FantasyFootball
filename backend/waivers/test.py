import nfl_data_py as nfl
import pandas as pd

# TODO can speed up with multithreading or async
year = [x for x in range(2018, 2022 + 1)]
# year = [2022]

rush_df = pd.DataFrame()
df = nfl.import_pbp_data(years=year)
rush_df = df.loc[df["play_type"] == "run"].groupby("name")["play_type"].count()
rush_df = pd.DataFrame(rush_df)

injuries = nfl.import_injuries(years=year)
injuries["name"] = injuries.apply(
    lambda x: x["first_name"][0] + "." + x["last_name"], axis=1
)

injury_df = (
    injuries.loc[injuries["position"] == "RB"].groupby("name")["position"].count()
)
injury_df = pd.DataFrame(injury_df)

final_df = rush_df.join(injury_df)
final_df = final_df.rename(columns={"play_type": "rushes", "position": "injuries"})
# FILTERS
# 10 rushes per game. 14 games. 5 years
# final_df = final_df[final_df['rushes'] > 700]
# finds the average amount of runs for people who were injured
# does not take into account people who played an entire season healthy
# final_df = final_df[final_df['position'].notnull()]

# final_df = final_df[final_df['rushes'] > final_df['rushes'].median()]

total_rushes = final_df["rushes"].sum()
avg_rushes = final_df["rushes"].mean()
median_rushes = final_df["rushes"].median()
total_injuries = final_df["injuries"].sum()
rushes_per_injury = total_rushes / total_injuries

print(total_rushes)
print(avg_rushes)
print(median_rushes)
print(rushes_per_injury)
