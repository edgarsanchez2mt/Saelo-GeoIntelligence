import streamlit as st

def mostrar_kpis(df):

    total = len(df)

    geo = df["LATITUD"].notna().sum()

    cobertura = geo / total * 100

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🚖 Servicios", f"{total:,}")

    c2.metric("📍 Geocodificados", f"{geo:,}")

    c3.metric("📈 Cobertura", f"{cobertura:.1f}%")

    c4.metric("🛫 Destino", "El Dorado")