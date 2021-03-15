import streamlit as st
import pandas as pd
import numpy as np
from file_handler import load_df, create_data, validate_input, load_cache_df, get_ms
from calculations import calculate_ms, calculate_total_ms
import os
import math

aa_mass_df = load_cache_df("character.csv")
n_option_df = load_df("n-option.csv")
c_option_df = load_df("c-option.csv")

sequence = st.text_input("One-character symbols are used for natural amino acids and numbers for other residues",
                         "")
if sequence == "":
    st.write("insert sequence")

u_mono = None
U_avg = None
if st.checkbox("show unnatural amino acids"):
    st.write(aa_mass_df[19:-1])
    unnatural = st.text_input("Add unnatural amino acid", "")
    if unnatural is not None:
        u_mono, u_avg, aa_mass_df = validate_input(aa_mass_df, unnatural, "character")
    else:
        st.write("Type name, monoisotopic and average mass (e.g. Any, 101.0603, 101.1250")

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


if math.isnan(n_mono) or math.isnan(c_mono) or sequence == "":
   st.write("Insert values")

else:
    mono_ms_df, avg_ms_df = create_data(aa_mass_df)
    sum_mono, sum_avg = calculate_ms(aa_mass_df, sequence)



    st.write("monoisotopic mass:", "{:12.4f}".format(calculate_total_ms(sum_mono, n_mono, c_mono)))
    st.write("average mass:", "{:12.4f}".format(calculate_total_ms(sum_avg, n_avg, c_avg)))
