import pandas as pd
import streamlit as st
import re


def calculate_ms(ms, sequence) -> (float, float):
    try:

        delimiter_count = sequence.count("(")
        delimiter_count += sequence.count(")")

        if delimiter_count < 2:
            return calculate_sequence_ms(ms, sequence)

        else:

            unusual_list, sequence = extract_unusual_aa(sequence, delimiter_count)

            sum_mono, sum_avg = calculate_sequence_ms(ms, sequence)

            for unusual_aa in unusual_list:
                unusual_ms = ms[ms["character"] == unusual_aa].reset_index()
                if unusual_ms.empty:
                    raise ValueError(f"Error: Could not find {unusual_aa} in the list."
                                     f"Please add {unusual_aa} to the list or choose an existing unusual amino acid.")
                else:
                    sum_mono += unusual_ms["mono"][0]
                    sum_avg += unusual_ms["avg"][0]

            return sum_mono, sum_avg

    except ValueError as ex:
        raise


def calculate_sequence_ms(ms, sequence) -> (float, float):
    sum_mono: float = 0
    sum_avg: float = 0

    for char in sequence.upper():
        temp_ms_df = ms[ms["character"] == char].reset_index()
        if temp_ms_df.empty:
            raise ValueError(f"Error: {char} is not a valid natural amino acid")
        else:
            sum_mono = sum_mono + temp_ms_df["mono"][0]
            sum_avg = sum_avg + temp_ms_df["avg"][0]

    return sum_mono, sum_avg


def calculate_total_ms(sum_ms: float, c_ms: float, n_ms: float) -> float:
    return sum_ms + c_ms + n_ms


def extract_unusual_aa(sequence: str, delimiter_count: int):
    unusual_list = []

    for delimiter in range(0, delimiter_count, 2):
        start = sequence.find("(")
        end = sequence.find(")")
        unusual_list.append(sequence[start + 1:end])
        sequence = sequence[0:start] + sequence[end + 1:]
    return unusual_list, sequence


def calc_fragmentation(ms_type: float):
    frag_ms_df = pd.DataFrame(columns=["charge", "m/z"])
    for charge in range(1, 11, 1):
        frag_ms_df = frag_ms_df.append({"charge": f"+{charge}", "m/z": (ms_type + charge) // charge}, ignore_index=True)
    return frag_ms_df
