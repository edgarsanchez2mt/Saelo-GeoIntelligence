from pathlib import Path
import pandas as pd
import re

# ==========================================================
# SAELO GEOINTELLIGENCE
# PREPARACIÓN PARA GEOCODIFICACIÓN
# VERSIÓN 1.0
# ==========================================================

BASE = Path(__file__).resolve().parent.parent

archivo = BASE / "resultados" / "direcciones_limpias.xlsx"

df = pd.read_excel(archivo)

# Nombre de la columna creada por el limpiador
COLUMNA = "DIRECCION_LIMPIA"

# ----------------------------------------------------------
# Expresión regular para detectar direcciones de Bogotá
# ----------------------------------------------------------

patron = re.compile(
    r"(AK|AC|AV|CL|KR|DG|TV|AUTO NORTE|AUTOPISTA NORTE|AUTOPISTA|AV SUBA|AV EL DORADO|AV BOYACA)"
    r".*?#\s*[\w\-]+\s*[- ]\s*[\w\-]+",
    flags=re.IGNORECASE
)

# ----------------------------------------------------------
# Función para extraer la mejor dirección
# ----------------------------------------------------------

def preparar_direccion(texto):

    if pd.isna(texto):
        return "", "VACIA"

    texto = str(texto).upper()

    # Eliminar comentarios posteriores
    texto = texto.split("///")[0]

    # Eliminar múltiples espacios
    texto = re.sub(r"\s+", " ", texto).strip()

    # Buscar dirección principal
    match = patron.search(texto)

    if match:
        direccion = match.group(0)

    else:
        direccion = texto

    # Limpiar espacios alrededor del #
    direccion = re.sub(r"\s*#\s*", " #", direccion)

    # Limpiar espacios alrededor del guion
    direccion = re.sub(r"\s*-\s*", "-", direccion)

    # Eliminar caracteres especiales
    direccion = direccion.replace("*", "")
    direccion = direccion.replace("(", "")
    direccion = direccion.replace(")", "")

    direccion = direccion.strip()

    # Consulta final para OpenStreetMap
    consulta = f"{direccion}, Bogotá D.C., Colombia"

    return consulta, "LISTA"


# ----------------------------------------------------------
# Procesar todas las direcciones
# ----------------------------------------------------------

consultas = []
estado = []

for direccion in df[COLUMNA]:

    consulta, est = preparar_direccion(direccion)

    consultas.append(consulta)
    estado.append(est)

df["CONSULTA_OSM"] = consultas
df["ESTADO"] = estado

# ----------------------------------------------------------
# Guardar resultado
# ----------------------------------------------------------

salida = BASE / "resultados" / "direcciones_preparadas.xlsx"

df.to_excel(salida, index=False)

# ----------------------------------------------------------
# Estadísticas
# ----------------------------------------------------------

print("=" * 70)
print("PREPARACIÓN PARA GEOCODIFICACIÓN")
print("=" * 70)

print(f"Direcciones procesadas : {len(df):,}")

print(f"Consultas listas       : {(df['ESTADO']=='LISTA').sum():,}")

print("\nPrimeros 20 ejemplos:\n")

for i in range(min(20, len(df))):

    print("-" * 70)
    print("Original : ", df.loc[i, COLUMNA])
    print("Consulta : ", df.loc[i, "CONSULTA_OSM"])

print("\nArchivo generado correctamente:")
print(salida)