from pathlib import Path
import streamlit as st

BASE = Path(__file__).resolve().parents[1]
LOGO = BASE / "assets" / "logo_saelo.png"

def mostrar_header():

    col1, col2 = st.columns([1,4])

    with col1:
        st.image(str(LOGO), width=170)

    with col2:
        st.markdown(
            """
            <h1 style='margin-bottom:0;color:#39FF14;'>
            SAELO GEO INTELLIGENCE
            </h1>

            <h4 style='margin-top:0;color:#A020F0;'>
            Inteligencia Geográfica para Transporte Especial
            </h4>
            """,
            unsafe_allow_html=True
        )

    st.divider()