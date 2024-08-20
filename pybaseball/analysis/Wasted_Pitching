from pybaseball import pitching_stats
import pandas as pd

# Fetching pitching data from 2000 to 2023
pitching_data = pd.concat([pitching_stats(year) for year in range(2000, 2024)])

# Keep only relevant columns
pitching_data = pitching_data[['Team', 'Year', 'ERA', 'FIP', 'WAR']]

from pybaseball import batting_stats

# Fetching hitting data from 2000 to 2023
hitting_data = pd.concat([batting_stats(year) for year in range(2000, 2024)])

# Keep only relevant columns
hitting_data = hitting_data[['Team', 'Year', 'BA', 'OPS', 'WAR']]

from pybaseball import team_stats

# Fetching team stats for wins, losses, and runs from 2000 to 2023
team_performance = pd.concat([team_stats(year) for year in range(2000, 2024)])

# Keep only relevant columns
team_performance = team_performance[['Team', 'Year', 'W', 'L', 'R', 'RA']]

# Normalize team names if necessary and merge datasets on Team and Year
pitching_data['Team'] = pitching_data['Team'].str.replace(' ', '')
hitting_data['Team'] = hitting_data['Team'].str.replace(' ', '')
team_performance['Team'] = team_performance['Team'].str.replace(' ', '')

# Merge pitching and hitting data
combined_data = pd.merge(pitching_data, hitting_data, on=['Team', 'Year'], suffixes=('_pitching', '_hitting'))

# Merge with team performance data
combined_data = pd.merge(combined_data, team_performance, on=['Team', 'Year'])

# Calculate league averages for ERA, FIP, OPS
league_avg = combined_data.groupby('Year').mean().reset_index()
league_avg = league_avg[['Year', 'ERA', 'FIP', 'OPS']]

# Merge league averages back to the main dataset
combined_data = pd.merge(combined_data, league_avg, on='Year', suffixes=('', '_league_avg'))

# Calculate relative metrics
combined_data['ERA+'] = combined_data['ERA_league_avg'] / combined_data['ERA']
combined_data['FIP+'] = combined_data['FIP_league_avg'] / combined_data['FIP']
combined_data['OPS+'] = combined_data['OPS'] / combined_data['OPS_league_avg']

# Calculate the disparity ratio
combined_data['Disparity_Ratio'] = combined_data['ERA+'] / combined_data['OPS+']

# Sort data by Disparity Ratio to identify teams with the highest disparities
disparity_data = combined_data.sort_values(by='Disparity_Ratio', ascending=False)

# Top 10 teams with the greatest disparity
top_disparity_teams = disparity_data[['Team', 'Year', 'ERA+', 'OPS+', 'Disparity_Ratio']].head(10)
print(top_disparity_teams)

import matplotlib.pyplot as plt

# Plotting the top 10 teams with the greatest disparities
plt.figure(figsize=(10, 6))
plt.barh(top_disparity_teams['Team'] + ' (' + top_disparity_teams['Year'].astype(str) + ')', top_disparity_teams['Disparity_Ratio'])
plt.xlabel('Pitching to Hitting Disparity Ratio')
plt.title('Top 10 MLB Teams with Greatest Pitching to Hitting Disparity (2000-2023)')
plt.gca().invert_yaxis()
plt.show()
