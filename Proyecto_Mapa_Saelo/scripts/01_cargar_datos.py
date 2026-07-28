from pathlib import Path
import pandas as pd

# ==========================================
# PROYECTO MAPA DE CALOR SAELO
# Cargar archivo de Excel
# ==========================================

# Carpeta raíz del proyecto
BASE = Path(__file__).resolve().parent.parent

# Ruta del archivo Excel
archivo = BASE / "datos" / "PROYECTO MAPA CALOR SERVICIOS.xlsx"

print("=" * 60)
print("PROYECTO MAPA DE CALOR - SAELO")
print("=" * 60)
print(f"\nBuscando archivo en:\n{archivo}\n")

# Verificar si el archivo existe
if not archivo.exists():
    print("❌ ERROR: No se encontró el archivo.")
    exit()

print("✅ Archivo encontrado.")

# Leer el Excel
df = pd.read_excel(archivo)

print("\n✅ Excel cargado correctamente.")

print("\nPrimeras filas:")
print(df.head())

print("\nColumnas:")
print(df.columns.tolist())

print("\nCantidad de registros:")
print(len(df))

print("\nTipos de datos:")
print(df.dtypes)