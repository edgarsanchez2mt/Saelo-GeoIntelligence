from pathlib import Path
import pandas as pd

# ==========================================
# PROYECTO MAPA DE CALOR SAELO
# Exploración de datos
# ==========================================

BASE = Path(__file__).resolve().parent.parent
archivo = BASE / "datos" / "PROYECTO MAPA CALOR SERVICIOS.xlsx"

df = pd.read_excel(archivo)

print("=" * 70)
print("RESUMEN DEL ARCHIVO")
print("=" * 70)

print(f"\nTotal de registros: {len(df)}")
print(f"Total de columnas : {len(df.columns)}")

print("\nCOLUMNAS")
print("-" * 70)

for i, col in enumerate(df.columns):
    print(f"{i+1:02d}. {col}")

print("\n" + "=" * 70)
print("VALORES NULOS")
print("=" * 70)

print(df.isnull().sum())

print("\n" + "=" * 70)
print("TIPOS DE DATOS")
print("=" * 70)

print(df.dtypes)

print("\n" + "=" * 70)
print("PRIMEROS 5 REGISTROS")
print("=" * 70)

print(df.head())