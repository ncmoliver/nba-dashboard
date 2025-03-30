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
