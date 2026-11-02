from pathlib import Path

import pandas as pd
import streamlit as st

@st.cache_data
def load_data(path="data/clean/dataset.csv"):
    """Lê o dataset tratado e reutiliza os dados entre interações."""
    raiz = Path(__file__).resolve().parent.parent

    return pd.read_csv(raiz / path)
