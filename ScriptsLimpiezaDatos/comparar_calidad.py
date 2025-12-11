import pandas as pd
import numpy as np
import re
from pathlib import Path
import matplotlib.pyplot as plt

carpeta_root = Path(__file__).resolve().parent.parent

#cargamos todos los csv
amimir_ibiza=pd.read_csv(carpeta_root / "Datos" / "Crudo" / "resultados_Amimir_Ibiza.csv", sep=";", encoding="utf-8")
amimir_sevilla=pd.read_csv(carpeta_root / "Datos" / "Crudo" / "resultados_Amimir_Sevilla.csv", sep=";", encoding="utf-8")
amimir_zaragoza=pd.read_csv(carpeta_root / "Datos" / "Crudo" / "resultados_Amimir_Zaragoza.csv", sep=";", encoding="utf-8")

booking_ibiza=pd.read_csv(carpeta_root / "Datos" / "Crudo" / "resultados_Booking_Ibiza.csv", sep=";", encoding="utf-8")
booking_sevilla=pd.read_csv(carpeta_root / "Datos" / "Crudo" / "resultados_Booking_Sevilla.csv", sep=";", encoding="utf-8")
booking_zaragoza=pd.read_csv(carpeta_root / "Datos" / "Crudo" / "resultados_Booking_Zaragoza.csv", sep=";", encoding="utf-8")

edreams_ibiza=pd.read_csv(carpeta_root / "Datos" / "Crudo" / "resultados_Edreams_Ibiza.csv", sep=";", encoding="utf-8")
edreams_sevilla=pd.read_csv(carpeta_root / "Datos" / "Crudo" / "resultados_Edreams_Sevilla.csv", sep=";", encoding="utf-8")
edreams_zaragoza=pd.read_csv(carpeta_root / "Datos" / "Crudo" / "resultados_Edreams_Zaragoza.csv", sep=";", encoding="utf-8")

#añadimos a tosos columnas con sus respectivas ciudades y webs, para al concatenar poder diferenciar
amimir_ibiza["ciudad"]="Ibiza"
amimir_ibiza["web"]="Amimir"
amimir_sevilla["ciudad"]="Sevilla"
amimir_sevilla["web"]="Amimir"
amimir_zaragoza["ciudad"]="Zaragoza"
amimir_zaragoza["web"]="Amimir"
booking_ibiza["ciudad"]="Ibiza"
booking_ibiza["web"]="Booking"
booking_sevilla["ciudad"]="Sevilla"
booking_sevilla["web"]="Booking"
booking_zaragoza["ciudad"]="Zaragoza"
booking_zaragoza["web"]="Booking"
edreams_ibiza["ciudad"]="Ibiza"
edreams_ibiza["web"]="Edreams"
edreams_sevilla["ciudad"]="Sevilla"
edreams_sevilla["web"]="Edreams"
edreams_zaragoza["ciudad"]="Zaragoza"
edreams_zaragoza["web"]="Edreams"
df=pd.concat([amimir_ibiza, amimir_sevilla, amimir_zaragoza, booking_ibiza, booking_sevilla, booking_zaragoza, edreams_ibiza, edreams_sevilla, edreams_zaragoza], ignore_index=True)

#unificamos las columnas puntuacion, puntuación
df["puntuaciont"]=df["Puntuación"].fillna(df["Puntuacion"])
#vamos a limpiar puntuacion y precio, porque se accede de la misma manera y queremos el mismo formato
patr_punt=re.compile(r"\d+(?:[.,]\d+)?")
def limpiar_puntuacion(x):
    if pd.isna(x):
        return None
    texto=str(x).strip()
    m=patr_punt.search(texto)
    if not m:
        raise ValueError(f"Puntuacion con formato diferente: {repr(texto)}")
    numero=m.group(0)
    numero=numero.replace(",", ".")
    return float(numero)
df["puntuacion_num"]=df["puntuaciont"].apply(limpiar_puntuacion)


#limpiar estrellas y llaves
patr_entero=re.compile(r"\d+")
def extraer_entero(x):
    if pd.isna(x):
        return None
    texto=str(x)
    m=patr_entero.search(texto)
    if not m:
        raise ValueError(f"Entero con formato diferente: {repr(texto)}")
    return int(m.group(0))
df["estrellas_num"]=df["Estrellas"].apply(extraer_entero)
if "Llaves" in df.columns:
    df["llaves_num"]=df["Llaves"].apply(extraer_entero)
else:
    df["llaves_num"]=0

#crear coluimna que separe si es hotel o apartamento
df["tipo_alojamiento"]=np.where(df["llaves_num"].fillna(0)>0, "Apartamento", "Hotel")

print(df[["Nombre", "Precio", "puntuaciont", "puntuacion_num", "Estrellas", "estrellas_num", "Llaves", "llaves_num"]].head(15))
print(df[["Nombre", "llaves_num", "tipo_alojamiento"]].head(15))

#crear dataframe limpio
df_limpio=df.dropna(subset=["puntuacion_num"]).copy()
print("Filas originales:", len(df))
print("Filas después de limpiar:", len(df_limpio))
#para comprobar el error que comento de las puntuaciones sobre 5

print("\comprobar escalas (0-5 vs 0-10)")
resumen_escalas = df_limpio.groupby("web")["puntuacion_num"].describe()[["min", "max", "mean"]]
print(resumen_escalas)
print("-----------------------------------------------\n")

#en efecto edreams sigue la escala osbre 5 asi que hay que cambiarlo 

mask_edreams = df_limpio["web"] == "Edreams"
df_limpio.loc[mask_edreams, "puntuacion_num"] = df_limpio.loc[mask_edreams, "puntuacion_num"] * 2

print("Corrección aplicada a Edreams y comprobacion con uevas estadísticas:")
print(df_limpio.groupby("web")["puntuacion_num"].describe()[["min", "max", "mean"]])
print("-----------------------------------------------")