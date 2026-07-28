import streamlit as st
import plotly.express as px

def mostrar_graficas(df):

    top = (
        df["DIRECCION_LIMPIA"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    top.columns = ["Dirección", "Servicios"]

    fig = px.bar(
        top,
        x="Servicios",
        y="Dirección",
        orientation="h",
        color="Servicios",
        color_continuous_scale="Viridis",
        title="Top 15 Direcciones con Mayor Demanda"
    )

    fig.update_layout(
        height=550,
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(fig, use_container_width=True)