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


def validate_input(df, user_input: str, column: str):
    try:
        if len(user_input) == 0:
            raise ValueError("Error: User input should not be empty.")

        temp_splits = user_input.split(",")
        name = temp_splits[0]
        mono = temp_splits[1]
        avg = temp_splits[2]
        description = temp_splits[3]

        mono = float(mono)
        avg = float(avg)
        description = str(description)

        if len(name) < 2:
            raise ValueError("Error: User input too short. Please enter at least 2 characters.")
        if len(name) > 20:
            raise ValueError("Error: User input too long. Please enter no more than 20 characters.")

        duplicate_check = df[df[column] == name]

        if not duplicate_check.empty:
            name = duplicate_check[column][0]
            mono = duplicate_check["mono"][0]
            avg = duplicate_check["avg"][0]

        else:
            df = save_new_entry(df, column, name, mono, avg, description)

        return mono, avg, df


    except ValueError as ex:
        raise


def save_new_entry(df, column: str, name: str, mono: float, avg: float, description: str):
    if len(df.columns) == 3:
        df = df.append({f"{column}": name, "mono": mono, "avg": avg}, ignore_index=True)
        df.to_csv(os.path.join("data", f"{column}.csv"), index=True)
    else:
        df = df.append({f"{column}": name, "mono": mono, "avg": avg, "description": description}, ignore_index=True)
        df.to_csv(os.path.join("data", f"{column}.csv"), index=True)

    return df


def get_ms(df, user_input: str, column: str):
    predefined_ms = df[df[column] == user_input].reset_index()
    mono_ms = predefined_ms["mono"][0]
    avg_ms = predefined_ms["avg"][0]
    return mono_ms, avg_ms
