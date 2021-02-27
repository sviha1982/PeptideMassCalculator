import streamlit as st
import pandas as pd
import numpy as np
from file_handler import load_df, create_data, validate_input, load_cache_df, get_ms
from calculations import calculate_ms, calculate_total_ms
import os

aa_mass_df = load_cache_df("aa_residues.csv")
n_option_df = load_df("n-option.csv")
c_option_df = load_df("c-option.csv")
sequence = st.text_input("One-character symbols are used for natural amino acids and numbers for other residues",
                         "")
col_n, col_c = st.beta_columns(2)
n_mono = None
n_avg = None
n_option = col_n.selectbox("Select N-terminal group", n_option_df["n-option"])

if n_option == "other":
    n_input = col_n.text_input("Type name, monoisotopic and average mass (e.g. Boc, 101.0603, 101.1250)")
    if n_input is not None:
        n_mono, n_avg, n_option_df = validate_input(n_option_df, n_input, "n-option")

else:
    n_mono, n_avg = get_ms(n_option_df, n_option, "n-option")

c_mono = None
c_avg = None
c_option = col_c.selectbox("Select C-terminal group", c_option_df["c-option"])

if c_option == "other":
    c_input = col_c.text_input("Type name, monoisotopic and average mass (e.g. egal, 101.0603, 101.1250)")
    if c_input is not None:
        c_mono, c_avg, c_option_df = validate_input(c_option_df, c_input, "c-option")

else:
    c_mono, c_avg = get_ms(c_option_df, c_option, "c-option")


#TODO: figure out how to get selectbox in 2 columns

if n_mono is None or c_mono is None:
   st.write("Insert values")

else:
    mono_ms_df, avg_ms_df = create_data(aa_mass_df)
    sum_mono = calculate_ms(mono_ms_df, sequence, "mono")
    sum_avg = calculate_ms(avg_ms_df, sequence, "avg")

    st.write("monoisotopic mass:", "{:12.4f}".format(calculate_total_ms(sum_mono, n_mono, c_mono, "mono")))
    st.write("average mass:", "{:12.4f}".format(calculate_total_ms(sum_avg, n_avg, c_avg, "avg")))
