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


@st.cache_resource
def display_scatter(df, user_team, title):

    if user_team != "League":
        title = f"{user_team} Production vs Points"
        scatter_plot = px.scatter(data_frame=df[df['team'] == user_team],
                                color_discrete_map=color_map,
                                x="total_production",
                                y="pts",
                                color='team',
                                title=title)
    else:
        scatter_plot = px.scatter(data_frame=df,
                                color_discrete_map=color_map,
                                x="total_production",
                                y="pts",
                                color='team',
                                title=title)
    return scatter_plot
