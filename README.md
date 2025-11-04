# GRUPOVIAL - Análisis de Tráfico Vehicular

Aplicación web para el análisis de datos de conteo vehicular. Permite cargar archivos CSV/Excel con registros de tráfico, aplicar filtros personalizados y generar visualizaciones interactivas y reportes detallados.

---

## Índice
1. [Instalación](#instalación)
2. [Requisitos Previos](#requisitos-previos)
3. [Uso](#uso)
4. [Estructura del Proyecto](#estructura-del-proyecto)

---

## Instalación

```bash
# Clona este repositorio
git clone https://github.com/AlejandraCarvajal95/GRUPOVIALAPP.git

# Navega al directorio del proyecto
cd GRUPOVIALAPP

# Crea un entorno virtual (recomendado)
python -m venv .venv

# Activa el entorno virtual
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate

# Instala las dependencias
pip install -r requirements.txt
```

---

## Requisitos Previos
- Python 3.8 o superior
- Git
- Dependencias listadas en `requirements.txt`

---

## Uso

```bash
# Activa el entorno virtual
.venv\Scripts\activate

# Ejecuta la aplicación
streamlit run app_streamlit.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

---

## Estructura del Proyecto

```
GRUPOVIALAPP/
│
├── app_streamlit.py            # Punto de entrada principal de la aplicación web
│
├── streamlit_app/              #  Módulo de la interfaz Streamlit
│   ├── __init__.py
│   ├── utils_streamlit.py      # Funciones adaptadoras entre Streamlit y lógica de negocio
│   └── pages/                  # Páginas de la aplicación
│       ├── __init__.py
│       └── analizar_db.py      # Página principal de análisis con filtros y visualizaciones
│
├── conteo/                     # Módulo de lógica de negocio (análisis de datos)
│   ├── __init__.py
│   ├── config.py               # Configuración global (hora pico)
│   ├── database_reader.py      # Lectura y carga de archivos CSV/Excel
│   ├── data_filter.py          # Carga de filtros disponibles desde datos
│   ├── df_generator.py         # Generación de tablas agregadas (15min, hora)
│   └── graph_generator.py      # Creación de gráficos Plotly (torta, barras, apiladas)
│
├── assets/                     # Recursos visuales
│   └── logogv.png              # Logo de GRUPOVIAL
│
├── .streamlit/                 # Configuración de Streamlit
│   └── config.toml             # Tema personalizado con colores corporativos
│
├── .gitignore                  # Archivos excluidos del control de versiones
├── README.md                   # Documentación del proyecto
└── requirements.txt            # Dependencias de Python
```

---

## Módulos Principales

### `app_streamlit.py`
Archivo principal que inicializa la aplicación Streamlit, configura el tema, carga el logo y establece la navegación.

### `streamlit_app/pages/analizar_db.py`
Página principal con toda la funcionalidad:
- Carga de archivos CSV/Excel
- 7 categorías de filtros (Fecha, Hora, Digitador, Movimientos, Estación, Tipo, Intersección)
- Visualización de datos filtrados
- Generación de gráficos interactivos
- Exportación a Excel, HTML y ZIP

### `streamlit_app/utils_streamlit.py`
Funciones adaptadoras que conectan la interfaz Streamlit con la lógica de negocio:
- `cargar_archivo_db()` - Carga archivos desde Streamlit
- `obtener_filtros_disponibles()` - Extrae valores únicos para filtros
- `aplicar_filtros_seleccionados()` - Procesa filtros y genera análisis completo
- `exportar_a_excel()` - Exporta DataFrames a Excel
- `exportar_grafico_html()` - Exporta gráficos Plotly a HTML interactivo
- `crear_zip_completo()` - Genera paquete ZIP con todos los archivos de análisis

### `conteo/graph_generator.py`
Genera visualizaciones Plotly interactivas:
- `generar_grafico_torta()` - Distribución por tipo de vehículo
- `generar_grafico_barras()` - Vehículos totales por hora
- `generar_grafico_barras_apiladas()` - Distribución de vehículos por intervalo de 15 minutos

### `conteo/df_generator.py`
Crea tablas agregadas del análisis:
- `crear_tabla_rango_15min()` - Suma de vehículos cada 15 minutos
- `crear_tabla_rango_hora()` - Suma de vehículos por hora completa

### `conteo/database_reader.py`
Maneja la lectura de archivos:
- `leer_datos()` - Lee CSV/Excel y devuelve DataFrame
- `ajustar_direccion()` - Normaliza rutas de archivos

### `conteo/data_filter.py`
Extrae valores únicos de columnas para construir filtros dinámicos en la interfaz.

---

## Personalización

Los colores corporativos de GRUPOVIAL están configurados en `.streamlit/config.toml`:
- **Color primario**: `#E63946` (rojo GRUPOVIAL)
- **Fondo**: `#FFFFFF` (blanco)
- **Fondo secundario**: `#F8F9FA` (gris claro)
- **Sidebar**: `#2C2C2C` (gris oscuro)

---

## Notas

- Los archivos generados (.xlsx, .html, .zip) se excluyen automáticamente del repositorio (ver `.gitignore`)
- El logo debe estar en `assets/logogv.png` para mostrarse correctamente
- La aplicación guarda el estado en sesión para mantener filtros y datos cargados

