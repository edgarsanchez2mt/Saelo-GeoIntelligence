from pathlib import Path
import pandas as pd
import re

BASE = Path(__file__).resolve().parent.parent

archivo = BASE / "resultados" / "direcciones_normalizadas.xlsx"

df = pd.read_excel(archivo)

col = "DIRECCION_NORMALIZADA"

# Patrones
patron_calle = r"(CL|KR|DG|TV|AK|AC)"
patron_numero = r"#"

tienen_calle = df[col].str.contains(patron_calle, regex=True, na=False)
tienen_numero = df[col].str.contains(patron_numero, regex=True, na=False)

print("="*70)
print("AUDITORÍA DE DIRECCIONES")
print("="*70)

print(f"Total direcciones : {len(df):,}")

print(f"\nCon nomenclatura vial : {tienen_calle.sum():,}")

print(f"Con símbolo #         : {tienen_numero.sum():,}")

print(f"\nSin nomenclatura : {(~tienen_calle).sum():,}")

print("\nEjemplos SIN nomenclatura:\n")

ejemplos = df.loc[~tienen_calle, col].head(50)

for e in ejemplos:
    print("-", e)