import plotly.graph_objects as go

def create_player_vs_team_chart(player_name, condensed_data, metrics):
    """
    Creates a bar chart comparing a player's stats to the team's average stats.

    Args:
        player_name (str): The name of the player.
        condensed_data (pd.DataFrame): The dataset containing the stats for all players on the team.
        metrics (list): The list of metrics to compare (e.g., ["shooting_production", "ancillary_production", "total_production"]).

    Returns:
        plotly.graph_objects.Figure: The bar chart figure.
    """
    # Extract the player's stats
    player_stats = condensed_data[condensed_data["PLAYER"] == player_name][metrics].iloc[0]

    # Calculate the team's average stats excluding the selected player
    team_average_stats = condensed_data[condensed_data["PLAYER"] != player_name][metrics].mean()

    # Create the bar chart
    fig = go.Figure()

    # Add player's stats to the chart
    fig.add_trace(go.Bar(
        x=metrics,
        y=player_stats,
        name=f"{player_name}'s Stats",
        marker_color='blue'
    ))

    # Add team's average stats to the chart
    fig.add_trace(go.Bar(
        x=metrics,
        y=team_average_stats,
        name="Team Average (Excluding Player)",
        marker_color='orange'
    ))

    # Update layout
    fig.update_layout(
        title=f"Player vs Team Average Stats: {player_name}",
        xaxis_title="Metrics",
        yaxis_title="Values",
        barmode='group',
        template="plotly_white"
    )

    return fig