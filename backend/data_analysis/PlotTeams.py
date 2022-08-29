import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

def main(year):
    df_rush_share = pd.read_csv('data/rush_share_'+str(year)+'.csv')
    df_rush_yards = pd.read_csv('data/rush_yards_share_'+str(year)+'.csv')
    df_wopr = pd.read_csv('data/wopr_'+str(year)+'.csv')

    for team in df_rush_share['TEAM'].unique():
        plot(df_rush_share, team, value='Rushing Share', year)
        plot(df_rush_yards, team, value='Rushing Yards Share', year)
        plot(df_wopr, team, value='WOPR', year)

def plot(df, team, value, year=None):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    patterns = ['.', 'x', '*', '^', 's']
    c = 0
    p = 0

    df = df.loc[df['TEAM']==team]
    columns = [column for column in df.columns if column not in ['PLAYER', 'TEAM', "AVG"]]
    new_df = df[columns]

    plt.figure()
    for i in range(len(new_df.index)):
        plt.plot(columns, new_df.iloc[i], colors[c]+patterns[p], label=df.iloc[i]['PLAYER'])
        plt.plot(columns, new_df.iloc[i], colors[c])

        #iterate through colors and patterns
        #loop back to the beginning of each list when the index exceeds the list's length
        c+=1
        c%=len(colors)
        #only proceed to the next pattern type when the color resets to index 0
        if c == 0:
            p += 1
            p %= len(patterns)

    plt.title(team + " Weekly " + value)
    plt.xlabel("Week")
    plt.ylabel(value)
    plt.legend()
    if year:
        plt.savefig('data/WeeklyTeam/'+year+re.sub(' ', '', value)+'/'+team+'_'+re.sub(' ', '_', value.lower())+'.png')
    else:
        plt.savefig('data/WeeklyTeam'+re.sub(' ', '', value)+'/'+team+'_'+re.sub(' ', '_', value.lower())+'.png')
    plt.close()

if __name__ == '__main__':
    today = date.today()
    year = today.year
    if(today.month == 1):
        year -= 1
    main(year)