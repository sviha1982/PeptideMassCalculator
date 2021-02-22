import pandas as pd
import streamlit as st

def calculate_ms(ms, sequence, ms_type: str) -> float:
    sum_ms: float = 0

    for char in sequence.upper():
        temp_ms_df = ms[ms["character"] == char].reset_index()
        sum_ms = sum_ms + temp_ms_df[ms_type][0]

    return sum_ms

def calculate_total_ms(sum_ms: float, c_ms: float, n_ms: float, ms_type) -> float:
    return sum_ms + c_ms + n_ms
