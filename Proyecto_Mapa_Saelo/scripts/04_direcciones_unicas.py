from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent

archivo = BASE / "datos" / "PROYECTO MAPA CALOR SERVICIOS.xlsx"

df = pd.read_excel(archivo)

# Limpiar la columna de direcciones
df["DIRECCIÓN ORIGEN"] = (
    df["DIRECCIÓN ORIGEN"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# Eliminar vacíos
df = df[df["DIRECCIÓN ORIGEN"] != ""]
df = df[df["DIRECCIÓN ORIGEN"] != "NAN"]

# Direcciones únicas
direcciones = (
    df["DIRECCIÓN ORIGEN"]
    .drop_duplicates()
    .sort_values()
    .reset_index(drop=True)
)

print(f"Direcciones únicas encontradas: {len(direcciones):,}")

salida = BASE / "resultados" / "direcciones_unicas.xlsx"

direcciones.to_excel(salida, index=False)

print(f"\nArchivo guardado en:\n{salida}")