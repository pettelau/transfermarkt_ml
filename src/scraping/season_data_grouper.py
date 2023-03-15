'''
99946,2012,Championnat National,13,1.46,0,0,0,0,0,0,0,430,9902,wettbewerb
99946,2012,Coupe de France,1,3.0,2,0,0,0,0,0,45,90,9902,pokalwettbewerb
99946,2012,Coupe de la Ligue,1,3.0,0,0,0,0,0,0,0,57,1095,pokalwettbewerb
99946,2012,Ligue 1,1,0.0,0,0,0,0,0,0,0,2,1095,wettbewerb
'''

import pandas as pd

# read the csv file into a pandas dataframe
df = pd.read_csv('season_data_all.csv')

# group the data by player and season, and sum the statistics
grouped_df = df.groupby(['Player_id', 'Season']).agg({
    'Games': 'sum',
    'PPG': 'mean',
    'Goals': 'sum',
    'Assists': 'sum',
    'Yellow_cards': 'sum',
    'Yellow_red_cards': 'sum',
    'Red_cards': 'sum',
    'Penalty_goals': 'sum',
    'Minutes_per_goal': 'mean',
    'Minutes_played': 'sum'
})

# for the 'competition' column, get the most played competition that is also a 'wettbewerb'
def get_most_played_wettbewerb(group):
    wettbewerb_count = group.loc[group['League_type'] == 'wettbewerb'].groupby('Competition')['Games'].sum()
    if wettbewerb_count.empty:
        return ''
    else:
        return wettbewerb_count.idxmax()

competition_df = df.groupby(['Player_id', 'Season']).apply(get_most_played_wettbewerb).rename('Competition')

# join the statistics dataframe with the competition dataframe
result_df = grouped_df.join(competition_df)

# save the result to a new csv file
result_df.to_csv('football_data_grouped.csv')
