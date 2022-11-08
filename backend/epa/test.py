import pandas as pd
# from matplotlib import pyplot as plt
# import matplotlib as mpl
# import numpy as np
# from scipy import stats
# import seaborn as sns

#TODO need to get current year
df = pd.read_csv('https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2022.csv.gz', compression='gzip', low_memory=False)

epa_df = pd.DataFrame({
    'offense_epa': df.groupby('posteam')['epa'].sum(),
    'offense_plays': df['posteam'].value_counts(),
    'offense_yards': df.groupby('posteam')['yards_gained'].sum(), 
})

epa_df['offense_epa/play'] = epa_df['offense_epa'] / epa_df['offense_plays']

epa_df.sort_values(by='offense_epa/play', ascending=False).head()

epa_df['defense_epa'] = df.groupby('defteam')['epa'].sum()
epa_df['defense_plays'] = df['defteam'].value_counts()
epa_df['defense_epa/play'] = epa_df['defense_epa'] / epa_df['defense_plays']
epa_df['defense_yards_given_up'] = df.groupby('defteam')['yards_gained'].sum()


epa_df.sort_values(by='defense_epa/play', ascending=False).head()

print(epa_df)