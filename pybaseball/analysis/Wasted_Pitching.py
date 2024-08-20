from pybaseball import team_batting, team_pitching, team_results
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Fetch and process pitching data using team_pitching
pitching_data = pd.concat([team_pitching(year).assign(Year=year) for year in range(2000, 2024)])
pitching_data = pitching_data[['Team', 'Year', 'ERA', 'FIP', 'WAR']]

# Step 2: Fetch and process hitting data using team_batting
hitting_data = pd.concat([team_batting(year).assign(Year=year) for year in range(2000, 2024)])
hitting_data = hitting_data[['Team', 'Year', 'BA', 'OPS', 'WAR']]

# Step 3: Fetch and process team performance data using team_results
team_performance = pd.concat([team_results(year).assign(Year=year) for year in range(2000, 2024)])
team_performance = team_performance[['Team', 'Year', 'W', 'L', 'R', 'RA']]

# Step 4: Normalize team names if necessary and merge datasets on Team and Year
pitching_data['Team'] = pitching_data['Team'].str.replace(' ', '')
hitting_data['Team'] = hitting_data['Team'].str.replace(' ', '')
team_performance['Team'] = team_performance['Team'].str.replace(' ', '')

# Merge pitching and hitting data
combined_data = pd.merge(pitching_data, hitting_data, on=['Team', 'Year'], suffixes=('_pitching', '_hitting'))

# Merge with team performance data
combined_data = pd.merge(combined_data, team_performance, on=['Team', 'Year'])

# Step 5: Calculate league averages for ERA, FIP, OPS
league_avg = combined_data.groupby('Year').mean().reset_index()
league_avg = league_avg[['Year', 'ERA', 'FIP', 'OPS']]

# Merge league averages back to the main dataset
combined_data = pd.merge(combined_data, league_avg, on='Year', suffixes=('', '_league_avg'))

# Step 6: Calculate relative metrics
combined_data['ERA+'] = combined_data['ERA_league_avg'] / combined_data['ERA']
combined_data['FIP+'] = combined_data['FIP_league_avg'] / combined_data['FIP']
combined_data['OPS+'] = combined_data['OPS'] / combined_data['OPS_league_avg']

# Step 7: Calculate the disparity ratio
combined_data['Disparity_Ratio'] = combined_data['ERA+'] / combined_data['OPS+']

# Step 8: Sort data by Disparity Ratio to identify teams with the highest disparities
disparity_data = combined_data.sort_values(by='Disparity_Ratio', ascending=False)

# Top 10 teams with the greatest disparity
top_disparity_teams = disparity_data[['Team', 'Year', 'ERA+', 'OPS+', 'Disparity_Ratio']].head(10)
print(top_disparity_teams)

# Step 9: Plotting the top 10 teams with the greatest disparities
plt.figure(figsize=(10, 6))
plt.barh(top_disparity_teams['Team'] + ' (' + top_disparity_teams['Year'].astype(str) + ')', top_disparity_teams['Disparity_Ratio'])
plt.xlabel('Pitching to Hitting Disparity Ratio')
plt.title('Top 10 MLB Teams with Greatest Pitching to Hitting Disparity (2000-2023)')
plt.gca().invert_yaxis()
plt.show()