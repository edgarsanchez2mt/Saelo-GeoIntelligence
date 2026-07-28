import streamlit as st

from utils.cargar_datos import cargar_datos
from components.header import mostrar_header
from components.sidebar import mostrar_sidebar
from components.kpis import mostrar_kpis
from components.mapa import mostrar_mapa
from components.graficas import mostrar_graficas

st.set_page_config(
    page_title="Saelo Geo Intelligence",
    page_icon="🛰️",
    layout="wide"
)

df = cargar_datos()

año = mostrar_sidebar(df)

if año != "Todos":
    df = df[df["FECHA"].dt.year == año]

mostrar_header()

mostrar_kpis(df)

st.divider()

mostrar_mapa(df)

st.divider()

mostrar_graficas(df)

st.divider()

st.subheader("Mapa de Operación")

mostrar_mapa(df)

st.divider()

st.subheader("Análisis de Demanda")

mostrar_graficas(df)