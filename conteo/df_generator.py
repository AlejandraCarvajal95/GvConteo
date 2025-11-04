import pandas as pd
from conteo import config

def crear_tabla_rango_15min(df_filtrado_fechas):
    #  4.13 Seleccionar solo las columnas deseadas y cambiarles el nombre
    df_suma = df_filtrado_fechas[['HORA_I']].rename(columns={'HORA_I': 'rango_15_min'})

    #  5) Dataframe de SUMA
    #  5.1) Sumar las cantidades de cada tipo de vehículo
    df_suma['AUTOS'] = df_filtrado_fechas['AUTOS']
    df_suma['MOTOS'] = df_filtrado_fechas['MOTOS']
    df_suma['MIO'] = df_filtrado_fechas.get('C_PADRON',  0) + df_filtrado_fechas.get('C_ALIMENTADOR',  0) + df_filtrado_fechas.get('C_ARTICULADO',  0)
    df_suma['TPC'] = df_filtrado_fechas.get('MICROBUS',  0) + df_filtrado_fechas.get('BUSETA',  0) + df_filtrado_fechas.get('BUS',  0)
    df_suma['CAMIONES'] = df_filtrado_fechas.get('CAM_2EJ_PQ',  0)+ df_filtrado_fechas.get('CAM_2EJ_GD',  0) + df_filtrado_fechas.get('CAM_3EJ',  0) + df_filtrado_fechas.get('CAM_4EJ',  0) + df_filtrado_fechas.get('CAM_5EJ',0) + df_filtrado_fechas.get('CAM_6EJ',  0) + df_filtrado_fechas.get('C_CAMION3A4EJES',  0) + df_filtrado_fechas.get('C_CAMION5Y6EJES',  0)
    df_suma['MIXTOS'] = df_suma['AUTOS'] + df_suma['MIO']  + df_suma['TPC'] + df_suma['CAMIONES'] + df_suma['MOTOS']
    df_suma['BICICLETAS'] = df_filtrado_fechas['BICICLETA']

    #  5.2) Convertir la columna 'rango_15_min' a tipo datetime
    df_suma['rango_15_min'] = pd.to_datetime(df_suma['rango_15_min'], format='%H:%M:%S', errors='coerce')

    #  5.3) Agrupar por hora y sumar las cantidades
    df_suma_por_hora = df_suma.groupby(df_suma['rango_15_min'].dt.time).agg({
        'AUTOS': 'sum',
        'MOTOS': 'sum',
        'MIO' : 'sum',
        'TPC': 'sum',
        'CAMIONES': 'sum',
        'MIXTOS': 'sum',
        'BICICLETAS': 'sum'
    }).reset_index()

    return df_suma_por_hora

def crear_tabla_rango_hora(df):
    # Crear un DataFrame vacío para almacenar los resultados
    df_nuevo = pd.DataFrame(columns=df.columns[1:])  # Excluir la primera columna

    # Iterar sobre las filas de df
    for i in range(0, len(df), 4):  # Avanzar de 4 en 4
        # Seleccionar las filas disponibles a partir de la fila actual
        filas_disponibles = df.iloc[i:i + 4]  # Seleccionar 4 filas

        # Sumar las columnas seleccionadas
        suma_filas = filas_disponibles.iloc[:, 1:].sum()

        # Crear un nuevo DataFrame con la suma en la primera fila
        df_suma = pd.DataFrame(columns=suma_filas.index)
        df_suma.loc[filas_disponibles.iloc[0, 0]] = suma_filas

        # Agregar el resultado al DataFrame final
        df_nuevo = pd.concat([df_nuevo, df_suma])

    # Restablecer el índice y renombrar la columna del índice
    df_nuevo = df_nuevo.reset_index()
    df_nuevo = df_nuevo.rename(columns={'index': 'rango_15_min'})

    # Si df_nuevo está vacío, no intentes encontrar el índice máximo
    if not df_nuevo.empty:
        # Encontrar el índice del valor máximo en la columna "MIXTOS"
        indice_max = df_nuevo["MIXTOS"].idxmax()
        fila_max = df_nuevo.iloc[indice_max]  # Acceder al valor de la primera columna en el índice máximo

        # Obtener el valor máximo de la columna "MIXTOS"
        valor_max = df_nuevo["MIXTOS"].max()

        hora_pico = fila_max["rango_15_min"]
        
        config.hora_pico_global = 'La hora pico es ' + str(hora_pico) + ' con ' + str(valor_max) + ' vehículos'

    return df_nuevo


"""
def crear_tabla_rango_hora(df):
 
    # Crear un DataFrame vacío para almacenar los resultados
    df_nuevo = pd.DataFrame(columns=df.columns[1:])  # Excluir la primera columna

    # Iterar sobre las filas de df
    for i, fila in df.iterrows():
        # Seleccionar las primeras 4 filas a partir de la fila actual
        primeras_cuatro_filas = df.iloc[i:i+4]

        # Si hay menos de 4 filas disponibles, detener el bucle
        if len(primeras_cuatro_filas) < 4:
            break

        # Seleccionar todas las columnas excepto la primera
        columnas_a_sumar = primeras_cuatro_filas.iloc[:, 1:]

        # Sumar las columnas seleccionadas
        suma_primeras_cuatro = columnas_a_sumar.sum()

        # Crear un nuevo DataFrame con la suma en la primera fila
        df_suma_primeras_cuatro = pd.DataFrame(columns=columnas_a_sumar.columns)
        df_suma_primeras_cuatro.loc[primeras_cuatro_filas.iloc[0, 0]] = suma_primeras_cuatro

        # Agregar el resultado al DataFrame final
        df_nuevo = pd.concat([df_nuevo, df_suma_primeras_cuatro])

    # Restablecer el índice y renombrar la columna del índice
    df_nuevo = df_nuevo.reset_index()
    df_nuevo = df_nuevo.rename(columns={'index': 'rango_15_min'})

    # Encontrar el índice del valor máximo en la columna "MIXTOS"
    indice_max = df_nuevo["MIXTOS"].idxmax()
    fila_max = df_nuevo.iloc[indice_max]  # Acceder al valor de la primera columna en el índice máximo

    # Obtener el valor máximo de la columna "MIXTOS"
    valor_max = df_nuevo["MIXTOS"].max()

    hora_pico = fila_max["rango_15_min"]
    
    config.hora_pico_global = 'La hora pico es ' + str(hora_pico) + ' con ' + str(valor_max) + ' vehículos'

    return df_nuevo

"""














"""




def crear_tabla_rango_hora(df):
    # Obtener el índice de la última fila
    ultimo_indice = df.index[-1]


    # Inicializar un DataFrame vacío para almacenar los resultados
    resultados = pd.DataFrame(columns=df.columns)


    # Iterar sobre los índices desde el primero hasta el último - 3
    for indice in range(ultimo_indice - 3):


        # Seleccionar solo las columnas numéricas para la suma
        filas_para_suma = df.iloc[indice:indice+4].select_dtypes(include='number')
       
        # Sumar las filas seleccionadas
        suma = filas_para_suma.sum()
        print(suma)
       
        # Agregar la suma al DataFrame de resultados
       # resultados = resultados.append(suma, ignore_index=True)


    return resultados


























def crear_tabla_rango_hora(df):
    print('ESTE ES EL NUEVO DATAFRAMEEEEEE')
    # Crear un DataFrame vacío para almacenar los resultados
    df_nuevo = pd.DataFrame(columns=df.columns)


    # Iterar sobre las filas de df
    for i, fila in df.iterrows():
        # Seleccionar las primeras 4 filas a partir de la fila actual
        primeras_cuatro_filas = df.iloc[i:i+4]


        # Si hay menos de 4 filas disponibles, detener el bucle
        if len(primeras_cuatro_filas) < 4:
            break


        # Seleccionar todas las columnas excepto la primera
        columnas_a_sumar = primeras_cuatro_filas.iloc[:, 1:]


        # Sumar las columnas seleccionadas
        suma_primeras_cuatro = columnas_a_sumar.sum()


        # Crear un nuevo DataFrame con la suma en la primera fila
        df_suma_primeras_cuatro = pd.DataFrame(columns=columnas_a_sumar.columns)
        df_suma_primeras_cuatro.loc[primeras_cuatro_filas.iloc[0, 0]] = suma_primeras_cuatro


        # Agregar el resultado al DataFrame final
        df_nuevo = pd.concat([df_nuevo, df_suma_primeras_cuatro])


    # Eliminar la columna 'rango_15_min'
    df_nuevo = df_nuevo.drop(columns=['rango_15_min'])


    print('Este es el nuevo DataFrame:')
    print(df_nuevo)
    print(df_nuevo.columns)
    print(df_nuevo.index)
    return df_nuevo
"""
