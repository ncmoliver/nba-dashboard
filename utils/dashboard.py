import streamlit as st
from utils.functions import load_data, recreate_dataframe, get_metrics
from utils.view_data_option import replace_nba_abbreviations
from utils.calculations import calculate_production
from utils.display_scatterplot import display_scatter
from utils.display_team_logo import display_team_logo
from utils.fetch_data import get_team_data
from utils.display_barchart import create_player_vs_team_chart
import pandas as pd
import plotly.graph_objects as go



def display_dashboard():
    st.set_page_config(layout="wide")

    if "data" not in st.session_state:
        st.session_state.data = load_data("data/nba_team_stats.csv")
    data = st.session_state.data
    if data.empty:
        st.error("The data could not be loaded or is empty. Please check the data source.")
        return
    if "league_checkb" not in st.session_state:
        st.session_state.league_checkb = False


    column1, column2= st.columns([2, 1])
    column1.markdown("<h2 style-'text-align: center;'>B A S K E T B A L L | E X P L A I N E D</h2>", unsafe_allow_html=True)
    
    # Select a season
    years = ["All"] + st.session_state.data['season'].unique().tolist()
    selected_year = column2.selectbox("Select a season", options=years, key="selected_year")

    # Validate if a year is selected
    if not selected_year:
        st.warning("Please select a season to proceed.")
        return

    # Filter data by the selected year
    data = calculate_production(data)
    selected_columns = ["season", "team", "fg", "fga", "fgmi", "3p", "3pa", "3pmi", "ft", "fta", "ftmi", "ast", "orb", "drb", "tov", "stl", "blk", "pf", "pts", "fg_efficiency", "ft_efficiency", "total_production", "shooting_production", "ancillary_production", "team_opp", "fg_opp", "fga_opp", "fgmi_opp", "3p_opp", "3pa_opp", "3pmi_opp", "ft_opp", "fta_opp", "ftmi_opp", "ast_opp", "orb_opp", "drb_opp", "tov_opp", "stl_opp", "blk_opp", "pf_opp", "pts_opp", "fg_opp_efficiency", "ft_opp_efficiency", "total_opp_production", "shooting_opp_production", "ancillary_opp_production"]
    data = recreate_dataframe(data, selected_columns)
    data = replace_nba_abbreviations(data, column="team")
    data = replace_nba_abbreviations(data, column="team_opp")

    if selected_year != "All":
        data_by_year = data[data['season'] == selected_year]
    else:
        data_by_year = data

    if "selected_year_data" not in st.session_state:
        st.session_state.selected_year_data = data_by_year

    st.markdown("---")

    # Average League Production
    cola, colb = st.columns([1, 3])
    cola.checkbox(label="Hide League Metrics", key="league_checkb", label_visibility="collapsed")
    colb.markdown("### Average League Production")
    
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


    title = f"{selected_year if selected_year != 'All' else 'All Seasons'} League Average Production vs Points"
    scatter_plot = display_scatter(data_by_year, user_team, title)
    st.plotly_chart(scatter_plot, use_container_width=True)

    st.markdown("---")

    # Display Team Logo
    image_folder_path = "data/nba_logos/"
    col5, col6, col7 = st.columns([3, 5, 2])
    if user_team and user_team != "League":
        with col5:
            display_team_logo(user_team, image_folder_path)
        col6.markdown(f'# **{selected_year} {user_team}**')
    else:
        st.write("Select a team to view its logo.")

    # Team Production Metrics
    if user_team and user_team != "League":
        average_team_shooting_production = round(data_by_year[data_by_year["team"] == user_team]["shooting_production"].mean(), 2)
        average_team_ancillary_production = round(data_by_year[data_by_year["team"] == user_team]["ancillary_production"].mean(), 2)
        average_team_total_production = round(data_by_year[data_by_year["team"] == user_team]["total_production"].mean(), 2)

        shooting_difference = round(average_team_shooting_production - average_shooting_production, 2)
        ancillary_difference = round(average_team_ancillary_production - average_ancillary_production, 2)
        total_difference = round(average_team_total_production - average_total_production, 2)

        col5.markdown("---")
        col5.metric(label="Average Shooting Production", value=average_team_shooting_production, delta=shooting_difference)
        col5.markdown("---")
        col5.metric(label="Average Ancillary Production", value=average_team_ancillary_production, delta=ancillary_difference)
        col5.markdown("---")
        col5.metric(label="Average Total Production", value=average_team_total_production, delta=total_difference)
        col5.markdown("---")

    # Check if the selected team and year are in the session state
    if "playerData" not in st.session_state:
        player_data = pd.read_csv("data/nba_new.csv")
        st.session_state.playerData = player_data

    player_data = st.session_state.playerData

    # Validate if player data exists for the selected team
    if player_data[player_data["Team"] == user_team].empty:
        st.warning(f"No player data available for {user_team} in {selected_year}.")
        return

    col6.selectbox(label="Choose A Player", options=player_data[player_data["Team"] == user_team]["PLAYER"].unique(), key="player")
    col7.selectbox(label="(inactive..developing feature)", options=["Player Analysis", "Shooting Analysis", "Ancillary Analysis", "Total Production Analysis"], key="team_analysis")
    col7.markdown("---")
    condensed_players = get_team_data(player_data, user_team, selected_year)

    # Validate if a player is selected
    if "player" not in st.session_state or not st.session_state.player:
        st.warning("Please select a player to view their metrics.")
        return

    with col7:
        st.markdown("### Player Season Metrics")
        if st.session_state.player in condensed_players['PLAYER'].values:
            shooting, ancillary, total = get_metrics(condensed_players, st.session_state.player)
            st.metric(label="Shooting Production", value=shooting)
            st.metric(label="Ancillary Production", value=ancillary)
            st.metric(label="Total Production", value=total)
        else:
            st.warning(f"No metrics available for the selected player: {st.session_state.player}.")

        # Create and display the player vs team chart
        metrics = ["shooting_production", "ancillary_production", "total_production"]
        try:
            player_vs_team_chart = create_player_vs_team_chart(st.session_state.player, condensed_players, metrics)
            col6.plotly_chart(player_vs_team_chart, use_container_width=True)
        except ValueError as e:
            col6.warning(str(e))


    st.markdown(
        "<h6 style='text-align: center;'> 🕋 Built with Streamlit by Marques Oliver</h6>",
        unsafe_allow_html=True
        )
