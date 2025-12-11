import pandas as pd
import numpy as np
import re
from pathlib import Path
import matplotlib.pyplot as plt


carpeta_root = Path(__file__).resolve().parent.parent

#cargamos todos los csv
path=carpeta_root/"Datos/Crudo"
web_ciu=[("Amimir",  "Ibiza"),("Amimir",  "Sevilla"),("Amimir",  "Zaragoza"),
    ("Booking", "Ibiza"),("Booking", "Sevilla"),("Booking", "Zaragoza"),
    ("Edreams", "Ibiza"),("Edreams", "Sevilla"),("Edreams", "Zaragoza")]

df_1=[]
for web, ciudad in web_ciu:
    path_t=f"{path}/resultados_{web}_{ciudad}.csv"
    df_temp=pd.read_csv(path_t, sep=";", encoding="utf-8")
    df_temp["ciudad"]=ciudad
    df_temp["web"]=web
    df_1.append(df_temp)
df=pd.concat(df_1, ignore_index=True)

#vamos a limpiar puntuacion y precio, porque se accede de la misma manera y queremos el mismo formato
patr_punt=re.compile(r"\d+(?:[.,]\d+)?")
def limpiar_puntuacion(x):
    if pd.isna(x):
        return np.nan
    texto=str(x).strip()
    m=patr_punt.search(texto)
    if not m:
        return np.nan
    numero=m.group(0).replace(",", ".")
    return float(numero)


def limpiar_estrellas(x:str):
    x = str(x)
    if "estrellas" in x:
        estrellas = x.split("estrellas")[0]
    else:
        estrellas = x
    estrellas = estrellas.strip()
    estrellas = int(estrellas)
    return estrellas

def df_limpiar(df):
    """
    -
    -Unifica columnas de Puntuación y Puntuacion en puntuaciont
    -Pasar las columnas de puntuacion y precio a formato exclusivamente númerico
    -crea la columna con la relacion calidad precio
    -borra las filas donde puntuacion o precio sea nan
    -guardamos en df_limpio las columnas nombre, web, ciudad, puntuacion,
    precio y calidad precio, para poder ahroa visualizar lo que nos interesa
    """
    df=df.copy()
    filtro = df["web"] == "Edreams"
    df.loc[filtro, "Puntuacion"] = df.loc[filtro, "Puntuacion"] * 2

    df["puntuaciont"] = df["Puntuación"].fillna(df["Puntuacion"])
    df["puntuacion_num"] = df["puntuaciont"].map(limpiar_puntuacion)
    df["precio_num"] = df["Precio"].map(limpiar_puntuacion)
    df["Estrellas_limp"] = df["Estrellas"].apply(limpiar_estrellas)
    
    df["calidad_precio"] = df["puntuacion_num"] / df["precio_num"]
    df["calidad_precio_estrellas"] = df["Estrellas_limp"] / df["precio_num"]
    df_limpio = df.dropna(subset=["puntuacion_num", "precio_num"]).copy()
    df_limpio=df_limpio[["Nombre", "web", "ciudad", "puntuacion_num", "precio_num", "calidad_precio", "calidad_precio_estrellas"]]
    return df_limpio

def marcar_chollo(df):
    """
    va a marcar en es_chollo los hoteles que estan por encima del cuantil 75
    de calidad_precio dentro de cada web, top 25%
    """
    df=df.copy()
    limite=df.groupby("web")["calidad_precio"].quantile(0.75)
    df["lim_web"]=df["web"].map(limite)
    df["es_chollo"]=df["calidad_precio"]>=df["lim_web"]
    df=df.drop(columns=["lim_web"])
    return df

def graf_media_web(df):
    """
    Grafico de barras con la calidad_precio media por web
    """
    media=(df.groupby("web")["calidad_precio"].mean().sort_values(ascending=False))
    media.plot(kind="bar", rot=0, title="Calidad-precio media por web", xlabel="Web", ylabel="Puntuacion/precio")

def graf_dispersion_precio_puntuacion(df):
    """
    Gráficos de dispersión para ver la relación entre precio y puntuación
    en cada web, coloreando por ciudad.
    """
    webs = df["web"].unique()

    for web in webs:
        df_web = df[df["web"] == web]

        plt.figure()
        ciudades = df_web["ciudad"].unique()

        for ciudad in ciudades:
            df_wc = df_web[df_web["ciudad"] == ciudad]
            plt.scatter(df_wc["precio_num"], df_wc["puntuacion_num"], label=ciudad)

        plt.title("Relación precio–puntuación en " + web)
        plt.xlabel("Precio")
        plt.ylabel("Puntuación")
        plt.legend()

def graf_media_ciudad(df):
    """
    Gráfico de barras con la calidad_precio media por ciudad.
    """
    media = df.groupby("ciudad")["calidad_precio"].mean().sort_values(ascending=False)
    media.plot(
        kind="bar",
        rot=0,
        title="Calidad-precio media por ciudad",
        xlabel="Ciudad",
        ylabel="Puntuacion/precio"
    )



if __name__ == "__main__":
    df_limpio = df_limpiar(df)
    df_chollos = marcar_chollo(df_limpio)

    print("Ejemplo de df_limpio:")
    print(df_limpio.head())

    print("\nEjemplo de df_chollos:")
    print(df_chollos.head())

    plt.figure()
    graf_media_web(df_chollos)


    graf_dispersion_precio_puntuacion(df_chollos)

    plt.figure()
    graf_media_ciudad(df_limpio)

    plt.show()

print(df["web"])