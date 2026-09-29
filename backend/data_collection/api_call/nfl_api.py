import nflreadpy as nfl

def get_data(
        years = [2026], 
        columns = [
            'player_name', 
            'position_group', 
            'season', 
            'week', 
            'team', 
            'carries', 
            'targets', 
            'receiving_air_yards', 
            'target_share', 
            'wopr',
        ]
    ):
    data = nfl.load_player_stats(
        seasons=years
    ).to_pandas()
    print(list(data.columns))

    if columns:
        data = data[columns]
    data = data[data['position_group'].isin(["QB", "RB", 'WR', 'TE'])]

    return data