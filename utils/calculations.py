# utils/calculations.py



def calculate_home_production(df):
    # Shooting Production Calculations
    #Calculate missed shots

    df['fgmi'] = df['fga'] - df['fg']
    df['3pmi'] = df['3pa'] - df['3p']
    df['ftmi'] = df['fta'] - df['ft']

    df['fg_production'] = (df['fg'] - df['fgmi']) * 2
    df['fg3_production'] = (df['3p'] - df['3pmi']) * 3
    df['ft_production'] = (df['ft'] - df['ftmi']) * 1

    # Ancillary Production
    key_number = 1  # Adjust this as needed
    df['ancillary_production'] = ((df['ast'] * .25) + (df['orb'] *.50) + (df['drb'] *.25) - (df['tov'] * .5)
                                  + (df['stl'] * .5) + (df['blk'] * .5) - (df['pf'] * .05))

    #Shooting Production
    # Shooting Production
    df['shooting_production'] = df['fg_production'] + df['fg3_production'] + df['ft_production']

    # Total Production
    df['total_production'] = (df['shooting_production'] + df['ancillary_production'])

    # Efficiency and Effectiveness
    df['fg_efficiency'] = df['fg'] / df['fga']
    df['fg3_efficiency'] = df['3p'] / df['3pa']
    df['ft_efficiency'] = df['ft'] / df['fta']

    return df


def calculate_away_production(df):
    # Shooting Production Calculations
    #Calculate missed shots

    df['fgmi_opp'] = df['fga_opp'] - df['fg_opp']
    df['3pmi_opp'] = df['3pa_opp'] - df['3p_opp']
    df['ftmi_opp'] = df['fta_opp'] - df['ft_opp']

    df['fg_opp_production'] = (df['fg_opp'] - df['fgmi_opp']) * 2
    df['fg3_opp_production'] = (df['3p_opp'] - df['3pmi_opp']) * 3
    df['ft_opp_production'] = (df['ft_opp'] - df['ftmi_opp']) * 1

    # Shooting Production
    df['shooting_opp_production'] = df['fg_opp_production'] + df['fg3_opp_production'] + df['ft_opp_production']

    # Ancillary Production
    key_number = 1  # Adjust this as needed
    df['ancillary_opp_production'] = ((df['ast_opp'] * .25) + (df['orb_opp'] *.50) + (df['drb_opp'] *.25) - (df['tov_opp'] * .5)
                                  + (df['stl_opp'] * .5) + (df['blk_opp'] * .5) - (df['pf_opp'] * .05))

    # Total Production
    df['total_opp_production'] = (df['shooting_opp_production']+ df['ancillary_opp_production'])

    # Efficiency and Effectiveness
    df['fg_opp_efficiency'] = df['fg_opp'] / df['fga_opp']
    df['fg3_opp_efficiency'] = df['3p_opp'] / df['3pa_opp']
    df['ft_opp_efficiency'] = df['ft_opp'] / df['fta_opp']

    return df




    
def calculate_production(df):
    df = calculate_home_production(df)
    df = calculate_away_production(df)
    return df