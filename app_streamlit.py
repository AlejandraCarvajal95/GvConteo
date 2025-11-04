"""
GRUPOVIALAPP - Análisis de Aforos Vehiculares
Aplicación moderna con Streamlit
"""

import streamlit as st
import sys
import os

# Configurar el path para importar módulos locales
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)

# Configuración de la página
st.set_page_config(
    page_title="GRUPOVIAL - Análisis de Aforos",
    page_icon="assets/logogv.png",  # Logo como favicon
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importar la página de análisis
from streamlit_app.pages import analizar_db

def main():
    """Función principal de la aplicación"""
    
    # Estilos CSS personalizados para coincidir con el logo de GRUPOVIAL
    st.markdown("""
        <style>
        /* Color del sidebar */
        [data-testid="stSidebar"] {
            background-color: #2C2C2C;
        }
        
        /* Texto del sidebar */
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        
        /* Título principal con acento rojo */
        .main h1 {
            color: #212529;
            border-bottom: 4px solid #E63946;
            padding-bottom: 10px;
        }
        
        /* Tabs con estilo profesional */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #F8F9FA;
            border-radius: 4px 4px 0 0;
            padding: 10px 20px;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #E63946;
            color: white;
        }
        
        /* Botones de descarga con hover mejorado */
        .stDownloadButton > button {
            border-radius: 6px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(230, 57, 70, 0.3);
        }
        
        /* Métricas con estilo */
        [data-testid="stMetricValue"] {
            color: #E63946;
            font-weight: 600;
        }
        
        /* Alerts y mensajes */
        .stAlert {
            border-radius: 8px;
        }
        
        /* Info boxes */
        .stInfo {
            background-color: #FFF5F5;
            border-left: 4px solid #E63946;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Título principal
    st.title("GRUPOVIAL - Sistema de Análisis de Aforos Vehiculares")
    st.markdown("---")
    
    # Sidebar para navegación (por si en el futuro agregas más páginas)
    with st.sidebar:
        # Logo en el sidebar
        st.image("assets/logogv.png", use_container_width=True)
        st.markdown("---")
        st.header("Navegación")
        
        # Por ahora solo una página, pero preparado para más
        page = st.radio(
            "Selecciona una opción:",
            ["Analizar DB"],
            label_visibility="collapsed"
        )
    
    # Mostrar la página seleccionada
    if page == "Analizar DB":
        analizar_db.show()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### Información
    **Versión:** 2.0  
    **Fecha:** Octubre 2025  
    **Tecnología:** Streamlit + Pandas + Plotly
    """)

if __name__ == "__main__":
    main()
