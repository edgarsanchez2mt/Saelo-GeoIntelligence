import folium
from folium.plugins import HeatMap, MarkerCluster, Fullscreen
from streamlit_folium import st_folium

def mostrar_mapa(df):

    df = df.dropna(subset=["LATITUD", "LONGITUD"])

    mapa = folium.Map(
        location=[4.68, -74.08],
        zoom_start=11,
        tiles="CartoDB positron"
    )

    # HeatMap
    HeatMap(
        df[["LATITUD", "LONGITUD"]].values.tolist(),
        radius=18,
        blur=22,
        min_opacity=0.30
    ).add_to(mapa)

    # Cluster de servicios
    cluster = MarkerCluster(name="Servicios")

    for _, fila in df.iterrows():

        popup = f"""
        <b>Dirección</b><br>
        {fila["DIRECCION_LIMPIA"]}
        """

        folium.CircleMarker(
            location=[fila["LATITUD"], fila["LONGITUD"]],
            radius=3,
            color="#39FF14",
            fill=True,
            fill_opacity=0.7,
            popup=popup
        ).add_to(cluster)

    cluster.add_to(mapa)

    # Aeropuerto
    folium.Marker(
        [4.7016, -74.1469],
        tooltip="Aeropuerto El Dorado",
        icon=folium.Icon(color="red", icon="plane")
    ).add_to(mapa)

    # Pantalla completa
    Fullscreen().add_to(mapa)

    folium.LayerControl().add_to(mapa)

    st_folium(
        mapa,
        use_container_width=True,
        height=700
    )