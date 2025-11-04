import pandas as pd
from conteo.database_reader import (convertir_fecha, convertir_hora, agregar_vehiculos)

def cargar_filtros (df):
    
    df = convertir_fecha(df, ['FECHA'])
    df = convertir_hora(df, ['HORA_I'])
    df = convertir_hora(df, ['HORA_F'])
    lista_columnas = ['FECHA', 'HORA_RANGO_I', 'HORA_RANGO_F','DIGITADOR' ,'AFORADOR' ,'MOVIMIENTOS' ,
                'ZONA_TRANSITO' , 'ID_ESTACION','TIPO','MUNICIPIO','CORREGIMIENTO','VEREDA','UBICACION',
                'INTERSECCION','ID','FOLIO','HORA_I','HORA_F','AUTOS', 'C_PADRON', 'C_ALIMENTADOR', 'C_ARTICULADO',
                'MICROBUS', 'BUSETA', 'BUS','CAM_2EJ_PQ', 'CAM_2EJ_GD', 'CAM_3EJ', 'CAM_4EJ', 'CAM_5EJ',
                'CAM_6EJ', 'C_CAMION3A4EJES', 'C_CAMION5Y6EJES', 'MOTOS', 'BICICLETA']
    
    df = agregar_vehiculos(df, lista_columnas)

    filtros = ['FECHA', 'HORA_I', 'HORA_F', 'DIGITADOR', 'MOVIMIENTOS', 'ID_ESTACION', 'TIPO', 'INTERSECCION']

    # Diccionario para almacenar las opciones únicas de cada filtro
    opciones_unicas = {}

    # Por cada filtro, obtener las opciones únicas y almacenarlas en el diccionario
    for f in filtros:
        opciones = df[f].unique()  # Obtener opciones únicas de la columna
        opciones_unicas[f] = opciones.tolist()  # Convertir a lista y agregar al diccionario

    return opciones_unicas  # Devolver el diccionario con todas las opciones únicas

   