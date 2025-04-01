import plotly.express as px
import streamlit as st

color_map = {'Los Angeles Lakers': 'blue',
             'Los Angeles Clippers': 'red',
             'Golden State Warriors': 'yellow',
             'Sacramento Kings': 'purple',
             'Phoenix Suns': 'orange',
             'Denver Nuggets': 'green',
             'Utah Jazz': 'brown',
             'Dallas Mavericks': 'cyan',
             'Houston Rockets': 'pink',
             'San Antonio Spurs': 'gray',
             'Oklahoma City Thunder': 'black',
             'Minnesota Timberwolves': 'magenta',
             'Memphis Grizzlies': 'lime',
             'New Orleans Pelicans': 'teal',
             'Portland Trail Blazers': 'navy',
             'Chicago Bulls': 'maroon',
             'Milwaukee Bucks': 'olive',
             'Indiana Pacers': 'coral',
             'Detroit Pistons': 'salmon',
             'Cleveland Cavaliers': 'gold',
             'Toronto Raptors': 'violet',
             'Atlanta Hawks': 'crimson',
             'Charlotte Hornets': 'lavender',
             'Miami Heat': 'chocolate',
             'Brooklyn Nets': 'indigo',
             'Philadelphia 76ers': 'khaki',
             'Boston Celtics': 'darkgreen',
             'New York Knicks': 'darkorange',
             'Orlando Magic': 'darkviolet',
             'Washington Wizards': 'darkred',}


def display_scatter(data, team, title):
    """
    Creates a scatter plot for the given data.

    Args:
        data (pd.DataFrame): The dataset containing production data.
        team (str): The selected team or "League" for all teams.
        title (str): The title of the scatter plot.

    Returns:
        plotly.graph_objects.Figure: The scatter plot figure.
    """
    if team != "League":
        # Filter data for the selected team
        data = data[data["team"] == team]

    # Create the scatter plot
    fig = px.scatter(
        data,
        x="total_production",
        y="pts",
        color="team",
        hover_data=["team", "total_production", "pts"],
        title=title
    )

    fig.update_layout(
        xaxis_title="Total Production",
        yaxis_title="Points",
        template="plotly_white"
    )

    return fig
