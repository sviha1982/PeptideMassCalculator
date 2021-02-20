import pandas as pd

def calculate_ms(mono, sequence) -> float:
    sum_mono: float = 0
    for char in sequence.upper():
        temp_mono_df = mono[mono["character"] == char].reset_index()
        sum_mono = sum_mono + temp_mono_df["mono"][0]

    return sum_mono

def calculate_total_mono(sum_mono: float, c_mono: float, n_mono: float) -> float:
    return sum_mono + c_mono["mono"][0] + n_mono["mono"][0]
