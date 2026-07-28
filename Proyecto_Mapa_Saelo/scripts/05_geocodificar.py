from pathlib import Path
import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm

# ==========================================================
# PROYECTO MAPA DE CALOR SAELO
# GEOCODIFICADOR PROFESIONAL
# ==========================================================

BASE = Path(__file__).resolve().parent.parent

archivo_direcciones = BASE / "resultados" / "direcciones_unicas.xlsx"
archivo_salida = BASE / "resultados" / "coordenadas.xlsx"

# ----------------------------------------------------------
# Leer direcciones
# ----------------------------------------------------------

df = pd.read_excel(archivo_direcciones)

# Normalizar nombre de la columna
df.columns = [c.strip().upper() for c in df.columns]
columna = df.columns[0]

# ----------------------------------------------------------
# Si ya existe un archivo anterior lo continúa
# ----------------------------------------------------------

if archivo_salida.exists():

    print("\nEncontré un archivo de coordenadas anterior.")
    print("Continuando desde el último registro...\n")

    anterior = pd.read_excel(archivo_salida)

    df = df.merge(
        anterior,
        on=columna,
        how="left"
    )

else:

    df["LATITUD"] = None
    df["LONGITUD"] = None
    df["ESTADO"] = None

# ----------------------------------------------------------
# Configuración OpenStreetMap
# ----------------------------------------------------------

geolocator = Nominatim(
    user_agent="saelo_geocoder"
)

geocode = RateLimiter(
    geolocator.geocode,
    min_delay_seconds=1.1
)

# ----------------------------------------------------------
# Contadores
# ----------------------------------------------------------

exitos = 0
errores = 0

print("="*60)
print("INICIANDO GEOCODIFICACIÓN")
print("="*60)

# ----------------------------------------------------------
# Recorrer direcciones
# ----------------------------------------------------------

for i in tqdm(df.index):

    # Saltar registros ya procesados
    if pd.notnull(df.loc[i, "LATITUD"]):
        continue

    direccion = str(df.loc[i, columna]).strip()

    consulta = direccion + ", Bogotá, Colombia"

    try:

        location = geocode(consulta)

        if location:

            df.loc[i, "LATITUD"] = location.latitude
            df.loc[i, "LONGITUD"] = location.longitude
            df.loc[i, "ESTADO"] = "OK"

            exitos += 1

        else:

            df.loc[i, "ESTADO"] = "NO ENCONTRADA"

            errores += 1

    except Exception:

        df.loc[i, "ESTADO"] = "ERROR"

        errores += 1

    # Guardar cada 20 registros
    if i % 20 == 0:

        df.to_excel(
            archivo_salida,
            index=False
        )

# ----------------------------------------------------------
# Guardar resultado final
# ----------------------------------------------------------

df.to_excel(
    archivo_salida,
    index=False
)

print("\n")

print("="*60)
print("PROCESO FINALIZADO")
print("="*60)

print(f"Direcciones procesadas : {len(df):,}")
print(f"Geocodificadas         : {(df['ESTADO']=='OK').sum():,}")
print(f"No encontradas         : {(df['ESTADO']=='NO ENCONTRADA').sum():,}")
print(f"Errores                : {(df['ESTADO']=='ERROR').sum():,}")

print("\nArchivo generado:")

print(archivo_salida)