import nfl_data_py as nfl
import pandas as pd

# roster = nfl.import_rosters([2022])
# print(roster.columns)
# roster = roster[['player_name', 'team', 'position', 'depth_chart_position', 'status']]
# roster = roster.apply(lambda x: pd.Series({column:None for column in roster.columns}) if x['position'] not in ['WR', 'TE', 'QB', 'RB'] else x, axis=1).dropna()
# print(roster)


roster = nfl.import_depth_charts([2022])
roster = roster[["full_name", "formation", "position", "depth_team"]]
roster = roster.apply(
    lambda x: pd.Series({column: None for column in roster.columns})
    if x["position"] not in ["WR", "TE", "QB", "RB"]
    else x,
    axis=1,
).dropna()
print(roster)

injuries = nfl.import_injuries([2022])
injuries = injuries[
    ["full_name", "team", "report_primary_injury", "report_status", "practice_status"]
]
injuries = injuries.dropna()
print(injuries)
