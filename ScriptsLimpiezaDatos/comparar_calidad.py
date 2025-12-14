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



#crear dataframe limpio
df_limpio=df.dropna(subset=["puntuacion_num"]).copy()
#para comprobar el error que comento de las puntuaciones sobre 5

print("\comprobar escalas (0-5 vs 0-10)")
resumen_escalas = df_limpio.groupby("web")["puntuacion_num"].describe()[["min", "max", "mean"]]
print(resumen_escalas)


#en efecto edreams sigue la escala osbre 5 asi que hay que cambiarlo 

mask_edreams = df_limpio["web"] == "Edreams"
df_limpio.loc[mask_edreams, "puntuacion_num"] = df_limpio.loc[mask_edreams, "puntuacion_num"] * 2



#como he visto que edreams hay hoteles que le inflan un poco la meida, y ademas que podria ser posible que se repitan en el top
#he hecho que si los hoteles coinciden, haga una media d elas 3 valoraciones y de eso como resultado para comparar 

# Si un hotel sale en varias webs  media de sus notas
df_unicos = df_limpio.groupby(["Nombre", "ciudad", "tipo_alojamiento"])["puntuacion_num"].mean().reset_index()
df_unicos = df_unicos.sort_values("puntuacion_num", ascending=False)

#graficas de comparacion de los mejores hoteles  de cada ciudad
#guarda puntuacion y estrellas
df_unicos = df_limpio.groupby(["Nombre", "ciudad", "tipo_alojamiento"])[["puntuacion_num", "estrellas_num"]].mean().reset_index()

# nota total teniendo en cuenta estrellas y valoraxion.
df_unicos["nota_combinada"] = df_unicos["puntuacion_num"] + (df_unicos["estrellas_num"] * 2)

#ibz
ibiza_data = df_unicos[df_unicos["ciudad"] == "Ibiza"]
# ordenaos por la nueva nota combinada
top_ibiza = ibiza_data.sort_values("nota_combinada", ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_ibiza["Nombre"], top_ibiza["nota_combinada"], color='gold', edgecolor='orange')
plt.title("Top 10 hoteles (Estrellas + Valoracion)")
plt.xlabel("Puntuación Combinada (Máx 20)")
plt.xlim(0, 20) #lim en 20
plt.gca().invert_yaxis()
plt.show()

# sevilla
sevilla_data = df_unicos[df_unicos["ciudad"] == "Sevilla"]
top_sevilla = sevilla_data.sort_values("nota_combinada", ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_sevilla["Nombre"], top_sevilla["nota_combinada"], color='gold', edgecolor='orange')
plt.title("Top 10 hoteles de Sevilla (Estrelals + Valoración)")
plt.xlabel("Puntuación Combinada (Máx 20)")
plt.xlim(0, 20)
plt.gca().invert_yaxis()
plt.show()

# zaragoza
zaragoza_data = df_unicos[df_unicos["ciudad"] == "Zaragoza"]
top_zaragoza = zaragoza_data.sort_values("nota_combinada", ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_zaragoza["Nombre"], top_zaragoza["nota_combinada"], color='gold', edgecolor='orange')
plt.title("Top 10 hoteles Zaragoza (Estrelals + Valoració¡on)")
plt.xlabel("Puntuación Combinada (Máx 20)")
plt.xlim(0, 20)
plt.gca().invert_yaxis()
plt.show()

#ahora con los peores, pero teniendo solo en cuenta la valoracion 

# ibz peores
ibiza_data = df_unicos[df_unicos["ciudad"] == "Ibiza"]

# Ode menor a mayor
peor_ibiza = ibiza_data.sort_values("puntuacion_num", ascending=True).head(10)

plt.figure(figsize=(10, 6))
plt.barh(peor_ibiza["Nombre"], peor_ibiza["puntuacion_num"], color='salmon') 
plt.title("Top 10 Hoteles peor valorados de Ibiza ")
plt.xlabel("Valoración (0-10)")
plt.xlim(0, 10)
plt.gca().invert_yaxis() # que el peor de todos vaya aririba
plt.show()


# sev peores
sevilla_data = df_unicos[df_unicos["ciudad"] == "Sevilla"]

peor_sevilla = sevilla_data.sort_values("puntuacion_num", ascending=True).head(10)

plt.figure(figsize=(10, 6))
plt.barh(peor_sevilla["Nombre"], peor_sevilla["puntuacion_num"], color='salmon') 
plt.title("Top 10 Hoteles peor valorados de Sevilla")
plt.xlabel("Valoración (0-10)")
plt.xlim(0, 10)
plt.gca().invert_yaxis() 
plt.show()


# zar peores
zaragoza_data = df_unicos[df_unicos["ciudad"] == "Zaragoza"]

peor_zaragoza = zaragoza_data.sort_values("puntuacion_num", ascending=True).head(10)

plt.figure(figsize=(10, 6))
plt.barh(peor_zaragoza["Nombre"], peor_zaragoza["puntuacion_num"], color='salmon')
plt.title("Top 10 Hoteles peor valorados de Zaragoza")
plt.xlabel("Valoración (0-10)")
plt.xlim(0, 10)
plt.gca().invert_yaxis()
plt.show()

#que web tiene los hoteles mejor valorados de media 

ranking_webs = df_limpio.groupby("web")["puntuacion_num"].mean().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
ranking_webs.plot(kind="bar", color="blue", edgecolor="black")
plt.title("Nota Media Global por Web")
plt.ylim(0, 10)
plt.ylabel("Media")
plt.xticks(rotation=0)
plt.show()

#que ciudad tiene mejores hoteles con mejores valoraciones 
ranking_ciudades = df_unicos.groupby("ciudad")["puntuacion_num"].mean().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
ranking_ciudades.plot(kind="bar", color="orange", edgecolor="black")
plt.title("Media  por Ciudad")
plt.ylim(0, 10)
plt.ylabel("Media")
plt.xticks(rotation=0)
plt.show()


#comparacion con estrellas
#cada web cuantos hoteles dispone de cada tipo (con tipo me refiero a que un tipo seria de dos estrellas, otro tipo de 3 etc) para saber en que web buscar un tipo de hotel concereto: quiero buscar un hotel de 4 estrellas? mejor ir a esta pagina q tiene mas opicones


# filtrar para quitar 0 estrellas
df_estrellas = df_limpio[df_limpio["estrellas_num"] > 0]

# afrupar y contar
conteo_estrellas = df_estrellas.groupby(["estrellas_num", "web"]).size().unstack(fill_value=0)

conteo_estrellas.plot(kind="barh", figsize=(12, 8), width=0.8, edgecolor='black')

plt.title("Numero de hoteles segun Estrellas y Web")
plt.xlabel("Número de Hoteles disponibles")
plt.ylabel("Estrellas")
plt.legend(title="Web") #la leyenda
plt.grid(axis='x', linestyle='--', alpha=0.3) # rejilla vertical para medir mejor

plt.show()

# para ver num exactos
print("num exacto ")
print(conteo_estrellas)


#que ciudad tiene hoteles de mas calidad objetiva (teniendo en cuenta como calidad las estrellas)


ranking_estrellas = df_limpio.groupby("ciudad")["estrellas_num"].mean().sort_values(ascending=False)

plt.figure(figsize=(8, 6))
ranking_estrellas.plot(kind="bar", color="gold", edgecolor="black")
plt.title("Media de calidad de cada ciudad")
plt.ylabel("Media de Estrellas")
plt.ylim(0, 5) # estrellas de 0 a 5
plt.xticks(rotation=0) # nombres rectos
plt.show()

#ver quien cumple supuestamente lo que promete: hoteles que dan falsas espectativas (tienen muchas estrellas y buenas valoraciones) o por el contrario tienen pocas estrellas y buenas valoraciones es decir que estos datos se contradicen


datos_grafica = df_unicos[df_unicos["estrellas_num"] > 0]

plt.figure(figsize=(10, 6))
plt.scatter(datos_grafica["estrellas_num"], datos_grafica["puntuacion_num"], alpha=0.5, color='blue')
plt.title("Expectativas (Estrellas) vs Realidad (Nota)")
plt.xlabel("Estrellas Oficiales")
plt.ylabel("Nota de Usuarios (0-10)")
plt.grid(True, linestyle='--', alpha=0.3)

plt.show()


