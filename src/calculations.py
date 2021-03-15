import pandas as pd
import streamlit as st
import re

def calculate_ms(ms, sequence) -> (float, float):
    sum_mono: float = 0
    sum_avg: float = 0

    delimiter_list = [s.start() for s in re.finditer('$', sequence)]
    for delimiter in range(0,len(delimiter_list),2):
        start = delimiter
        end = delimiter +1
        sub_sequence = sequence[start:end]
        unusual_ms = ms[ms["character"] == sub_sequence].reset_index()

        if unusual_ms.empty:
            continue

        sum_mono += unusual_ms["mono"][0]
        sum_avg += unusual_ms["avg"][0]

    for delimiter in range(0,len(delimiter_list),2):
        start = delimiter
        end = delimiter +1
        if len(sequence) >= end:
            sequence = sequence[0: start:] + sequence[end + 1::]

    for char in sequence.upper():
        temp_ms_df = ms[ms["character"] == char].reset_index()
        sum_mono = sum_mono + temp_ms_df["mono"][0]
        sum_avg = sum_avg + temp_ms_df["avg"][0]

    return sum_mono, sum_avg

def calculate_total_ms(sum_ms: float, c_ms: float, n_ms: float) -> float:
        return sum_ms + c_ms + n_ms
