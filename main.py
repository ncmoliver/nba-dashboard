import streamlit as st
from utils.functions import load_data, recreate_dataframe
from utils.view_data_option import calculate_production, replace_nba_abbreviations
from utils.calculations import calculate_production
from utils.display_scatterplot import display_scatter
from utils.display_team_logo import display_team_logo
st.set_page_config(layout="wide")

if "data" not in st.session_state:
    st.session_state.data = load_data("KDAM1/BasketballGames")

if "league_checkb" not in st.session_state:
    st.session_state.league_checkb = False

st.title("🏀NBA Dashboard")


years = st.session_state.data['season'].unique()
selected_year = st.selectbox("Select a season", label_visibility="collapsed", options=years)
df_plot = st.session_state.data[st.session_state.data['season'] == selected_year]
df_plot = calculate_production(st.session_state.data)

selected_columns = ["season", "team", "fg", "fga", "fgmi", "3p", "3pa", "3pmi", "ft", "fta", "ftmi", "ast", "orb", "drb", "tov", "stl", "blk", "pf", "pts", "fg_efficiency",  "ft_efficiency", "total_production", "shooting_production", "ancillary_production", "team_opp", "fg_opp", "fga_opp", "fgmi_opp", "3p_opp", "3pa_opp", "3pmi_opp", "ft_opp", "fta_opp", "ftmi_opp", "ast_opp", "orb_opp", "drb_opp", "tov_opp", "stl_opp", "blk_opp", "pf_opp", "pts_opp", "fg_opp_efficiency", "ft_opp_efficiency", "total_opp_production", "shooting_opp_production", "ancillary_opp_production"]
df = recreate_dataframe(st.session_state.data, selected_columns)
df = replace_nba_abbreviations(df, column="team")
df = replace_nba_abbreviations(df, column="team_opp")
with st.expander("View Sample Data"):
    st.write(df.head())

st.markdown("---")

st.markdown("### Average League Production")
st.sidebar.markdown("### Dashboard Toolbar")
st.sidebar.checkbox(label="Hide League Metrics", key="league_checkb")


if st.session_state.league_checkb == False:
    ### --------------------------------- Average League Production --------------------------------- ###
    average_shooting_production = round(df["shooting_production"].mean(), 2)
    average_ancillary_production = round(df["ancillary_production"].mean(), 2)
    average_total_production = round(df["total_production"].mean(), 2)

    col1, col2, col3 = st.columns([1,1,1])
    col1.metric(label="Average Shooting Production", value=average_shooting_production)
    col2.metric(label="Average Ancillary Production", value=average_ancillary_production)
    col3.metric(label="Average Total Production", value=average_total_production)



        ### --------------------------------- Plot Production vs Points --------------------------------- ###


if "team" not in st.session_state:
    user_team = st.selectbox("Select a team", 
                            label_visibility="collapsed", 
                            options=["League"] + sorted(df["team"].dropna().unique().tolist()))
    st.session_state.team = user_team
else:
    user_team = st.session_state.team

title = " League Average Production vs Points"


scatter_plot = display_scatter(df, st.session_state.team, title)

st.plotly_chart(scatter_plot, use_container_width=True)

# Import Logo Library
# Path to the folder containing team logos
image_folder_path = "data/nba_logos/"

# Display the team logo
col5, col6 = st.columns([4, 6])
if st.session_state.team:
    user_team = st.session_state.team
    with col5:
        display_team_logo(user_team, image_folder_path)
    col6.markdown(f'# **{user_team}**')
else:
    st.write("Select a team to view its logo.")



### --------------------------------- Team Production --------------------------------- ###

average_team_shooting_production = round(df[df["team"] == user_team]["shooting_production"].mean(), 2)
average_team_ancillary_production = round(df[df["team"] == user_team]["ancillary_production"].mean(), 2)
average_team_total_production = round(df[df["team"] == user_team]["total_production"].mean(), 2)

col7, col8, col9 = st.columns([1, 1, 1])
col7.metric(label="Average Shooting Production", value=average_team_shooting_production)
col8.metric(label="Average Ancillary Production", value=average_team_ancillary_production)
col9.metric(label="Average Total Production", value=average_team_total_production)

st.write(st.session_state)