import pandas as pd
from pathlib import Path 
import matplotlib.pyplot as plt

def leer_csv_zona_webs(zonas:list, webs:list):
    """
    Esta funcion requiere dos parámetros, el de zona es una lista con la o las zonas(["Ibiza", "Sevilla" , "Zaragoza"] o
    ["Ibiza"] o ["Ibiza", "Sevilla"], etc) y webs es una lista con las webs de las cuales se van a abrir esos csv 
    (["Amimir", "Booking"] o ["Amimir", "Booking", "Edreams"], etc). Esta funcion lo  que hace es crear un diccionario 
    cuyos elementos son los csv de la zona indicada y la o las webs que se quieran.
    Además, esta funcion soluciona el problema de la columna Puntuación y Puntuacion dejandolo como Puntuacion
    y tambien crea una columna con la web a la que pertenece el df y otra con la zona
    """
    directorio_root = Path(__file__).resolve().parent
    dfs = {}
    
    for web in webs:
        for zona in zonas:
            nombre_df = f"df_{web}_{zona}"
            ruta_csv = directorio_root / "Datos" / "Crudo" / f"resultados_{web}_{zona}.csv"
            dfs[nombre_df] = pd.read_csv(ruta_csv, sep=';')
            dfs[nombre_df]["web"] = web
            dfs[nombre_df]["zona"] = zona
            dfs[nombre_df].columns = dfs[nombre_df].columns.str.replace("ó", "o")
    return dfs

def normalizar_nombres(dfs: dict):
    """
    Esta funcion requiere como parametro de entrada un diccionario con data frames y lo que hacer es 
    unificar por asi decirlo la columna de Nombre, creando una columna llamada Nombre_norm que sirve
    luego para detectar los hoteles que están simultaneamente en varias webs a la vez. Devuelve un 
    diccionario con los df con la columna esta de Nombre_norm
    """
    for df in dfs.values():
        df["Nombre_norm"] = df["Nombre"]#Creo una nueva columna para asi conservar los nombres originales

        df["Nombre_norm"] = df["Nombre_norm"].str.lower()#Poner todo a minúsculas

        #Quitar tíldes
        df["Nombre_norm"] = df["Nombre_norm"].str.replace("á", "a")
        df["Nombre_norm"] = df["Nombre_norm"].str.replace("é", "e")
        df["Nombre_norm"] = df["Nombre_norm"].str.replace("í", "i")
        df["Nombre_norm"] = df["Nombre_norm"].str.replace("ó", "o")
        df["Nombre_norm"] = df["Nombre_norm"].str.replace("ú", "u")

        # Quitar stopwords o palabras inutiles
        hoteles = ["affiliated","guesthouse", "agroturismo", "aparthotel","resorts", "resort", "boutique","hotels","hoteles", "hotel","sevilla's","sevilla", "seville", "bedroom","zaragoza", "hostales","hostal", "hostel", "apartamentos","apartamento", "apartments","apartment", "aparment", "adults only", "ibiza", "suites", "suite", "pensiones", "pension", "villa"]
        for hotel in hoteles:
            df["Nombre_norm"] = df["Nombre_norm"].str.replace(hotel, "")
        
        #Quitar determinantes y signos de puntuación
        determinantes = [r"\bde\b", r"\bel\b", r"\bla\b", r"\blos\b", r"\bdel\b", r"\bcan\b", r"\by\b", r"\*", ","]
        for det in determinantes:
            df["Nombre_norm"] = df["Nombre_norm"].str.replace(det, "", regex=True)

        #Quitar descripciones irrelevantes
        df["Nombre_norm"] = df["Nombre_norm"].str.replace("-", " ")
        df["Nombre_norm"] = df["Nombre_norm"].map(lambda x: x.split(" by ")[0])
        df["Nombre_norm"] = df["Nombre_norm"].map(lambda x: x.split(" en ")[0])
        df["Nombre_norm"] = df["Nombre_norm"].map(lambda x: x.split("with")[0])
        df["Nombre_norm"] = df["Nombre_norm"].map(lambda x: x.split("zona")[0])

        #Quitar espacios extra
        df["Nombre_norm"] = df["Nombre_norm"].str.replace(r"\s+", " ", regex=True)
        df["Nombre_norm"] = df["Nombre_norm"].str.strip()
        df.drop(df[df["Nombre_norm"] == ""].index, inplace=True)#Quitar los que se quedan sin nombre
    
    return dfs
        

def unir_df(dfs:dict):
    """
    Esta funcion lo que hace es que a partir de un diccionario de dfs, lo que hace es unir todos esos
    dfs en uno solo. Devuelve un  df
    """
    df_unido = pd.concat(list(dfs.values()), ignore_index=True)
    return df_unido

def hacer_plot_freq(df, tipo_grafica="pie"):
    """
    Dado un df con la columna de Nombre_norm(importante), lo que hace es agrupar los hoteles según
    si aparecen en 1 hotel, 2  o en los 3 a la vez y hace un grafico de barras o un diagrama de sectores.
    Eso se elige segun la variable tipo_grafica que puede tomar los valores pie o bar.
    
    """
    num_webs = df.groupby("web").count()
    
    df_ordenado = df_unido.sort_values("Nombre_norm")
    
    df_filtrado = df_ordenado.groupby("Nombre_norm").filter(lambda x: len(x) < len(num_webs)+1)
    df_filtrado.reset_index()
    
    frecuencia = df_filtrado.value_counts("Nombre_norm")
    df_frecuencias = frecuencia.reset_index(name="count")
    df_frecuencias  = df_frecuencias.groupby("count").count()
    
    webs=""
    for i in range(len(num_webs)):
        if len(num_webs) == 2:
            webs += num_webs.index[i] + " y "
        else:
            webs += num_webs.index[i] + ", "
    webs = webs[:-2]
    
    total = df_frecuencias["Nombre_norm"].sum()#Sirve para el porcentaje
    
    #Pintar la gráfica
    try:
        if tipo_grafica == "bar" or tipo_grafica == "pie":
            #Hacer la grafica
            if tipo_grafica=="bar":
                #Hacer plot de barras
                graf = df_frecuencias["Nombre_norm"].plot(kind="bar",rot=0)
                plt.title(f"Número de coincidencias del mismo hotel en {webs}", pad=30)
                plt.xlabel("Número de webs", labelpad=15)
                plt.ylabel("Número de hoteles", labelpad=55, rotation=0)
                graf.set_ylim(0, (max(df_frecuencias.values)+max(df_frecuencias.values)*0.1))
                graf.bar_label(graf.containers[0], padding=1, fontsize=10)
                plt.show()
            else:
                #Hacer el pie
                df_frecuencias["Nombre_norm"].plot(kind="pie", autopct= lambda p : '{:.0f}\n({:.1f}%)'. format( p * total/100,p))
                plt.title(f"Número de coincidencias del mismo hotel en {webs}")
                plt.ylabel("")
                leyenda =["Hoteles en 1 web"]
                for i in range(2,len(num_webs)+2):
                    leyenda.append(f"Hoteles en {i} webs")
                plt.legend(leyenda, loc="lower right", borderaxespad=-5)
                plt.show()
        else:
            raise Exception()
    except Exception:
        print("Tipo de gráfica introducida no válida. Tiene que ser o pie o bar")
    

if __name__ == "__main__":
    webs= ["Amimir", "Booking"]
    dfs = leer_csv_zona_webs(["Zaragoza"], webs)
    dfs_normalizado = normalizar_nombres(dfs)
    df_unido = unir_df(dfs)
    df_solo_3 = df_unido.groupby("Nombre_norm").filter(lambda x: len(x) == 3)
    df_solo_3.reset_index(inplace=True)
    df_solo_3.to_csv("prueba.csv")
    #Hacer plot de los hoteles y donde aparecen repetidos
    #Coincidencias en las 3 webs
    barras_2_webs = hacer_plot_freq(df_unido, "bar")
    pie_3_webs = hacer_plot_freq(df_unido)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    