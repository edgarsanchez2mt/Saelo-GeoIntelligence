from pathlib import Path
import pandas as pd
import folium

from folium.plugins import HeatMap
from folium.plugins import MarkerCluster

# ===========================================
# RUTAS
# ===========================================

BASE = Path(__file__).resolve().parent.parent

archivo = BASE / "resultados" / "coordenadas.xlsx"

carpeta_mapas = BASE / "mapas"
carpeta_mapas.mkdir(exist_ok=True)

salida = carpeta_mapas / "mapa_saelo.html"

# ===========================================
# CARGAR DATOS
# ===========================================

df = pd.read_excel(archivo)

df = df.dropna(subset=["LATITUD", "LONGITUD"])

print("Servicios geocodificados:", len(df))

# ===========================================
# CREAR MAPA
# ===========================================

mapa = folium.Map(
    location=[4.68, -74.08],
    zoom_start=11,
    tiles="CartoDB positron"
)

# ===========================================
# CAPA HEATMAP
# ===========================================

datos_heat = df[["LATITUD", "LONGITUD"]].values.tolist()

HeatMap(
    datos_heat,
    radius=16,
    blur=20,
    min_opacity=0.35
).add_to(mapa)

# ===========================================
# CLUSTERS
# ===========================================

cluster = MarkerCluster(name="Servicios").add_to(mapa)

for _, fila in df.iterrows():

    popup = f"""
    <b>Origen</b><br>
    {fila["DIRECCIÓN ORIGEN"]}
    """

    folium.Marker(
        [fila["LATITUD"], fila["LONGITUD"]],
        popup=popup
    ).add_to(cluster)

# ===========================================
# AEROPUERTO
# ===========================================

folium.Marker(
    [4.70159, -74.1469],
    tooltip="Aeropuerto El Dorado",
    icon=folium.Icon(color="red", icon="plane")
).add_to(mapa)

# ===========================================
# CONTROL DE CAPAS
# ===========================================

folium.LayerControl().add_to(mapa)

# ===========================================
# GUARDAR
# ===========================================

mapa.save(salida)

print("="*60)
print("MAPA GENERADO")
print("="*60)
print(salida)