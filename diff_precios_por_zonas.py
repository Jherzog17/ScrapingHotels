import pandas as pd
from pathlib import Path


def leer_csv_zona(zona):
    """
    Esta función lee los csv de una zona y los almacena en un diccionario
    cuya clave es el nombre que identifica al df y el valor el df
    """
    webs = ["Amimir", "Booking", "Edreams"]
    directorio_root = Path(__file__).resolve().parent
    dfs = {}
    
    for web in webs:
        nombre_df = f"df_{web}_{zona}"
        ruta_csv = directorio_root / "csv" / f"resultados_{web}_{zona}.csv"
        dfs[nombre_df] = pd.read_csv(ruta_csv, sep=';')
        dfs[nombre_df]["web"] = web
        dfs[nombre_df].columns = dfs[nombre_df].columns.str.replace("ó", "o")
    return dfs

def normalizar_nombres(dfs: dict):
    """
    Función que modifica la columna de Nombre y la pone toda
    en minusculas, quita las tildes, quita palabras redundantes 
    y quita escapios extra
    """
    for df in dfs.values():
        df["Nombre"] = df["Nombre"].str.lower()#Poner todo a minúsculas

        #Quitar tíldes
        df["Nombre"] = df["Nombre"].str.replace("á", "a")
        df["Nombre"] = df["Nombre"].str.replace("é", "e")
        df["Nombre"] = df["Nombre"].str.replace("í", "i")
        df["Nombre"] = df["Nombre"].str.replace("ó", "o")
        df["Nombre"] = df["Nombre"].str.replace("ú", "u")

        #Quitar stopwords o palabras inutiles
        hoteles = ["guesthouse", "agroturismo", "aparthotel","resorts", "resort", "boutique","hotels","hoteles", "hotel", "hostales","hostal", "hostel", "apartamentos","apartamento", "apartments", "apartment", "adults only", "ibiza", "suites", "suit", "pensiones", "pension", "villa"]
        for hotel in hoteles:
            df["Nombre"] = df["Nombre"].str.replace(hotel, "")
        
        #Quitar determinantes y signos de puntuación
        determinantes = [r"\bde\b", r"\bel\b", r"\bla\b", r"\blos\b", r"\bdel\b", r"\bcan\b"]
        for det in determinantes:
            df["Nombre"] = df["Nombre"].str.replace(det, "", regex=True)

        #En booking a veces viene una descripcion con el nombre, esto viene siempre separado por - o ,

        #Quitar espacios extra
        df["Nombre"] = df["Nombre"].str.replace(r"\s+", " ", regex=True)
        df["Nombre"] = df["Nombre"].str.strip()
        df.drop(df[df["Nombre"] == ""].index, inplace=True)#Quitar los que se quedan sin nombre
    
    return dfs
        

def unir_df(dfs:dict):
    df_unido = pd.concat(list(dfs.values()), ignore_index=True)
    df_ordenado = df_unido.sort_values("Nombre")
    df_filrado = df_ordenado.groupby('Nombre').filter(lambda x: len(x) == 3)
    df_filrado.reset_index(drop=True, inplace=True)
    print(df_ordenado.head(n=50))
    return df_filrado

if __name__ == "__main__":
    dfs = leer_csv_zona("Ibiza")
    dfs_normalizado = normalizar_nombres(dfs)
    df_unido = unir_df(dfs_normalizado)