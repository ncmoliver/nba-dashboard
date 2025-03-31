# utils/view_data_options.py
import pandas as pd


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
