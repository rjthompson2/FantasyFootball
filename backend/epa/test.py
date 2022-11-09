import nfl_data_py as nfl
import pandas as pd
year = [2022]
# values = nfl.import_pbp_data(years=year).columns.to_list()
# for value in values:
#     if "epa" in value:
#         print(value)
# print(nfl.import_pbp_data(years=year).columns.to_list())


#TODO need to get current year
def get_epa(year):
    df = nfl.import_pbp_data(years=year)

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

    return epa_df

def get_rush_pass_epa(year):
    df = nfl.import_pbp_data(years=year)
    team = []
    
    epa_df = pd.DataFrame({
        'offense_epa': df.groupby('posteam')['epa'].sum(),
        'offense_pass_epa': df.loc[df['play_type']=='pass'].groupby('posteam')['epa'].sum(),
        'offense_rush_epa': df.loc[df['play_type']=='run'].groupby('posteam')['epa'].sum(),
        'offense_epa/play': df.groupby('posteam')['epa'].mean(),
        'offense_pass_epa/play': df.loc[df['play_type']=='pass'].groupby('posteam')['epa'].mean(),
        'offense_rush_epa/play': df.loc[df['play_type']=='run'].groupby('posteam')['epa'].mean(),
    })

    epa_df['defense_epa'] = df.groupby('defteam')['epa'].sum()
    epa_df['defense_pass_epa'] = df.loc[df['play_type']=='pass'].groupby('defteam')['epa'].sum()
    epa_df['defense_rush_epa'] = df.loc[df['play_type']=='run'].groupby('defteam')['epa'].sum()
    epa_df['defense_epa/play'] = df.groupby('defteam')['epa'].mean()
    epa_df['defense_pass_epa/play'] = df.loc[df['play_type']=='pass'].groupby('defteam')['epa'].mean()
    epa_df['defense_rush_epa/play'] = df.loc[df['play_type']=='run'].groupby('defteam')['epa'].mean()

    return epa_df


def epa_schedule(year):
    #https://www.fantasyfootballdatapros.com/blog/intermediate/26
    epa_df = get_epa(year)

    schedule = nfl.import_schedules(years=year)

    team = []
    offense_delta = []
    defense_delta = []

    for i in epa_df.index:
        team.append(i)
        offense_delta.append(delta_epa_offense(i, schedule, epa_df, 10))
        defense_delta.append(delta_epa_defense(i, schedule, epa_df, 10))
        
        
    schedule_epa = pd.DataFrame()
    schedule_epa['Team'] = team
    schedule_epa['Offense_EPA_Delta'] = offense_delta
    schedule_epa['Defense_EPA_Delta'] = defense_delta

    return schedule_epa

def get_opponent(team, schedule):
    team_df = schedule[(schedule['away_team']==team) | (schedule['home_team']==team)]
    opponent = team_df[['week', 'home_team']].where(team_df.away_team == team, team_df[['week', 'away_team']].values)
    return opponent.rename(columns={'home_team':'opp_team'})

def opponent_epa(team, schedule, epa_df):
    opponent = get_opponent(team, schedule)
    epa_opponent = epa_df.reset_index().rename(columns={'index':'opp_team'})
    return opponent.merge(epa_opponent, on = 'opp_team').loc[:,['week',
                                                                'opp_team',
                                                                'offense_epa/play',
                                                                'defense_epa/play']].sort_values(by='week')

def past_future_opp_epa(team, schedule, epa_df, weeks_played):
    opponent_epa_df = opponent_epa(team, schedule, epa_df)
    past_games = opponent_epa_df[opponent_epa_df['week'] <= weeks_played].loc[:,['offense_epa/play','defense_epa/play']].mean()
    future_games = opponent_epa_df[opponent_epa_df['week'] > weeks_played].loc[:,['offense_epa/play','defense_epa/play']].mean()
    return past_games, future_games

def delta_epa_offense(team, schedule, epa_df, weeks_played):
    offense_past = past_future_opp_epa(team, schedule, epa_df, weeks_played)[0]['offense_epa/play']
    offense_future = past_future_opp_epa(team, schedule, epa_df, weeks_played)[1]['offense_epa/play']
    offense_delta = offense_future - offense_past
    return offense_delta

def delta_epa_defense(team, schedule, epa_df, weeks_played):
    defense_past = past_future_opp_epa(team, schedule, epa_df, weeks_played)[0]['defense_epa/play']
    defense_future = past_future_opp_epa(team, schedule, epa_df, weeks_played)[1]['defense_epa/play']
    defense_delta = defense_future - defense_past
    return defense_delta