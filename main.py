import streamlit as st
import pandas as pd
from utils.functions import load_data, recreate_dataframe
from utils.view_data_option import calculate_production, replace_nba_abbreviations
from utils.calculations import calculate_production
import plotly.express as px


if "data" not in st.session_state:
    st.session_state.data = load_data("KDAM1/BasketballGames")
st.set_page_config(layout="wide")
st.title("🏀NBA Dashboard")


years = st.session_state.data['season'].unique()
selected_year = st.selectbox("Select a season", label_visibility="collapsed", options=years)
df_plot = st.session_state.data[st.session_state.data['season'] == selected_year]
df_plot = calculate_production(st.session_state.data)
st.write(st.session_state)
selected_columns = ["season", "team", "fg", "fga", "fgmi", "3p", "3pa", "3pmi", "ft", "fta", "ftmi", "ast", "orb", "drb", "tov", "stl", "blk", "pf", "pts", "fg_efficiency",  "ft_efficiency", "total_production", "shooting_production", "ancillary_production", "team_opp", "fg_opp", "fga_opp", "fgmi_opp", "3p_opp", "3pa_opp", "3pmi_opp", "ft_opp", "fta_opp", "ftmi_opp", "ast_opp", "orb_opp", "drb_opp", "tov_opp", "stl_opp", "blk_opp", "pf_opp", "pts_opp", "fg_opp_efficiency", "ft_opp_efficiency", "total_opp_production", "shooting_opp_production", "ancillary_opp_production"]
df = recreate_dataframe(st.session_state.data, selected_columns)
df = replace_nba_abbreviations(df, column="team")
df = replace_nba_abbreviations(df, column="team_opp")
st.write(df.head())

### --------------------------------- Average League Production --------------------------------- ###
average_shooting_production = round(df["shooting_production"].mean(), 2)
average_ancillary_production = round(df["ancillary_production"].mean(), 2)
average_total_production = round(df["total_production"].mean(), 2)

st.markdown("### Average League Production")
col1, col2, col3 = st.columns([1,1,1])
col1.metric(label="Average Shooting Production", value=average_shooting_production)
col2.metric(label="Average Ancillary Production", value=average_ancillary_production)
col3.metric(label="Average Total Production", value=average_total_production)


### --------------------------------- Plot Production vs Points --------------------------------- ###
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


col3, col4 = st.columns([5,1])
st.markdown("### Production vs Points")
user_team = col4.selectbox("Select a team", 
                           label_visibility="collapsed", 
                           options=["All"] + sorted(df["team"].dropna().unique().tolist()))

title = " League Average Production vs Points"

if user_team != "All":
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

col3.plotly_chart(scatter_plot, use_container_width=True)
