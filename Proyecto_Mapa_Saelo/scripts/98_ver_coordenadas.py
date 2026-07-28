from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent

archivo = BASE / "resultados" / "coordenadas.xlsx"

df = pd.read_excel(archivo)

print("\nCOLUMNAS\n")
print(df.columns.tolist())

print("\nPRIMEROS REGISTROS\n")
print(df.head())