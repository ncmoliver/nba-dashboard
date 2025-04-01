from datasets import load_dataset
import pandas as pd
import streamlit as st


@st.cache_data
def load_data(dataset_name):
  dataset = load_dataset(dataset_name)
  dataset = pd.DataFrame(dataset['train'])
  return dataset

def recreate_dataframe(df, selected_columns):
    df = df[selected_columns]
    return df

def get_metrics(df, player):
    shooting_production = round(df[df['PLAYER'] == player]['shooting_production'].values[0] , 2)
    ancillary_production = round(df[df['PLAYER'] == player]['ancillary_production'].values[0], 2)
    total_production = round(df[df['PLAYER'] == player]['total_production'].values[0], 2)
    return shooting_production, ancillary_production, total_production