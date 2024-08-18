import nfl_data_py as nfl

df = nfl.import_pbp_data([2023, 2024])
values = ["game_id", "home_team", "away_team", "week", "posteam", "defteam", "yrdln", "ydstogo", "play_type", "yards_gained", "air_yards", "yards_after_catch", "play_type_nfl", "desc"]
full_df = df[values]
full_df.to_csv("ALL_games_data.csv")


sf_df = df.query('home_team == "SF" or away_team == "SF"')
sf_df = sf_df[values]
sf_df.to_csv("SF_games_data.csv")

det_df = df.query('home_team == "DET" or away_team == "DET"')
det_df = det_df[values]
det_df.to_csv("DET_games_data.csv")

sf_det_df = df.query('(home_team == "SF" and away_team == "DET") or (home_team == "DET" and away_team == "SF")')
sf_det_df = sf_det_df[values]
sf_det_df.to_csv("SF_DET_games_data.csv")