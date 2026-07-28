from pathlib import Path
import shutil
import zipfile
from datetime import datetime

# =====================================================
# SAELO GEO INTELLIGENCE
# Generador de Entregable Comercial
# =====================================================

BASE = Path(__file__).resolve().parent.parent

MAPAS = BASE / "mapas"
PLANTILLAS = BASE / "plantillas"
ENTREGABLES = BASE / "entregables"

ENTREGABLES.mkdir(exist_ok=True)

# -----------------------------------------------------
# Archivos origen
# -----------------------------------------------------

MAPA_HTML = MAPAS / "mapa_saelo.html"
LOGO = PLANTILLAS / "logo_saelo.png"
MAPA_PNG = PLANTILLAS / "Mapa_Calor.png"

# -----------------------------------------------------
# Verificar archivos
# -----------------------------------------------------

faltantes = []

for archivo in [MAPA_HTML, LOGO, MAPA_PNG]:
    if not archivo.exists():
        faltantes.append(str(archivo))

if faltantes:
    print("\nFALTAN LOS SIGUIENTES ARCHIVOS:\n")

    for f in faltantes:
        print(f)

    exit()

# -----------------------------------------------------
# Crear carpeta temporal
# -----------------------------------------------------

PAQUETE = ENTREGABLES / "Saelo_GeoIntelligence"

if PAQUETE.exists():
    shutil.rmtree(PAQUETE)

PAQUETE.mkdir()

# -----------------------------------------------------
# Copiar archivos
# -----------------------------------------------------

print("Copiando mapa interactivo...")

shutil.copy2(
    MAPA_HTML,
    PAQUETE / "Mapa_Interactivo.html"
)

print("Copiando logo...")

shutil.copy2(
    LOGO,
    PAQUETE / "Logo_Saelo.png"
)

print("Copiando imagen del mapa...")

shutil.copy2(
    MAPA_PNG,
    PAQUETE / "Mapa_Calor.png"
)

# -----------------------------------------------------
# Crear LEEME
# -----------------------------------------------------

texto = f"""
====================================================

SAELO GEO INTELLIGENCE

====================================================

Gracias por revisar esta demostración.

Este paquete contiene:

----------------------------------------------------

Mapa_Interactivo.html

Abra este archivo con:

• Google Chrome

• Microsoft Edge

• Mozilla Firefox

No necesita instalar ningún programa.

----------------------------------------------------

Mapa_Calor.png

Imagen del mapa generado por la plataforma.

----------------------------------------------------

Logo_Saelo.png

Logo corporativo.

----------------------------------------------------

Generado:

{datetime.now():%d/%m/%Y %H:%M}

====================================================

Desarrollado por

SAELO
Asistencia & Transporte

www.saelo.co

====================================================
"""

with open(PAQUETE / "LEEME.txt", "w", encoding="utf-8") as archivo:
    archivo.write(texto)

# -----------------------------------------------------
# Crear ZIP
# -----------------------------------------------------

ZIP = ENTREGABLES / "Saelo_GeoIntelligence.zip"

if ZIP.exists():
    ZIP.unlink()

print("Generando ZIP...")

with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:

    for archivo in PAQUETE.iterdir():
        z.write(archivo, archivo.name)

print("\n" + "="*60)
print("ENTREGABLE CREADO EXITOSAMENTE")
print("="*60)

print(f"\nArchivo generado:\n{ZIP}")