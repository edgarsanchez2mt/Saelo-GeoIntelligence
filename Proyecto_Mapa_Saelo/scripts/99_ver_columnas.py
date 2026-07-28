from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent

archivo = BASE / "resultados" / "direcciones_limpias.xlsx"

df = pd.read_excel(archivo)

print("="*70)
print("COLUMNAS")
print("="*70)

for i, c in enumerate(df.columns):
    print(f"{i+1}. {c}")

print("\n")
print(df.head())