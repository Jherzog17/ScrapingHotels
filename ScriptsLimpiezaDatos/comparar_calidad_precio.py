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
#patrón para decimales ya seas con coma o punto
patr_punt=re.compile(r"\d+(?:[.,]\d+)?")
def limpiar_puntuacion(x):
    if pd.isna(x):
        return np.nan
    #pasamos a string,por si tuviera otro tipo
    texto=str(x).strip()
    #busco según la expresión regular
    m=patr_punt.search(texto)
    if not m:
        return np.nan
    #convierto coma a punto
    numero=m.group(0).replace(",", ".")
    return float(numero)


def limpiar_estrellas(x:str):
    if pd.isna(x):
        return np.nan
    #paso a minúsculas
    texto = str(x).lower()
    #extraigo entero
    m = re.search(r"\d+", texto)
    if not m:
        return np.nan
    return int(m.group(0))

def df_limpiar(df):
    """
    -
    -Unifica columnas de Puntuación y Puntuacion en puntuaciont
    -Pasar las columnas de puntuacion y precio a formato exclusivamente númerico
    -crea la columna con la relacion calidad precio
    -borra las filas donde puntuacion o precio sea nan
    -guardamos en df_limpio las columnas nombre, web, ciudad, puntuacion,
    precio y calidad precio, para poder ahroa visualizar lo que nos interesa
    -mismo procedimiento que el anterior pero con estrellas
    """
    df=df.copy()

    df["puntuaciont"] = df["Puntuación"].fillna(df["Puntuacion"])
    df["puntuacion_num"] = df["puntuaciont"].map(limpiar_puntuacion)
    #en Edreams la puntuación era sobre 5
    df.loc[df["web"] == "Edreams", "puntuacion_num"] = df.loc[df["web"] == "Edreams", "puntuacion_num"] * 2
    df["precio_num"] = df["Precio"].map(limpiar_puntuacion)
    df["Estrellas_limp"] = df["Estrellas"].apply(limpiar_estrellas)
    
    df["calidad_precio"] = df["puntuacion_num"] / df["precio_num"]
    df["calidad_precio_estrellas"] = df["Estrellas_limp"] / df["precio_num"]
    df_limpio = df.dropna(subset=["puntuacion_num", "precio_num", "Estrellas_limp"]).copy()
    df_limpio = df_limpio[df_limpio["precio_num"] > 0]
    df_limpio=df_limpio[["Nombre", "web", "ciudad", "Estrellas_limp", "puntuacion_num", "precio_num", "calidad_precio", "calidad_precio_estrellas"]]
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

    limite2 = df.groupby(["web", "Estrellas_limp"])["calidad_precio_estrellas"].quantile(0.75)
    df["lim_web2"] = df.set_index(["web", "Estrellas_limp"]).index.map(limite2)
    df["es_chollo2"] = df["calidad_precio_estrellas"] >= df["lim_web2"]
    df=df.drop(columns=["lim_web", "lim_web2"])
    return df

def graf_media_web(df):
    """
    Grafico de barras con la calidad_precio media por web
    """
    media=(df.groupby("web")["calidad_precio"].mean().sort_values(ascending=False))
    media.plot(kind="bar", rot=0, title="Calidad-precio media por web", xlabel="Web", ylabel="Puntuacion/precio")

def graf_media_web2(df):
    """
    Grafico de barras con la calidad_precio media por web, pero con estrellas en vez de puntuacion
    """
    media=(df.groupby("web")["calidad_precio_estrellas"].mean().sort_values(ascending=False))
    media.plot(kind="bar", rot=0, title="Calidad-precio-estrellas media por web", xlabel="Web", ylabel="Estrellas/precio")

def graf_dispersion_precio_puntuacion(df):
    """
    Gráficos de dispersión para ver la relación entre precio y puntuación
    en cada web, coloreando por ciudad.
    """
    color_map = {"Ibiza": "red", "Sevilla": "blue", "Zaragoza": "black"}

    for web, df_web in df.groupby("web"):
        plt.figure()
        ax = plt.gca()

        for ciudad, group in df_web.groupby("ciudad"):
            group.plot(
                kind="scatter",
                x="precio_num",
                y="puntuacion_num",
                ax=ax,
                label=ciudad,
                color=color_map.get(ciudad, "black")
            )

        plt.title("Relación precio–puntuación en " + web)
        plt.xlabel("Precio")
        plt.ylabel("Puntuación")
        plt.legend()


if __name__ == "__main__":
    df_limpio = df_limpiar(df)
    df_chollos = marcar_chollo(df_limpio)

    print("Ejemplo de df_limpio:")
    print(df_limpio.head())

    print("\nEjemplo de df_chollos:")
    print(df_chollos.head())

    plt.figure()
    graf_media_web(df_chollos)
    plt.figure()
    graf_media_web2(df_chollos)


    graf_dispersion_precio_puntuacion(df_chollos)


    plt.show()

