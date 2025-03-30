# utils/view_data_options.py
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import json
import os
import re


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def drop_max_columns(df):
    # Filter out columns that contain 'max' (case-insensitive)
    columns_to_drop = [col for col in df.columns if '(Max)' or '(MAX)' in col.lower()]
    return df.drop(columns=columns_to_drop)

def drop_percentages(df):
    # Filter out columns that contain 'max' (case-insensitive)
    columns_to_drop = [col for col in df.columns if '(PERCENTAGE)' in col.lower()]
    return df.drop(columns=columns_to_drop)

def remove_null_values(df):
    # Remove rows with null values
    return df.dropna(axis=1)

def replace_nba_abbreviations(data, column=None):
    # NBA abbreviation to full team name mapping
    nba_teams = {
        'ATL': 'Atlanta Hawks',
        'BOS': 'Boston Celtics',
        'BKN': 'Brooklyn Nets',
        'CHA': 'Charlotte Hornets',
        'CHI': 'Chicago Bulls',
        'CLE': 'Cleveland Cavaliers',
        'DAL': 'Dallas Mavericks',
        'DEN': 'Denver Nuggets',
        'DET': 'Detroit Pistons',
        'GSW': 'Golden State Warriors',
        'HOU': 'Houston Rockets',
        'IND': 'Indiana Pacers',
        'LAC': 'Los Angeles Clippers',
        'LAL': 'Los Angeles Lakers',
        'MEM': 'Memphis Grizzlies',
        'MIA': 'Miami Heat',
        'MIL': 'Milwaukee Bucks',
        'MIN': 'Minnesota Timberwolves',
        'NOP': 'New Orleans Pelicans',
        'NYK': 'New York Knicks',
        'OKC': 'Oklahoma City Thunder',
        'ORL': 'Orlando Magic',
        'PHI': 'Philadelphia 76ers',
        'PHX': 'Phoenix Suns',
        'POR': 'Portland Trail Blazers',
        'SAC': 'Sacramento Kings',
        'SAS': 'San Antonio Spurs',
        'TOR': 'Toronto Raptors',
        'UTA': 'Utah Jazz',
        'WAS': 'Washington Wizards',
        'BRK': 'Brooklyn Nets',
        'CHO': 'Charlotte Hornets',
        'PHO': 'Phoenix Suns',
    }

    if isinstance(data, pd.DataFrame) and column:
        data[column] = data[column].map(nba_teams).fillna(data[column])
        return data
    elif isinstance(data, (pd.Series, list)):
        return pd.Series(data).map(nba_teams).fillna(data).tolist()
    else:
        raise ValueError("Provide a DataFrame with a column name, or a list/Series of abbreviations.")


def calculate_home_production(df):
    # Calculate missed shots
    df["FGMI"] = df["FIELD GOALS ATTEMPTED"] - df["FIELD GOALS MADE"]
    df["3PMI"] = df["THREE-POINTERS ATTEMPTED"] - df["THREE-POINTERS MADE"]
    df["FTMI"] = df["FREE THROWS ATTEMPTED"] - df["FREE THROWS MADE"]

    # Shooting Production
    df["FG_PRODUCTION"] = (df["FIELD GOALS MADE"] - df["FGMI"]) * 2
    df["FG3_PRODUCTION"] = (df["THREE-POINTERS MADE"] - df["3PMI"]) * 3
    df["FT_PRODUCTION"] = (df["FREE THROWS MADE"] - df["FTMI"]) * 1
    df["SHOOTING_PRODUCTION"] = df["FG_PRODUCTION"] + df["FG3_PRODUCTION"] + df["FT_PRODUCTION"]

    # Ancillary Production
    df["ANCILLARY_PRODUCTION"] = (
        df["ASSISTS"] * 0.25
        + df["OFFENSIVE REBOUNDS"] * 0.50
        + df["DEFENSIVE REBOUNDS"] * 0.25
        - df["TURNOVERS"] * 0.5
        + df["STEALS"] * 0.5
        + df["BLOCKS"] * 0.5
        - df["PERSONAL FOULS"] * 0.05
    )

    # Total Production
    df["TOTAL_PRODUCTION"] = df["SHOOTING_PRODUCTION"] + df["ANCILLARY_PRODUCTION"]

    # Efficiency
    df["FG_EFFICIENCY"] = df["FIELD GOALS MADE"] / df["FIELD GOALS ATTEMPTED"]
    df["FG3_EFFICIENCY"] = df["THREE-POINTERS MADE"] / df["THREE-POINTERS ATTEMPTED"]
    df["FT_EFFICIENCY"] = df["FREE THROWS MADE"] / df["FREE THROWS ATTEMPTED"]

    return df


def calculate_away_production(df):
    # Calculate missed shots
    df["FGMI_OPP"] = df["FIELD GOALS ATTEMPTED (OPPONENT)"] - df["FIELD GOALS MADE (OPPONENT)"]
    df["3PMI_OPP"] = df["THREE-POINTERS ATTEMPTED (OPPONENT)"] - df["THREE-POINTERS MADE (OPPONENT)"]
    df["FTMI_OPP"] = df["FREE THROWS ATTEMPTED (OPPONENT)"] - df["FREE THROWS MADE (OPPONENT)"]

    # Shooting Production
    df["FG_OPP_PRODUCTION"] = (df["FIELD GOALS MADE (OPPONENT)"] - df["FGMI_OPP"]) * 2
    df["FG3_OPP_PRODUCTION"] = (df["THREE-POINTERS MADE (OPPONENT)"] - df["3PMI_OPP"]) * 3
    df["FT_OPP_PRODUCTION"] = (df["FREE THROWS MADE (OPPONENT)"] - df["FTMI_OPP"]) * 1
    df["SHOOTING_OPP_PRODUCTION"] = (
        df["FG_OPP_PRODUCTION"] + df["FG3_OPP_PRODUCTION"] + df["FT_OPP_PRODUCTION"]
    )

    # Ancillary Production
    df["ANCILLARY_OPP_PRODUCTION"] = (
        df["ASSISTS (OPPONENT)"] * 0.25
        + df["OFFENSIVE REBOUNDS (OPPONENT)"] * 0.50
        + df["DEFENSIVE REBOUNDS (OPPONENT)"] * 0.25
        - df["TURNOVERS (OPPONENT)"] * 0.5
        + df["STEALS (OPPONENT)"] * 0.5
        + df["BLOCKS (OPPONENT)"] * 0.5
        - df["PERSONAL FOULS (OPPONENT)"] * 0.05
    )

    # Total Production
    df["TOTAL_OPP_PRODUCTION"] = df["SHOOTING_OPP_PRODUCTION"] + df["ANCILLARY_OPP_PRODUCTION"]

    # Efficiency
    df["FG_OPP_EFFICIENCY"] = df["FIELD GOALS MADE (OPPONENT)"] / df["FIELD GOALS ATTEMPTED (OPPONENT)"]
    df["FG3_OPP_EFFICIENCY"] = df["THREE-POINTERS MADE (OPPONENT)"] / df["THREE-POINTERS ATTEMPTED (OPPONENT)"]
    df["FT_OPP_EFFICIENCY"] = df["FREE THROWS MADE (OPPONENT)"] / df["FREE THROWS ATTEMPTED (OPPONENT)"]

    return df


def calculate_production(data):
    df = calculate_home_production(data)
    df = calculate_away_production(df)
    return df



def analyze_and_rename_basketball_csv(input_file, output_file):
    df = pd.read_csv(input_file)
    column_list = df.columns.tolist()

    prompt = f"""
    You are a data analyst. Below is a list of column headers from a basketball stats CSV file:

    {column_list}

    Your task:
    - Rename each column to a full, descriptive label.
    - For example, 'fg' should become 'Field Goals Made', 'ast' → 'Assists', etc.
    - If a column contains '_opp', add '(Opponent)' to the new name.
    - If it's a datetime or team-related column, name it appropriately.
    - Return only a JSON dictionary in the format:
    {{ "original_column_name": "New Descriptive Column Name", ... }}
    """

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful CSV data annotator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1000
    )

    # Parse the JSON mapping
    raw_content = response.choices[0].message.content.strip()
    print(raw_content)
    # Clean if wrapped in markdown
    match = re.search(r"\{.*\}", raw_content, re.DOTALL)
    column_mapping = json.loads(match.group()) if match else {}

    updated_df = df.rename(columns=column_mapping)
    updated_df.to_csv(output_file, index=False)

