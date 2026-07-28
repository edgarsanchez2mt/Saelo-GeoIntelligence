# 07_geocodificar.py
from pathlib import Path
import logging,time,pandas as pd
from tqdm import tqdm
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut,GeocoderUnavailable
BASE=Path(__file__).resolve().parent.parent
ENTRADA=BASE/"resultados"/"direcciones_limpias.xlsx"
SALIDA=BASE/"resultados"/"coordenadas.xlsx"
ERRORES=BASE/"resultados"/"errores_geocodificacion.xlsx"
logging.basicConfig(filename=BASE/"resultados"/"geocodificacion.log",level=logging.INFO)
SAVE_EVERY=10;DELAY=1.1;MAX_RETRIES=3
geo=Nominatim(user_agent="SaeloGeoIntelligence/1.0")
def cargar():
    if SALIDA.exists(): return pd.read_excel(SALIDA)
    df=pd.read_excel(ENTRADA)
    for c in["LATITUD","LONGITUD","RESULTADO","FECHA"]:
        if c not in df.columns: df[c]=None
    return df
def buscar(q):
    for _ in range(MAX_RETRIES):
        try:
            l=geo.geocode(q,timeout=20)
            if l:return l.latitude,l.longitude,"OK"
            return None,None,"NO ENCONTRADA"
        except (GeocoderTimedOut,GeocoderUnavailable):
            time.sleep(5)
        except Exception as e:
            return None,None,str(e)
    return None,None,"ERROR"
df=cargar()
pend=df[df["LATITUD"].isna()].index
for i,n in enumerate(tqdm(pend),1):
    lat,lon,res=buscar(str(df.loc[n,"CONSULTA_OSM"]))
    df.loc[n,"LATITUD"]=lat
    df.loc[n,"LONGITUD"]=lon
    df.loc[n,"RESULTADO"]=res
    df.loc[n,"FECHA"]=pd.Timestamp.now()
    if i%SAVE_EVERY==0: df.to_excel(SALIDA,index=False)
    time.sleep(DELAY)
df.to_excel(SALIDA,index=False)
df[df["RESULTADO"]!="OK"].to_excel(ERRORES,index=False)
print("Proceso finalizado")
