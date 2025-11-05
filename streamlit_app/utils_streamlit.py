"""
Funciones adaptadoras para usar la lógica existente con Streamlit
Este archivo hace de puente entre Streamlit y el código original
"""

import pandas as pd
import sys
import os

# Agregar path para importar módulos originales
current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(current_path)
sys.path.append(parent_path)

from conteo import database_reader
from conteo import data_filter
from conteo import df_generator
from conteo import graph_generator
from conteo import config


def cargar_archivo_db(uploaded_file):
    """
    Carga un archivo Excel o CSV desde Streamlit
    
    Args:
        uploaded_file: Objeto UploadedFile de Streamlit
        
    Returns:
        DataFrame con los datos cargados
    """
    try:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            raise ValueError("Formato de archivo no soportado")
        return df
    except Exception as e:
        raise Exception(f"Error al cargar archivo: {str(e)}")


def obtener_filtros_disponibles(df):
    """
    Obtiene los filtros disponibles del DataFrame
    
    Args:
        df: DataFrame con los datos
        
    Returns:
        Diccionario con las opciones únicas de cada filtro
    """
    try:
        filtros = data_filter.cargar_filtros(df)
        
        # Convertir fechas a string
        if 'FECHA' in filtros:
            filtros['FECHA'] = [fecha.strftime('%Y-%m-%d') for fecha in filtros['FECHA']]
        
        return filtros
    except Exception as e:
        raise Exception(f"Error al cargar filtros: {str(e)}")


def aplicar_filtros_seleccionados(df, filtros_seleccionados):
    """
    Aplica los filtros seleccionados al DataFrame
    
    Args:
        df: DataFrame original
        filtros_seleccionados: Diccionario con los filtros seleccionados
        
    Returns:
        Tupla con (df_filtrado, df_suma_por_hora, df_rango_hora, graficos)
    """
    try:
        # Convertir columnas del DataFrame a string para comparaciones uniformes
        df['FECHA'] = df['FECHA'].astype(str)
        df['HORA_I'] = df['HORA_I'].astype(str)
        df['HORA_F'] = df['HORA_F'].astype(str)
        df['DIGITADOR'] = df['DIGITADOR'].astype(str)
        df['MOVIMIENTOS'] = df['MOVIMIENTOS'].astype(str)
        df['ID_ESTACION'] = df['ID_ESTACION'].astype(str)
        df['TIPO'] = df['TIPO'].astype(str)
        df['INTERSECCION'] = df['INTERSECCION'].astype(str)

        # Aplicar filtros
        df_filtrado = df.copy()
        
        # Filtro por fecha
        if filtros_seleccionados.get('FECHA'):
            df_filtrado = df_filtrado[df_filtrado['FECHA'].isin(filtros_seleccionados['FECHA'])]
        
        # Filtro por hora inicial
        if filtros_seleccionados.get('HORA_I'):
            df_filtrado['HORA_I'] = pd.to_datetime(df_filtrado['HORA_I'], format='%H:%M:%S').dt.time
            hora_i = pd.to_datetime(filtros_seleccionados['HORA_I'], format='%H:%M:%S').time()
            df_filtrado = df_filtrado[df_filtrado['HORA_I'] >= hora_i]
        
        # Filtro por hora final
        if filtros_seleccionados.get('HORA_F'):
            df_filtrado['HORA_F'] = pd.to_datetime(df_filtrado['HORA_F'], format='%H:%M:%S').dt.time
            hora_f = pd.to_datetime(filtros_seleccionados['HORA_F'], format='%H:%M:%S').time()
            df_filtrado = df_filtrado[df_filtrado['HORA_F'] <= hora_f]
        
        # Filtro por digitador
        if filtros_seleccionados.get('DIGITADOR'):
            df_filtrado = df_filtrado[df_filtrado['DIGITADOR'].isin(filtros_seleccionados['DIGITADOR'])]
        
        # Filtro por movimientos
        if filtros_seleccionados.get('MOVIMIENTOS'):
            df_filtrado = df_filtrado[df_filtrado['MOVIMIENTOS'].isin(filtros_seleccionados['MOVIMIENTOS'])]
        
        # Filtro por ID estación
        if filtros_seleccionados.get('ID_ESTACION'):
            df_filtrado = df_filtrado[df_filtrado['ID_ESTACION'].isin(filtros_seleccionados['ID_ESTACION'])]
        
        # Filtro por tipo
        if filtros_seleccionados.get('TIPO'):
            df_filtrado = df_filtrado[df_filtrado['TIPO'].isin(filtros_seleccionados['TIPO'])]
        
        # Filtro por intersección
        if filtros_seleccionados.get('INTERSECCION'):
            df_filtrado = df_filtrado[df_filtrado['INTERSECCION'].isin(filtros_seleccionados['INTERSECCION'])]
        
        # Verificar que no esté vacío
        if df_filtrado.empty:
            raise ValueError("Los filtros aplicados no devolvieron ningún resultado")
        
        # Generar tablas de análisis
        df_suma_por_hora = df_generator.crear_tabla_rango_15min(df_filtrado)
        df_rango_hora = df_generator.crear_tabla_rango_hora(df_suma_por_hora)
        
        # Generar gráficos
        grafico_barras = graph_generator.generar_grafico_barras(df_rango_hora)
        grafico_barras_apiladas = graph_generator.generar_grafico_barras_apiladas(df_suma_por_hora)
        
        # Extraer totales para gráfico de torta
        total_autos = df_suma_por_hora['AUTOS'].sum()
        total_motos = df_suma_por_hora['MOTOS'].sum()
        total_mio = df_suma_por_hora['MIO'].sum()
        total_tpc = df_suma_por_hora['TPC'].sum()
        total_camiones = df_suma_por_hora['CAMIONES'].sum()
        total_mixtos = df_suma_por_hora['MIXTOS'].sum()
        total_bicicletas = df_suma_por_hora['BICICLETAS'].sum()
        
        grafico_torta = graph_generator.generar_grafico_torta(
            total_autos, total_motos, total_mio, total_tpc, 
            total_camiones, total_mixtos, total_bicicletas
        )
        
        graficos = {
            'barras': grafico_barras,
            'barras_apiladas': grafico_barras_apiladas,
            'torta': grafico_torta
        }
        
        # Obtener hora pico
        hora_pico = config.hora_pico_global
        
        return df_filtrado, df_suma_por_hora, df_rango_hora, graficos, hora_pico
        
    except Exception as e:
        raise Exception(f"Error al aplicar filtros: {str(e)}")


def exportar_a_excel(df, nombre_archivo="dataframe"):
    """
    Convierte un DataFrame a bytes de Excel para descarga
    
    Args:
        df: DataFrame a exportar
        nombre_archivo: Nombre base del archivo
        
    Returns:
        Bytes del archivo Excel
    """
    import io
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')
    
    return output.getvalue()


def exportar_grafico_html(fig, nombre_archivo="grafico"):
    """
    Convierte un gráfico de Plotly a HTML para descarga
    
    Args:
        fig: Figura de Plotly
        nombre_archivo: Nombre base del archivo
        
    Returns:
        Bytes del archivo HTML
    """
    html_string = fig.to_html(include_plotlyjs='cdn')
    return html_string.encode('utf-8')


def exportar_grafico_png(fig):
    """
    Convierte un gráfico de Plotly a PNG para descarga
    Requiere kaleido instalado
    
    Args:
        fig: Figura de Plotly
        
    Returns:
        Bytes del archivo PNG
    """
    try:
        return fig.to_image(format="png", width=1200, height=800)
    except Exception as e:
        # Si falla (por falta de kaleido), retornar None
        return None


def crear_zip_completo(df_filtrado, df_suma_hora, df_rango_hora, graficos, hora_pico, nombre_archivo):
    """
    Crea un archivo ZIP con todos los resultados del análisis
    
    Args:
        df_filtrado: DataFrame con datos filtrados
        df_suma_hora: DataFrame con suma por 15 min
        df_rango_hora: DataFrame con rango por hora
        graficos: Diccionario con las figuras de Plotly
        hora_pico: String con información de hora pico
        nombre_archivo: Nombre base del archivo original
        
    Returns:
        Bytes del archivo ZIP
    """
    import io
    import zipfile
    from datetime import datetime
    
    # Crear buffer para el ZIP
    zip_buffer = io.BytesIO()
    
    # Obtener nombre limpio del archivo (sin extensión)
    nombre_base = nombre_archivo.replace('.xlsx', '').replace('.csv', '')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # 1. Agregar DataFrames como Excel
        zip_file.writestr(
            f"01_datos_filtrados.xlsx",
            exportar_a_excel(df_filtrado, "datos_filtrados")
        )
        
        zip_file.writestr(
            f"02_suma_15min.xlsx",
            exportar_a_excel(df_suma_hora, "suma_15min")
        )
        
        zip_file.writestr(
            f"03_rango_hora.xlsx",
            exportar_a_excel(df_rango_hora, "rango_hora")
        )
        
        # 2. Agregar gráficos como HTML
        zip_file.writestr(
            f"04_grafico_hora_pico.html",
            exportar_grafico_html(graficos['barras'], "grafico_barras")
        )
        
        zip_file.writestr(
            f"05_grafico_barras_apiladas.html",
            exportar_grafico_html(graficos['barras_apiladas'], "grafico_barras_apiladas")
        )
        
        zip_file.writestr(
            f"06_grafico_composicion.html",
            exportar_grafico_html(graficos['torta'], "grafico_torta")
        )
        
        # 3. Agregar hora pico como TXT
        zip_file.writestr(
            f"00_HORA_PICO.txt",
            hora_pico.encode('utf-8')
        )
        
        # 4. Agregar README con información
        readme_content = f"""
╔════════════════════════════════════════════════════════════╗
║          ANÁLISIS DE AFOROS VEHICULARES - GRUPOVIAL        ║
╚════════════════════════════════════════════════════════════╝

📅 Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
📁 Archivo original: {nombre_archivo}
🕐 {hora_pico}

═══════════════════════════════════════════════════════════════

📋 CONTENIDO DEL ARCHIVO:

1. 📊 DATOS Y TABLAS (Excel):
   ├─ 01_datos_filtrados.xlsx      - Datos completos después de filtros
   ├─ 02_suma_15min.xlsx            - Resumen cada 15 minutos
   └─ 03_rango_hora.xlsx            - Resumen por hora

2. 📈 GRÁFICOS INTERACTIVOS (HTML):
   ├─ 04_grafico_hora_pico.html     - Gráfico de barras con hora pico
   ├─ 05_grafico_barras_apiladas.html - Distribución por tipo de vehículo
   └─ 06_grafico_composicion.html   - Composición vehicular (torta)

3. 📝 INFORMACIÓN:
   └─ 00_HORA_PICO.txt              - Información de hora pico

═══════════════════════════════════════════════════════════════

💡 CÓMO USAR LOS GRÁFICOS HTML:

1. Abre los archivos .html en cualquier navegador web
2. Los gráficos son INTERACTIVOS:
   - Haz zoom con el mouse
   - Pasa el cursor para ver detalles
   - Usa los botones en la esquina superior derecha para:
     * Descargar como PNG
     * Hacer zoom
     * Pan
     * Resetear vista

═══════════════════════════════════════════════════════════════

📊 RESUMEN DEL ANÁLISIS:

Total de registros filtrados: {len(df_filtrado):,}
Periodo analizado: Ver archivos de datos
{hora_pico}

═══════════════════════════════════════════════════════════════

🚗 GRUPOVIALAPP v2.0 - Powered by Streamlit
        """
        
        zip_file.writestr(
            f"LEEME.txt",
            readme_content.encode('utf-8')
        )
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()
