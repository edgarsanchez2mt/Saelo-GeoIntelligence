from pathlib import Path
import pandas as pd
import streamlit as st

BASE = Path(__file__).resolve().parents[2]

ARCHIVO = BASE / "resultados" / "coordenadas.xlsx"

@st.cache_data
def cargar_datos():

    df = pd.read_excel(ARCHIVO)

    return df