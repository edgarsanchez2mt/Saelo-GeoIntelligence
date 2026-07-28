from pathlib import Path
from datetime import datetime
import pandas as pd

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)

#====================================================
# RUTAS
#====================================================

BASE = Path(__file__).resolve().parent.parent

PLANTILLAS = BASE / "plantillas"
RESULTADOS = BASE / "resultados"
ENTREGABLES = BASE / "entregables"

ENTREGABLES.mkdir(exist_ok=True)

LOGO = PLANTILLAS / "logo_saelo.png"
MAPA = PLANTILLAS / "Mapa_Calor.png"

BASE_DATOS = RESULTADOS / "servicios_georreferenciados.xlsx"

PDF = ENTREGABLES / "Resumen_Ejecutivo.pdf"

#====================================================
# LEER BASE
#====================================================

df = pd.read_excel(BASE_DATOS)

total = len(df)

geocodificados = df["LATITUD"].notna().sum()

cobertura = geocodificados / total * 100

#====================================================
# ESTILOS
#====================================================

styles = getSampleStyleSheet()

titulo = styles["Title"]
titulo.alignment = TA_CENTER

sub = styles["Heading2"]
sub.alignment = TA_CENTER

normal = styles["BodyText"]

#====================================================
# DOCUMENTO
#====================================================

doc = SimpleDocTemplate(str(PDF))

story = []

#====================================================
# PORTADA
#====================================================

story.append(Image(str(LOGO), width=180, height=60))

story.append(Spacer(1,20))

story.append(Paragraph("SAELO GEO INTELLIGENCE", titulo))

story.append(Paragraph("Análisis Geoespacial", sub))

story.append(Spacer(1,20))

story.append(Paragraph("<b>Cliente:</b> Servicios Bolívar", normal))
story.append(Paragraph("<b>Periodo:</b> 2025 - 2026", normal))
story.append(Paragraph(f"<b>Fecha:</b> {datetime.now():%d/%m/%Y}", normal))

story.append(Spacer(1,30))

#====================================================
# RESUMEN
#====================================================

story.append(Paragraph("<b>RESUMEN EJECUTIVO</b>", sub))

story.append(Spacer(1,15))

story.append(Paragraph(f"Servicios analizados: <b>{total:,}</b>", normal))

story.append(Paragraph(f"Servicios georreferenciados: <b>{geocodificados:,}</b>", normal))

story.append(Paragraph(f"Cobertura geográfica: <b>{cobertura:.2f}%</b>", normal))

story.append(Spacer(1,20))

#====================================================
# MAPA
#====================================================

story.append(Image(str(MAPA), width=500, height=300))

story.append(Spacer(1,20))

texto = """
La visualización geoespacial permite identificar los principales
corredores operacionales utilizados por Saelo hacia el Aeropuerto
Internacional El Dorado.

Esta información constituye la base para modelos de inteligencia
operacional, optimización de flota y análisis predictivo de demanda.
"""

story.append(Paragraph(texto, normal))

story.append(Spacer(1,20))

story.append(Paragraph("<b>www.saelo.co</b>", sub))

doc.build(story)

print("="*60)
print("PDF GENERADO CORRECTAMENTE")
print("="*60)
print(PDF)