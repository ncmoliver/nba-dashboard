import os
from PIL import Image
import streamlit as st

# Mapping of full team names to their abbreviations
TEAM_NAME_MAPPING = {
    "Atlanta Hawks": "atl",
    "Boston Celtics": "bos",
    "Brooklyn Nets": "bkn",
    "Charlotte Hornets": "cha",
    "Chicago Bulls": "chi",
    "Cleveland Cavaliers": "cle",
    "Dallas Mavericks": "dal",
    "Denver Nuggets": "den",
    "Detroit Pistons": "det",
    "Golden State Warriors": "gsw",
    "Houston Rockets": "hou",
    "Indiana Pacers": "ind",
    "Los Angeles Clippers": "lac",
    "Los Angeles Lakers": "lal",
    "Memphis Grizzlies": "mem",
    "Miami Heat": "mia",
    "Milwaukee Bucks": "mil",
    "Minnesota Timberwolves": "min",
    "New Orleans Pelicans": "nop",
    "New York Knicks": "nyk",
    "Oklahoma City Thunder": "okc",
    "Orlando Magic": "orl",
    "Philadelphia 76ers": "phi",
    "Phoenix Suns": "phx",
    "Portland Trail Blazers": "por",
    "Sacramento Kings": "sac",
    "San Antonio Spurs": "sas",
    "Toronto Raptors": "tor",
    "Utah Jazz": "uta",
    "Washington Wizards": "was"
}

def display_team_logo(selected_team, image_folder_path):
    """
    Displays the logo of the selected team.

    Args:
        selected_team (str): The name of the selected team.
        image_folder_path (str): The path to the folder containing team logo images.

    Returns:
        None
    """
    col5, _ = st.columns([1, 4])  # Create a column for the logo display

    if selected_team != "League":
        # Get the abbreviation for the selected team
        team_abbreviation = TEAM_NAME_MAPPING.get(selected_team, None)
        
        if team_abbreviation:
            # Construct the image file path
            image_file = os.path.join(image_folder_path, f"{team_abbreviation}.png")
            print(image_file)
            # Check if the image file exists
            if os.path.exists(image_file):
                # Load and display the image
                image = Image.open(image_file)
                col5.image(image, width=500)
            else:
                col5.write(f"Logo for {selected_team} not found.")
        else:
            col5.write(f"Team abbreviation for {selected_team} not found.")
    else:
        col5.write("Select a team to view its logo.")

