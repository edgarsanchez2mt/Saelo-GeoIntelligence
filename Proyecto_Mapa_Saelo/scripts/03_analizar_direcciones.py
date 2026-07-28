from pathlib import Path
import pandas as pd

# =====================================
# ANALISIS DE DIRECCIONES
# =====================================

BASE = Path(__file__).resolve().parent.parent
archivo = BASE / "datos" / "PROYECTO MAPA CALOR SERVICIOS.xlsx"

df = pd.read_excel(archivo)

print("="*70)
print("ANÁLISIS DE DIRECCIONES")
print("="*70)

# Total registros
print(f"\nTotal servicios : {len(df):,}")

# Solo Bogotá
bogota = df[df["Ciudad Origen"].str.upper().str.contains("BOGOTA", na=False)]

print(f"Servicios Bogotá : {len(bogota):,}")

print("\n")

print("="*70)
print("EMPRESAS")
print("="*70)

print(bogota["EMPRESA CLIENTE"].value_counts())

print("\n")

print("="*70)
print("TOP 20 DIRECCIONES MÁS FRECUENTES")
print("="*70)

print(bogota["DIRECCIÓN ORIGEN"].value_counts().head(20))

print("\n")

print("="*70)
print("TOP DESTINOS")
print("="*70)

print(bogota["DIRECCIÓN DESTINO"].value_counts().head(20))