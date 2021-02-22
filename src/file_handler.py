import pandas as pd
import streamlit as st
import os
from pathlib import Path

@st.cache
def load_cache_df(file_name: str):
    return pd.read_csv(os.path.join("data", file_name), index_col=0)


def load_df(file_name: str):
    return pd.read_csv(os.path.join("data", file_name), index_col=0)


@st.cache
def create_data(df):
    mono_ms_df = df[["character", "mono"]]
    avg_ms_df = df[["character", "avg"]]
    return mono_ms_df, avg_ms_df

def validate_input(df, user_input: str, column:str):

    try:
        if len(user_input) == 0:
            return None, None, None

        temp_splits = user_input.split(",")
        name = temp_splits[0]
        mono = temp_splits[1]
        avg = temp_splits[2]

        mono = float(mono)
        avg = float(avg)

        if len(name) < 2:
            return None, None, None
        if len(name) > 20:
            return None, None, None

        duplicate_check = df[df[column] == name]

        if not duplicate_check.empty:
            name = duplicate_check[column][0]
            mono = duplicate_check["mono"][0]
            avg = duplicate_check["avg"][0]

        else:
            df = save_new_entry(df, column, name, mono, avg)




        return mono, avg, df


    except BaseException as ex:
        return ex


def save_new_entry(df, column: str, name: str, mono: float, avg: float):
    df = df.append({f"{column}": name, "mono": mono, "avg": avg}, ignore_index=True)
    df.to_csv(os.path.join("data", f"{column}.csv"), index=True)
    return df

def get_ms(df, user_input: str, column: str):
    predefined_ms = df[df[column] == user_input].reset_index()
    mono_ms = predefined_ms["mono"][0]
    avg_ms = predefined_ms["avg"][0]
    return mono_ms, avg_ms


