import pandas as pd
import numpy as np
import re
from pathlib import Path
import matplotlib.pyplot as plt

carpeta_root = Path(__file__).resolve().parent
#cargamos todos los csv
path=carpeta_root
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



df_limpio=df_limpiar(df)
print(df_limpio)

#precio medio de los hoteles por web
media_por_web = df_limpio.groupby('web')['precio_num'].mean().sort_values()
plt.figure(figsize=(8, 5))
media_por_web.plot(kind='bar', rot=0)
plt.title("Precio medio por web")
plt.ylabel("Precio medio (€)")
plt.xlabel("Web")
plt.show()

#2
media_web_ciudad = (df_limpio.groupby(['ciudad', 'web'])['precio_num'].mean().reset_index())
tabla_pivot = media_web_ciudad.pivot(index='ciudad', columns='web', values='precio_num')

plt.figure(figsize=(10, 6))
tabla_pivot.plot(kind='bar', rot=0, ax=plt.gca())
plt.title("Precio medio por web en cada ciudad")
plt.ylabel("Precio medio (€)")
plt.xlabel("Ciudad")
plt.show()
#3 distribucion de precios
plt.figure(figsize=(8, 5))

# 2. Trazado del histograma (Integración con Pandas, Referencia: Page 14)
# Usamos directamente la Serie 'precio_num'
df_limpio['precio_num'].plot(kind='hist', bins=20)

# 3. Configuración de etiquetas y título (Referencia: Page 5)
plt.title("Distribución de precios de los hoteles")
plt.xlabel("Precio (€)")
plt.ylabel("Frecuencia") # Etiqueta estándar para un histograma
plt.show()

#3.1 distribución de precios para cada web
webs_unicas = df_limpio['web'].unique()
for web in webs_unicas:
    subset = df_limpio[df_limpio['web'] == web]
    plt.figure(figsize=(8, 5))
    subset['precio_num'].plot(kind='hist', bins=20)
    plt.title(f"Distribución de precios - {web}")
    plt.xlabel("Precio (€)")
    plt.ylabel("Frecuencia")
    plt.show()
###

tabla = media_web_ciudad.pivot(index='ciudad', columns='web', values='precio_num')

tabla.plot(kind='bar', figsize=(10,6))
plt.ylabel("Precio medio (€)")
plt.title("Precio medio por web en cada ciudad")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

#distribucion dr precios de los hoteles
plt.figure(figsize=(8,5))
plt.hist(df_limpio['precio_num'], bins=20)
plt.xlabel("Precio (€)")
plt.ylabel("Número de hoteles")
plt.title("Distribución de precios de los hoteles")
plt.tight_layout()
plt.show()

for web in df_limpio['web'].unique():
    plt.figure(figsize=(8,5))
    subset = df_limpio[df_limpio['web'] == web]
    plt.hist(subset['precio_num'], bins=20)
    plt.xlabel("Precio (€)")
    plt.ylabel("Número de hoteles")
    plt.title(f"Distribución de precios - {web}")
    plt.tight_layout()
    plt.show()

#que ciudad es más barata
media_ciudad = df_limpio.groupby('ciudad')['precio_num'].mean().sort_values()

plt.figure(figsize=(8,5))
x = np.arange(len(media_ciudad))
plt.bar(x, media_ciudad.values)
plt.xticks(x, media_ciudad.index)
plt.ylabel("Precio medio (€)")
plt.title("Precio medio de hoteles por ciudad")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,5))
plt.scatter(df_limpio['puntuacion_num'], df_limpio['precio_num'])
plt.xlabel("Puntuación")
plt.ylabel("Precio (€)")
plt.title("Relación entre puntuación y precio")
plt.tight_layout()
plt.show()

#top 10 hoteles mas caros
top_caros = df_limpio.sort_values('precio_num', ascending=False).head(10)
plt.figure(figsize=(8,6))
plt.barh(top_caros['Nombre'], top_caros['precio_num'])
plt.xlabel("Precio (€)")
plt.title("Top 10 hoteles más caros")
plt.tight_layout()
plt.show()

