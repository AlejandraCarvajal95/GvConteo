"""
Página de Análisis de Base de Datos
Versión Streamlit - Interfaz moderna y responsiva
"""

import streamlit as st
import pandas as pd
import sys
import os

# Agregar path
current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(os.path.dirname(current_path))
sys.path.append(parent_path)

from streamlit_app.utils_streamlit import (
    cargar_archivo_db,
    obtener_filtros_disponibles,
    aplicar_filtros_seleccionados,
    exportar_a_excel,
    exportar_grafico_html,
    exportar_grafico_png,
    crear_zip_completo
)


def show():
    """Función principal que muestra la página de análisis"""
    
    st.header("Análisis de Base de Datos de Aforos")
    st.markdown("---")
    
    # Inicializar estado de sesión
    if 'df_original' not in st.session_state:
        st.session_state.df_original = None
    if 'filtros_disponibles' not in st.session_state:
        st.session_state.filtros_disponibles = None
    if 'archivo_nombre' not in st.session_state:
        st.session_state.archivo_nombre = None
    
    # ==================== SECCIÓN 1: CARGAR ARCHIVO ====================
    st.subheader("1. Cargar Archivo")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Selecciona un archivo Excel o CSV",
            type=['xlsx', 'csv'],
            help="Formatos soportados: .xlsx, .csv"
        )
    
    with col2:
        if st.session_state.archivo_nombre:
            st.info(f"**Archivo cargado:**\n{st.session_state.archivo_nombre}")
            if st.button("Borrar archivo", use_container_width=True):
                st.session_state.df_original = None
                st.session_state.filtros_disponibles = None
                st.session_state.archivo_nombre = None
                st.rerun()
    
    # Procesar archivo si se cargó uno nuevo
    if uploaded_file is not None:
        if st.session_state.archivo_nombre != uploaded_file.name:
            try:
                with st.spinner('Cargando archivo...'):
                    df = cargar_archivo_db(uploaded_file)
                    st.session_state.df_original = df
                    st.session_state.archivo_nombre = uploaded_file.name
                    
                    # Obtener filtros disponibles
                    filtros = obtener_filtros_disponibles(df)
                    st.session_state.filtros_disponibles = filtros
                    
                    st.success(f"✅ Archivo cargado exitosamente: {uploaded_file.name}")
                    st.info(f"Total de filas: **{len(df):,}**")
                    
            except Exception as e:
                st.error(f"❌ Error al cargar el archivo: {str(e)}")
                return
    
    # Si no hay archivo cargado, mostrar mensaje y detener
    if st.session_state.df_original is None:
        st.warning("Por favor, carga un archivo para continuar")
        return
    

    
    st.markdown("---")
    
    # ==================== SECCIÓN 2: VISTA PREVIA DE DATOS ====================
    st.subheader("2. Vista Previa de Datos")
    
    with st.expander("Ver información del archivo cargado", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Filas", f"{len(st.session_state.df_original):,}")
        
        with col2:
            st.metric("Total de Columnas", len(st.session_state.df_original.columns))
        
        with col3:
            fechas_unicas = len(st.session_state.filtros_disponibles.get('FECHA', []))
            st.metric("Fechas Únicas", fechas_unicas)
        
        st.dataframe(
            st.session_state.df_original.head(10),
            use_container_width=True,
            height=300
        )
    
    st.markdown("---")
    
    # ==================== SECCIÓN 3: FILTROS ====================
    st.subheader("3. Seleccionar Filtros")
    
    filtros = st.session_state.filtros_disponibles
    
    # Crear tabs para organizar los filtros
    tab1, tab2 = st.tabs(["Filtros Temporales", "Filtros de Categoría"])
    
    # --- TAB 1: Filtros Temporales ---
    with tab1:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**FECHA**")
            fechas_opciones = filtros.get('FECHA', [])
            if fechas_opciones:
                seleccionar_todas_fechas = st.checkbox("Seleccionar todas las fechas", value=True)
                if seleccionar_todas_fechas:
                    fechas_seleccionadas = fechas_opciones
                else:
                    fechas_seleccionadas = st.multiselect(
                        "Selecciona fechas:",
                        options=fechas_opciones,
                        default=[],
                        label_visibility="collapsed",
                        placeholder="Selecciona opciones"
                    )
            else:
                fechas_seleccionadas = []
                st.warning("No hay fechas disponibles")
        
        with col2:
            st.markdown("**HORA INICIO**")
            horas_inicio = filtros.get('HORA_I', [])
            if horas_inicio:
                hora_inicio_seleccionada = st.selectbox(
                    "Hora de inicio:",
                    options=horas_inicio,
                    index=0,
                    label_visibility="collapsed"
                )
            else:
                hora_inicio_seleccionada = None
                st.warning("No hay horas disponibles")
        
        with col3:
            st.markdown("**HORA FIN**")
            horas_fin = filtros.get('HORA_F', [])
            if horas_fin:
                hora_fin_seleccionada = st.selectbox(
                    "Hora de fin:",
                    options=horas_fin,
                    index=len(horas_fin) - 1 if horas_fin else 0,
                    label_visibility="collapsed"
                )
            else:
                hora_fin_seleccionada = None
                st.warning("No hay horas disponibles")
    
    # --- TAB 2: Filtros de Categoría ---
    with tab2:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**DIGITADOR**")
            digitadores = filtros.get('DIGITADOR', [])
            digitadores_str = [str(d) for d in digitadores]
            if digitadores_str:
                seleccionar_todos_digitadores = st.checkbox("Todos", value=True, key="digitadores")
                if seleccionar_todos_digitadores:
                    digitadores_seleccionados = digitadores_str
                else:
                    digitadores_seleccionados = st.multiselect(
                        "Digitadores:",
                        options=digitadores_str,
                        default=[],
                        label_visibility="collapsed",
                        placeholder="Selecciona opciones"
                    )
            else:
                digitadores_seleccionados = []
        
        with col2:
            st.markdown("**MOVIMIENTOS**")
            movimientos = filtros.get('MOVIMIENTOS', [])
            movimientos_str = [str(m) for m in movimientos]
            if movimientos_str:
                seleccionar_todos_movimientos = st.checkbox("Todos", value=True, key="movimientos")
                if seleccionar_todos_movimientos:
                    movimientos_seleccionados = movimientos_str
                else:
                    movimientos_seleccionados = st.multiselect(
                        "Movimientos:",
                        options=movimientos_str,
                        default=[],
                        label_visibility="collapsed",
                        placeholder="Selecciona opciones"
                    )
            else:
                movimientos_seleccionados = []
        
        with col3:
            st.markdown("**ID ESTACIÓN**")
            id_estaciones = filtros.get('ID_ESTACION', [])
            id_estaciones_str = [str(i) for i in id_estaciones]
            if id_estaciones_str:
                seleccionar_todas_estaciones = st.checkbox("Todas", value=True, key="estaciones")
                if seleccionar_todas_estaciones:
                    estaciones_seleccionadas = id_estaciones_str
                else:
                    estaciones_seleccionadas = st.multiselect(
                        "Estaciones:",
                        options=id_estaciones_str,
                        default=[],
                        label_visibility="collapsed",
                        placeholder="Selecciona opciones"
                    )
            else:
                estaciones_seleccionadas = []
        
        with col4:
            st.markdown("**TIPO**")
            tipos = filtros.get('TIPO', [])
            tipos_str = [str(t) for t in tipos]
            if tipos_str:
                seleccionar_todos_tipos = st.checkbox("Todos", value=True, key="tipos")
                if seleccionar_todos_tipos:
                    tipos_seleccionados = tipos_str
                else:
                    tipos_seleccionados = st.multiselect(
                        "Tipos:",
                        options=tipos_str,
                        default=[],
                        label_visibility="collapsed",
                        placeholder="Selecciona opciones"
                    )
            else:
                tipos_seleccionados = []
        
        # Segunda fila de filtros
        st.markdown("**INTERSECCIÓN**")
        intersecciones = filtros.get('INTERSECCION', [])
        intersecciones_str = [str(i) for i in intersecciones]
        if intersecciones_str:
            seleccionar_todas_intersecciones = st.checkbox("Todas", value=True, key="intersecciones")
            if seleccionar_todas_intersecciones:
                intersecciones_seleccionadas = intersecciones_str
            else:
                intersecciones_seleccionadas = st.multiselect(
                    "Intersecciones:",
                    options=intersecciones_str,
                    default=[],
                    label_visibility="collapsed",
                    placeholder="Selecciona opciones"
                )
        else:
            intersecciones_seleccionadas = []
    
    st.markdown("---")
    
    # ==================== SECCIÓN 4: REALIZAR ANÁLISIS ====================
    st.subheader("4. Realizar Análisis")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        analizar_button = st.button(
            "REALIZAR ANÁLISIS",
            type="primary",
            use_container_width=True,
            help="Aplica los filtros seleccionados y genera los reportes"
        )
    
    if analizar_button:
        # Construir diccionario de filtros seleccionados
        filtros_seleccionados = {
            'FECHA': fechas_seleccionadas,
            'HORA_I': hora_inicio_seleccionada,
            'HORA_F': hora_fin_seleccionada,
            'DIGITADOR': digitadores_seleccionados,
            'MOVIMIENTOS': movimientos_seleccionados,
            'ID_ESTACION': estaciones_seleccionadas,
            'TIPO': tipos_seleccionados,
            'INTERSECCION': intersecciones_seleccionadas
        }
        
        try:
            with st.spinner('🔄 Aplicando filtros y generando análisis...'):
                df_filtrado, df_suma_hora, df_rango_hora, graficos, hora_pico = aplicar_filtros_seleccionados(
                    st.session_state.df_original.copy(),
                    filtros_seleccionados
                )
            
            st.success("✅ Análisis completado exitosamente!")
            
            # Guardar resultados en session_state
            st.session_state.resultados = {
                'df_filtrado': df_filtrado,
                'df_suma_hora': df_suma_hora,
                'df_rango_hora': df_rango_hora,
                'graficos': graficos,
                'hora_pico': hora_pico
            }
            
        except ValueError as e:
            st.warning(f"⚠️ {str(e)}")
            return
        except Exception as e:
            st.error(f"❌ Error durante el análisis: {str(e)}")
            return
    
    # ==================== SECCIÓN 5: RESULTADOS ====================
    if 'resultados' in st.session_state:
        st.markdown("---")
        st.subheader("5. Resultados del Análisis")
        
        resultados = st.session_state.resultados
        
        # Mostrar hora pico destacada
        st.info(f"**{resultados['hora_pico']}**")
        
        # Tabs para organizar los resultados
        tab1, tab2, tab3, tab4 = st.tabs(["Gráficos", "Datos Filtrados", "Por Hora", "Descargas"])
        
        # --- TAB 1: Gráficos ---
        with tab1:
            st.markdown("### Visualizaciones")
            
            # Gráfico de barras (hora pico)
            st.markdown("#### Volúmenes por Hora (Hora Pico)")
            st.plotly_chart(resultados['graficos']['barras'], use_container_width=True)
            
            # Gráfico de barras apiladas
            st.markdown("#### Distribución por Tipo de Vehículo (15 min)")
            st.plotly_chart(resultados['graficos']['barras_apiladas'], use_container_width=True)
            
            # Gráfico de torta
            st.markdown("#### Composición Vehicular")
            st.plotly_chart(resultados['graficos']['torta'], use_container_width=True)
        
        # --- TAB 2: Datos Filtrados ---
        with tab2:
            st.markdown("### Datos Filtrados")
            st.dataframe(
                resultados['df_filtrado'],
                use_container_width=True,
                height=400
            )
            
            st.metric("Total de filas después de filtros", f"{len(resultados['df_filtrado']):,}")
        
        # --- TAB 3: Por Hora ---
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Suma por Intervalos de 15 min")
                st.dataframe(
                    resultados['df_suma_hora'],
                    use_container_width=True,
                    height=400
                )
            
            with col2:
                st.markdown("### Resumen por Hora")
                st.dataframe(
                    resultados['df_rango_hora'],
                    use_container_width=True,
                    height=400
                )
        
        # --- TAB 4: Descargas ---
        with tab4:
            st.markdown("### Descargar Resultados")
            
            # Sección 1: Descargar TODO en un ZIP
            st.markdown("#### Descarga Completa")
            st.info("Descarga un archivo ZIP con todos los datos, gráficos y reportes")
            
            nombre_archivo_zip = f"Analisis-{st.session_state.archivo_nombre.replace('.xlsx', '').replace('.csv', '')}.zip"
            
            zip_completo = crear_zip_completo(
                resultados['df_filtrado'],
                resultados['df_suma_hora'],
                resultados['df_rango_hora'],
                resultados['graficos'],
                resultados['hora_pico'],
                st.session_state.archivo_nombre
            )
            
            st.download_button(
                label="DESCARGAR TODO (ZIP)",
                data=zip_completo,
                file_name=nombre_archivo_zip,
                mime="application/zip",
                use_container_width=True,
                type="primary"
            )
            
            st.markdown("**Contenido del ZIP:**")
            st.markdown("""
            - 3 archivos Excel (datos filtrados, suma 15min, rango hora)
            - 3 gráficos interactivos HTML (hora pico, barras apiladas, composición)
            - Archivo TXT con hora pico
            - Archivo LEEME.txt con instrucciones
            """)
            
            st.markdown("---")
            
            # Sección 2: Descargar Datos (Excel)
            st.markdown("#### Descargar Datos (Excel)")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                excel_filtrado = exportar_a_excel(resultados['df_filtrado'], "datos_filtrados")
                st.download_button(
                    label="Datos Filtrados",
                    data=excel_filtrado,
                    file_name="datos_filtrados.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col2:
                excel_suma = exportar_a_excel(resultados['df_suma_hora'], "suma_15min")
                st.download_button(
                    label="Suma 15 min",
                    data=excel_suma,
                    file_name="suma_15min.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col3:
                excel_rango = exportar_a_excel(resultados['df_rango_hora'], "rango_hora")
                st.download_button(
                    label="Rango Hora",
                    data=excel_rango,
                    file_name="rango_hora.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            st.markdown("---")
            
            # Sección 3: Descargar Gráficos (HTML)
            st.markdown("#### Descargar Gráficos (HTML Interactivo)")
            st.caption("Los gráficos HTML se pueden abrir en cualquier navegador y son totalmente interactivos")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                html_barras = exportar_grafico_html(resultados['graficos']['barras'])
                st.download_button(
                    label="Hora Pico (HTML)",
                    data=html_barras,
                    file_name="grafico_hora_pico.html",
                    mime="text/html",
                    use_container_width=True
                )
            
            with col2:
                html_apiladas = exportar_grafico_html(resultados['graficos']['barras_apiladas'])
                st.download_button(
                    label="Barras Apiladas (HTML)",
                    data=html_apiladas,
                    file_name="grafico_barras_apiladas.html",
                    mime="text/html",
                    use_container_width=True
                )
            
            with col3:
                html_torta = exportar_grafico_html(resultados['graficos']['torta'])
                st.download_button(
                    label="Composición (HTML)",
                    data=html_torta,
                    file_name="grafico_composicion.html",
                    mime="text/html",
                    use_container_width=True
                )
            
            st.markdown("---")
            
            # Sección 4: Descargar Hora Pico (TXT)
            st.markdown("#### Descargar Información")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                hora_pico_txt = resultados['hora_pico'].encode('utf-8')
                st.download_button(
                    label="Hora Pico (TXT)",
                    data=hora_pico_txt,
                    file_name="hora_pico.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            # Mostrar hora pico
            st.success(f"**{resultados['hora_pico']}**")
