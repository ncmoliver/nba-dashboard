import streamlit as st
from utils.functions import load_data, recreate_dataframe
from utils.view_data_option import replace_nba_abbreviations
from utils.calculations import calculate_production
from utils.display_scatterplot import display_scatter
from utils.display_team_logo import display_team_logo

def display_dashboard():
    st.set_page_config(layout="wide")

    if "data" not in st.session_state:
        st.session_state.data = load_data("KDAM1/BasketballGames")
    data = st.session_state.data
    if "league_checkb" not in st.session_state:
        st.session_state.league_checkb = False

    st.title("🏀NBA Dashboard")

    # Select a season
    years = st.session_state.data['season'].unique()
    selected_year = st.selectbox("Select a season", label_visibility="collapsed", options=years)

    # Filter data by the selected year
    data = calculate_production(data)
    selected_columns = ["season", "team", "fg", "fga", "fgmi", "3p", "3pa", "3pmi", "ft", "fta", "ftmi", "ast", "orb", "drb", "tov", "stl", "blk", "pf", "pts", "fg_efficiency", "ft_efficiency", "total_production", "shooting_production", "ancillary_production", "team_opp", "fg_opp", "fga_opp", "fgmi_opp", "3p_opp", "3pa_opp", "3pmi_opp", "ft_opp", "fta_opp", "ftmi_opp", "ast_opp", "orb_opp", "drb_opp", "tov_opp", "stl_opp", "blk_opp", "pf_opp", "pts_opp", "fg_opp_efficiency", "ft_opp_efficiency", "total_opp_production", "shooting_opp_production", "ancillary_opp_production"]
    data = recreate_dataframe(data, selected_columns)
    data = replace_nba_abbreviations(data, column="team")
    data = replace_nba_abbreviations(data, column="team_opp")
    data_by_year = data[data['season'] == selected_year]

    if "selected_year_data" not in st.session_state:
        st.session_state.selected_year_data = data_by_year

    with st.expander("View Sample Data"):
        st.write(data_by_year.head())

    st.markdown("---")

    # Average League Production
    st.markdown("### Average League Production")
    st.sidebar.markdown("### Dashboard Toolbar")
    st.sidebar.checkbox(label="Hide League Metrics", key="league_checkb")

    if not st.session_state.league_checkb:
        average_shooting_production = round(data_by_year["shooting_production"].mean(), 2)
        average_ancillary_production = round(data_by_year["ancillary_production"].mean(), 2)
        average_total_production = round(data_by_year["total_production"].mean(), 2)

        col1, col2, col3 = st.columns([1, 1, 1])
        col1.metric(label="Average Shooting Production", value=average_shooting_production)
        col2.metric(label="Average Ancillary Production", value=average_ancillary_production)
        col3.metric(label="Average Total Production", value=average_total_production)

    st.markdown("---")

    # Team Selection and Scatter Plot
    user_team = st.selectbox(
        "Select a team",
        label_visibility="collapsed",
        options=["League"] + sorted(data_by_year["team"].dropna().unique().tolist()),
        key="team"
    )

    title = f"{selected_year} League Average Production vs Points"
    scatter_plot = display_scatter(data_by_year, user_team, title)
    st.plotly_chart(scatter_plot, use_container_width=True)

    st.markdown("---")

    # Display Team Logo
    image_folder_path = "data/nba_logos/"
    col5, col6 = st.columns([3, 10])
    if user_team and user_team != "League":
        with col5:
            display_team_logo(user_team, image_folder_path)
        col6.markdown(f'# **{user_team}**')
    else:
        st.write("Select a team to view its logo.")

    # Team Production Metrics
    if user_team and user_team != "League":
        average_team_shooting_production = round(data_by_year[data_by_year["team"] == user_team]["shooting_production"].mean(), 2)
        average_team_ancillary_production = round(data_by_year[data_by_year["team"] == user_team]["ancillary_production"].mean(), 2)
        average_team_total_production = round(data_by_year[data_by_year["team"] == user_team]["total_production"].mean(), 2)

        shooting_difference = round(average_team_shooting_production - average_shooting_production,2)
        ancillary_difference = round(average_team_ancillary_production - average_ancillary_production, 2)
        total_difference = round(average_team_total_production - average_total_production, 2)

        col5.markdown("---")
        col5.metric(label="Average Shooting Production", value=average_team_shooting_production, delta=shooting_difference)
        col5.markdown("---")
        col5.metric(label="Average Ancillary Production", value=average_team_ancillary_production, delta=ancillary_difference)
        col5.markdown("---")
        col5.metric(label="Average Total Production", value=average_team_total_production, delta=total_difference)
        col5.markdown("---")

    