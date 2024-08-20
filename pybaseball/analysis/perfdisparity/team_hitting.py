from pybaseball import team_batting

def fetch_team_batting_data(start_season, end_season=None, league='all', ind=1):
    """
    Fetch and process team batting data for the specified seasons.
    
    Args:
    - start_season (int): The first season for which to fetch data.
    - end_season (int, optional): The last season for which to fetch data. Defaults to None.
    - league (str, optional): League to filter by ('all', 'nl', 'al', 'mnl'). Defaults to 'all'.
    - ind (int, optional): Whether to return individual-season stats (1) or aggregate (0). Defaults to 1.
    
    Returns:
    - pd.DataFrame: DataFrame with the specified columns: 'Team', 'Season', 'AVG', 'OPS', 'WAR'.
    """
    
    # Fetch the data using pybaseball's team_batting function
    data = team_batting(start_season=start_season, end_season=end_season, league=league, ind=ind)
    
    # Filter the DataFrame to only include the required columns
    filtered_data = data[['Team', 'Season', 'AVG', 'OPS', 'WAR']]
    
    return filtered_data

# Example usage
if __name__ == "__main__":
    # Fetch data for the 2020 and 2021 MLB seasons
    batting_data = fetch_team_batting_data(1980, 2023)
    print(batting_data)