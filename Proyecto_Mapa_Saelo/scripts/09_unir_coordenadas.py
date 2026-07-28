from pathlib import Path
import pandas as pd

# =====================================================
# RUTAS
# =====================================================

BASE = Path(__file__).resolve().parent.parent

ARCHIVO_ORIGINAL = BASE / "datos" / "servicios.xlsx"
ARCHIVO_COORDENADAS = BASE / "resultados" / "coordenadas.xlsx"

SALIDA = BASE / "resultados" / "servicios_georreferenciados.xlsx"

# =====================================================
# CARGAR ARCHIVOS
# =====================================================

print("=" * 60)
print("UNIÓN DE COORDENADAS")
print("=" * 60)

print("\nCargando archivo original...")

df_original = pd.read_excel(ARCHIVO_ORIGINAL)

print(f"Servicios originales: {len(df_original):,}")

print("\nCargando coordenadas...")

df_coord = pd.read_excel(ARCHIVO_COORDENADAS)

print(f"Direcciones geocodificadas: {len(df_coord):,}")

# =====================================================
# VALIDAR COLUMNAS
# =====================================================

if "DIRECCION_LIMPIA" not in df_original.columns:
    raise Exception("El archivo original NO tiene la columna DIRECCION_LIMPIA")

if "DIRECCION_LIMPIA" not in df_coord.columns:
    raise Exception("El archivo coordenadas NO tiene la columna DIRECCION_LIMPIA")

# =====================================================
# PREPARAR TABLA DE COORDENADAS
# =====================================================

columnas = [
    "DIRECCION_LIMPIA",
    "LATITUD",
    "LONGITUD",
    "RESULTADO"
]

df_coord = df_coord[columnas].drop_duplicates("DIRECCION_LIMPIA")

# =====================================================
# UNIR
# =====================================================

print("\nUniendo información...")

df = df_original.merge(
    df_coord,
    on="DIRECCION_LIMPIA",
    how="left"
)

# =====================================================
# ESTADÍSTICAS
# =====================================================

geocodificados = df["LATITUD"].notna().sum()

porcentaje = geocodificados / len(df) * 100

print("\n" + "=" * 60)
print("RESULTADOS")
print("=" * 60)

print(f"Servicios totales      : {len(df):,}")
print(f"Con coordenadas        : {geocodificados:,}")
print(f"Cobertura              : {porcentaje:.2f}%")

# =====================================================
# GUARDAR
# =====================================================

df.to_excel(SALIDA, index=False)

print("\nArchivo generado:")

print(SALIDA)

print("\nProceso finalizado correctamente.")