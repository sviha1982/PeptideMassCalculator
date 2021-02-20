import streamlit as st
import pandas as pd
import numpy as np
from file_handler import load_df, create_data, validate_input, load_cache_df, get_ms
from calculations import calculate_ms, calculate_total_mono
import os

aa_mass_df = load_cache_df("aa_residues.csv")
n_option_df = load_df("n-option.csv")
c_option_df = load_df("c-option.csv")
sequence = st.text_input("One-character symbols are used for natural amino acids and numbers for other residues",
                         "")
#col1, col2 = st.beta_columns(2)
n_mono = None
n_option = st.selectbox("Select N-terminal group", n_option_df["n-option"])
if n_option == "other":
    n_input = st.text_input("Type name, monoisotopic and average mass (e.g. Boc, 101.0603, 101.1250)")
    n_mono = validate_input(n_option_df, n_input, "n-option")

else:
    n_mono = get_ms(n_option_df, n_option, "n-option")

c_mono = None
c_option = st.selectbox("Select C-terminal group", c_option_df["c-option"])
if c_option == "other":
    c_input = st.text_input("Type name, monoisotopic and average mass (e.g. Boc, 101.0603, 101.1250)")
    c_mono = validate_input(c_option_df, c_input, "c-option")

else:
    c_mono = get_ms(c_option_df, c_option, "c-option")

    #TODO extract value from return also for n-option
#TODO: figure out how to get selectbox in 2 columns

if n_mono is None or c_mono is None:
    st.write("value is None")

else:
    mono_ms, avg_ms = create_data(aa_mass_df)
    sum_mono = calculate_ms(mono_ms, sequence)
    st.write(calculate_total_mono(sum_mono, n_mono, c_mono))

