import streamlit as st
import pandas as pd

def get_team_data(data, team, year):
    """
    Displays the players on a team based on the provided team and year,
    with each player's stats averaged if there are duplicates.

    Args:
        data (pd.DataFrame): The dataset containing player, team, and season information.
        team (str): The selected team.
        year (int): The selected year.

    Returns:
        None
    """

    # Filter the dataset for the provided team and year
    team_players = data[(data['Team'] == team) & (data['year'] == year)]

    # Check if there are players for the provided team and year
    if team_players.empty:
        st.write(f"No players found for the team: {team} in the year: {year}")
    else:
        # Group by PLAYER and calculate the mean for numeric columns
        numeric_columns = team_players.select_dtypes(include='number').columns
        condensed_players = team_players.groupby(['PLAYER'], as_index=False)[numeric_columns].mean()

        # Add back non-numeric columns like 'Pos_x' if needed (e.g., taking the first value)
        condensed_players = pd.merge(
            condensed_players,
            team_players[['PLAYER', 'Pos_x']].drop_duplicates(subset='PLAYER'),
            on='PLAYER',
            how='left'
        )

        # Display the condensed dataset

        return condensed_players[['PLAYER', 'shooting_production', 'ancillary_production', 'total_production']]