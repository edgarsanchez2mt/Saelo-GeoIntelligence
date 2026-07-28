import streamlit as st

def mostrar_sidebar(df):

    st.sidebar.image("dashboard/assets/logo_saelo.png", width=180)

    st.sidebar.title("Filtros")

    años = ["Todos"]

    if "FECHA" in df.columns:
        años += sorted(
            df["FECHA"].dt.year.dropna().astype(int).unique().tolist()
        )

    año = st.sidebar.selectbox("Año", años)

    return año