import numpy as np

def evaluate_production(df):
    df['home_result'] = np.where(df['total_production'] > df['total_opp_production'], "True", "False")

    df['won'] = df['won'].replace({'True': True, 'False': False})
    df['home_result'] = df['home_result'].replace({'True': True, 'False': False})

    return df

def compare_results(df):
    df['result_match'] = np.where(df['home_result'] == df['won'], "pass", "fail")
    return df

def calculate_win_loss(df):
    num_pass = len(df[df['result_match'] == 'pass'])
    num_total = len(df)

    if num_total == 0:
        return float('inf') if num_pass > 0 else 0 # Handle the case where there are no fails. If there are passes, then the ratio is infinity. If there are no passes either, then the ratio is 0.
    else:
        win_loss_ratio = num_pass / num_total
        return win_loss_ratio