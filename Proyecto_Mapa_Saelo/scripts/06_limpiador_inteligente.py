from pathlib import Path
import pandas as pd
import re

# ==========================================================
# SAELO - LIMPIADOR INTELIGENTE DE DIRECCIONES
# Versión 1.0
# ==========================================================

BASE = Path(__file__).resolve().parent.parent

archivo = BASE / "resultados" / "direcciones_normalizadas.xlsx"

df = pd.read_excel(archivo)

# Primera columna = dirección original
col = df.columns[0]

# ----------------------------------------------------------
# Correcciones frecuentes
# ----------------------------------------------------------

correcciones = {

    "ARRERA":"CARRERA",
    "CARREA":"CARRERA",
    "CARRAREA":"CARRERA",
    "CRR ":"KR ",
    "CRA ":"KR ",
    "CR ":"KR ",
    "CAR ":"KR ",

    "CALLEE":"CALLE",
    "CLL ":"CL ",
    "CLL.":"CL ",

    "AVEN ":"AV ",
    "AVENIDA ":"AV ",
    "AVC ":"AV ",

    "CINCURVALAR":"CIRCUNVALAR",

    "N°":"#",
    "NO ":"# ",
    "NUM ":"# ",
    "NUMERO ":"# "
}

# ----------------------------------------------------------
# Palabras que eliminaremos
# ----------------------------------------------------------

eliminar = [

    "APTO",
    "APARTAMENTO",
    "APART",
    "TORRE",
    "INTERIOR",
    "INT",
    "PISO",
    "CASA",
    "CONJUNTO",
    "CONJ",
    "RESIDENCIAL",
    "EDIFICIO",
    "EDF",
    "BARRIO",
    "BR",
    "LOCALIDAD",
    "LOC",
    "NOTA",
    "COLOMBIA",
    "BOGOTA",
    "BOGOTÁ",
    "D C",
    "D.C.",
]

# ----------------------------------------------------------
# Función principal
# ----------------------------------------------------------

def limpiar(direccion):

    if pd.isna(direccion):
        return ""

    d = str(direccion).upper()

    # Separador de comentarios
    d = d.split("///")[0]

    # Correcciones
    for viejo, nuevo in correcciones.items():
        d = d.replace(viejo, nuevo)

    # Eliminar puntuación
    d = re.sub(r"[;,]", " ", d)

    # Eliminar palabras innecesarias
    for palabra in eliminar:
        d = re.sub(r"\b" + re.escape(palabra) + r"\b", " ", d)

    # Eliminar espacios múltiples
    d = re.sub(r"\s+", " ", d)

    d = d.strip()

    return d


df["DIRECCION_LIMPIA"] = df[col].apply(limpiar)

# ----------------------------------------------------------
# Consulta optimizada para geocodificar
# ----------------------------------------------------------

df["CONSULTA_OSM"] = (
    df["DIRECCION_LIMPIA"] +
    ", Bogotá D.C., Colombia"
)

# ----------------------------------------------------------
# Guardar
# ----------------------------------------------------------

salida = BASE / "resultados" / "direcciones_limpias.xlsx"

df.to_excel(salida, index=False)

print("="*70)
print("LIMPIEZA COMPLETADA")
print("="*70)

print(f"Direcciones procesadas : {len(df):,}")

print("\nPrimeros ejemplos:\n")

for i in range(min(20, len(df))):

    print("-"*60)
    print("Original : ", df.loc[i, col])
    print("Limpia   : ", df.loc[i, "DIRECCION_LIMPIA"])