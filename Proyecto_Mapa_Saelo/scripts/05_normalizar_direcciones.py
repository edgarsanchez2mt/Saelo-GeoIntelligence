from pathlib import Path
import pandas as pd
import re

# =====================================================
# NORMALIZADOR DE DIRECCIONES - SAELO
# =====================================================

BASE = Path(__file__).resolve().parent.parent

archivo = BASE / "resultados" / "direcciones_unicas.xlsx"

df = pd.read_excel(archivo)

# Detectar automáticamente la primera columna
col = df.columns[0]


def normalizar(direccion):

    if pd.isna(direccion):
        return ""

    d = str(direccion).upper()

    # -----------------------------
    # Eliminar caracteres extraños
    # -----------------------------

    d = d.replace(".", " ")
    d = d.replace(",", " ")
    d = d.replace(";", " ")
    d = d.replace(":", " ")

    # -----------------------------
    # Unificar abreviaturas
    # -----------------------------

    reemplazos = {

        "CALLE":"CL",
        "CARRERA":"KR",
        "CRA":"KR",
        "CR ":"KR ",
        "CAR ":"KR ",
        "AVENIDA":"AV",
        "AVEN ":"AV",
        "DIAGONAL":"DG",
        "TRANSVERSAL":"TV",

        "NUMERO":"#",
        "NÚMERO":"#",
        "NO ":"# ",
        "N°":"#",
        "NUM ":"#",

        "SUR":"SUR",
        "NORTE":"NORTE",
        "ESTE":"ESTE",
        "OESTE":"OESTE"

    }

    for viejo, nuevo in reemplazos.items():
        d = d.replace(viejo, nuevo)

    # -----------------------------
    # Eliminar espacios dobles
    # -----------------------------

    d = re.sub(r"\s+", " ", d)

    d = d.strip()

    return d


df["DIRECCION_NORMALIZADA"] = df[col].apply(normalizar)

antes = len(df)

despues = df["DIRECCION_NORMALIZADA"].nunique()

print("="*60)
print("NORMALIZACIÓN COMPLETADA")
print("="*60)

print(f"Direcciones originales : {antes:,}")
print(f"Direcciones únicas     : {despues:,}")
print(f"Reducción              : {antes-despues:,}")

salida = BASE / "resultados" / "direcciones_normalizadas.xlsx"

df.to_excel(salida,index=False)

print("\nArchivo generado:")

print(salida)