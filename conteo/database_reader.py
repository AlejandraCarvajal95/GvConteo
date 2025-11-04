import pandas as pd

def leer_datos(db_direccion):
    """Carga datos de un archivo de Excel en un DataFrame."""
    return pd.read_excel(db_direccion)

def ajustar_direccion(ruta):
    """Ajusta una ruta de archivo cambiando las comillas dobles por comillas simples
    y cambiando la dirección de los slashes a la forma correcta."""
    
    ruta = ruta.replace('"', "'")
    ruta = ruta.replace(r'\\', '/')
    return ruta

def convertir_fecha(df, columnas):
    #Convierte columnas especificadas al formato de fecha y hora.
    for columna in columnas:
        df[columna] = pd.to_datetime(df[columna], errors='coerce').dt.date
    return df

def convertir_hora(df, columnas):
    #Convierte columnas especificadas al formato de fecha y hora.
    for columna in columnas:
        df[columna] = pd.to_datetime(df[columna], format='%H:%M:%S', errors='coerce')
        df[columna] = df[columna].dt.strftime('%H:%M:%S')  # Formatear la hora
    return df

def agregar_vehiculos(df,lista_columnas):
    #Le agrega al dataframe más vehículos
    columnas_coincidentes = [col for col in df.columns if col in lista_columnas]
    
    return df[columnas_coincidentes]



