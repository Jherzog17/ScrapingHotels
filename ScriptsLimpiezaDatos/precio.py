import pandas as pd
import numpy as np
import re
from pathlib import Path
import matplotlib.pyplot as plt

def limpiar_puntuacion(x):
    #vamos a limpiar puntuacion y precio, porque se accede de la misma manera y queremos el mismo formato
    patr_punt=re.compile(r"\d+(?:[.,]\d+)?")
    if pd.isna(x):
        return np.nan
    texto=str(x).strip()
    m=patr_punt.search(texto)
    if not m:
        return np.nan
    numero=m.group(0).replace(",", ".")
    return float(numero)


def df_limpiar(df):
    """
    -Unifica columnas de Puntuación y Puntuacion en puntuaciont
    -Pasar las columnas de puntuacion y precio a formato exclusivamente númerico
    -Convertir la columna de estrellas a númerico
    -La columna llaves a númerico
    """
    df=df.copy()
    df["puntuaciont"] = df["Puntuación"].fillna(df["Puntuacion"])
    df["puntuacion_num"] = df["puntuaciont"].map(limpiar_puntuacion)
    df["precio_num"] = df["Precio"].map(limpiar_puntuacion)

    df["calidad_precio"] = df["puntuacion_num"] / df["precio_num"]
    df_limpio = df.dropna(subset=["puntuacion_num", "precio_num"]).copy()
    df_limpio=df_limpio[["Nombre", "web", "ciudad", "puntuacion_num", "precio_num", "calidad_precio"]]

    return df_limpio



if __name__ == "__main__":
    carpeta_root = Path(__file__).resolve().parent.parent
    #cargamos todos los csv
    path=carpeta_root
    web_ciu=[("Amimir",  "Ibiza"),("Amimir",  "Sevilla"),("Amimir",  "Zaragoza"),
        ("Booking", "Ibiza"),("Booking", "Sevilla"),("Booking", "Zaragoza"),
        ("Edreams", "Ibiza"),("Edreams", "Sevilla"),("Edreams", "Zaragoza")]

    df_1=[]
    for web, ciudad in web_ciu:
        path_t=f"{path}/Datos/Crudo/resultados_{web}_{ciudad}.csv"
        df_temp=pd.read_csv(path_t, sep=";", encoding="utf-8")
        df_temp["ciudad"]=ciudad
        df_temp["web"]=web
        df_1.append(df_temp)
    df=pd.concat(df_1, ignore_index=True)
    df.to_csv(path / "Datos" / "Limpio" / "calidad-precio-all.csv", index=False)
    

    df_limpio=df_limpiar(df)


    #¿Qué web es más barata en términos generales?
    media_por_web = df_limpio.groupby('web')['precio_num'].mean().sort_values() #agrupo por web, caluclo el precio medio y ordeno (barato->caro)
    plt.figure(figsize=(8, 5)) #fijo ese tamaño para ver bien las etiquetas
    media_por_web.plot(kind='bar', rot=0) #pongo rot=0 para que no se giren las etiquetas
    plt.title("Precio medio por web")
    plt.ylabel("Precio medio (€)")
    plt.xlabel("Web")
    plt.show()

    #2¿Qué web es más barata dependiendo de la zona?
    media_web_ciudad = (df_limpio.groupby(['ciudad', 'web'])['precio_num'].mean().reset_index())
    tabla_pivot = media_web_ciudad.pivot(index='ciudad', columns='web', values='precio_num') #con pivot consigo una tabla en la que las columnas son las webs y las filas son las ciudades, así el valor que sale en cada casilla es el precio medio directamente
    plt.figure(figsize=(10, 6))
    tabla_pivot.plot(kind='bar', rot=0, ax=plt.gca()) #ax=plt.gca() hace que no se cree otra figura
    plt.title("Precio medio por web en cada ciudad")
    plt.ylabel("Precio medio (€)")
    plt.xlabel("Ciudad")
    plt.show()

    #3 ¿Cómo se distribuye el precio en todas las webs?
    plt.figure(figsize=(8, 5))
    df_limpio['precio_num'].plot(kind='hist', bins=20) #bins=20 divide el rango de los precio en 20 intervalos , así tiene más detalle el histograma
    plt.title("Distribución de precios de los hoteles")
    plt.xlabel("Precio (€)")
    plt.ylabel("Frecuencia") # Etiqueta estándar para un histograma
    plt.show()

    #3.1 ¿Y en cada web?
    webs_unicas = df_limpio['web'].unique() #he puesto unique() para así sacar un array con los nombres de las webs, poder recorrer cada web y entonces hacer el histograma
    #he preferido usar unique() en vez de poner for web in ["Amimir","Booking","Edreams"] para que así el código se adapte si añado o elimino alguna web
    for web in webs_unicas:
        subset = df_limpio[df_limpio['web'] == web] #filtro por web
        plt.figure(figsize=(8, 5))
        subset['precio_num'].plot(kind='hist', bins=20)
        plt.title(f"Distribución de precios - {web}") #pongo {web} para que se adapte a la web de ña que sea el histograma
        plt.xlabel("Precio (€)")
        plt.ylabel("Frecuencia")
        plt.show()

    #¿Cuáles son los 10 hoteles más caros?
    top_hoteles_mas_caros = df_limpio.sort_values('precio_num', ascending=False).head(10) #head(10) para que después de ordenarlos ascendentemente, coja los 10 más caros
    plt.figure(figsize=(8, 6))
    top_hoteles_mas_caros.plot(kind='barh', x='Nombre', y='precio_num', ax=plt.gca(), legend=False)
    plt.title("Top 10 hoteles más caros")
    plt.xlabel("Precio (€)")
    plt.xlim(800, 1000) #ajusto así el eje x para ver con más claridad la diferencia de precio entre los 10"
    plt.tight_layout() #evita que se corten las etiquetas de los nombres de los hoteles
    plt.show()
