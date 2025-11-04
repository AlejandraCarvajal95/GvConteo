import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def generar_grafico_torta(total_autos, total_motos, total_mio, total_tpc, total_camiones, total_mixtos, total_bicicletas):
    # Establecer la fuente de letra Arial Narrow
    font_family = "Arial Narrow, sans-serif"

    # Estableciendo el valor para el segundo gráfico de torta 'Otros'
    total_otros = total_mio + total_tpc + total_camiones + total_bicicletas
    total_general = total_autos + total_motos + total_otros

    # Estableciendo las etiquetas de ambos gráficos (primario y secundario)
    labels_principales = ['Autos', 'Motos', 'Otros']
    labels_secundarios = ['Mio', 'TPC', 'Camiones', 'Bicicletas']

    # Estableciendo los valores para ambos gráficos
    values_principales = [total_autos, total_motos, total_otros]

    # Escalar los valores del gráfico secundario para que representen su proporción en "Otros"
    # pero reflejando su proporción en el total general
    
    #values_secundarios = [round(v / total_general * 100, 1) for v in [total_mio, total_tpc, total_camiones, total_bicicletas]]
    values_secundarios = [v / total_general * 100 for v in [total_mio, total_tpc, total_camiones, total_bicicletas]]

    # Estableciendo los colores para ambos gráficos
    colores_primarios = ["#CCCCFF", "#ED7D31", "#4472C4"]
    colores_secundarios = ["#264478", "#FFC000", "#A5A5A5", "#70AD47"]

    # Crear subgráficos
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]], column_widths=[0.6, 0.25])

    # Añadir la primera gráfica de torta (gráfico principal)
    fig.add_trace(go.Pie(labels=labels_principales, values=values_principales, textfont_size=16,
                         textinfo='label+percent', direction='clockwise', showlegend=False,
                         marker=dict(colors=colores_primarios), title='(a)', pull=[0, 0, 0.2]), 1, 1)

    # Añadir la segunda gráfica de torta (gráfico secundario)
    fig.add_trace(go.Pie(labels=labels_secundarios, values=values_secundarios, textfont_size=16,
                         texttemplate='%{label}<br>%{value:.1f}%', direction='clockwise', showlegend=False,
                         marker=dict(colors=colores_secundarios), title='OTROS (b)', pull=[0.1, 0.1, 0.1, 0.1]), 1, 2)

    # Ajustar la rotación inicial del gráfico en 45 grados para ambos gráficos
    fig.update_traces(rotation=90)

    # Cambiar la fuente de letra en el layout
    fig.update_layout(font=dict(family=font_family, size=12))


    # Ajustar los márgenes de los gráficos
    fig.update_layout(margin=dict(l=30, r=200, t=50, b=50))

    return fig


def generar_grafico_barras_apiladas(df_suma_por_hora):
   
    # Definir los colores para cada vehículo
    colores_vehiculos = {
        "AUTOS": "#ED7D31", #naranja
        "MOTOS": "#FFC000", #amarillo
        "MIO": "#264478",
        "TPC": "#4472C4", #azul
        "CAMIONES": "#A5A5A5",  #gris
        "BICICLETAS": "#70AD47" #verde
    }

    # Crear el gráfico de barras
    fig = px.bar(df_suma_por_hora,
                x=df_suma_por_hora['rango_15_min'],
                y=["AUTOS", "MOTOS", "MIO", "TPC", "CAMIONES", "BICICLETAS"],
                color_discrete_map=colores_vehiculos)

    # Agregar una línea punteada para la columna 'mixtos'
    fig.add_trace(go.Scatter(x=df_suma_por_hora['rango_15_min'], y=df_suma_por_hora['MIXTOS'],
                            mode='lines', line=dict(color='black', dash='dash'), name='MIXTOS'))

    # Cambiar la fuente de letra del título y de los ejes a Arial Narrow
    fig.update_layout(font=dict(family="Arial Narrow, sans-serif", size=12))

    # Girar los labels del eje x 180 grados
    fig.update_xaxes(tickangle=-90)

    # Cambiar el título del eje Y
    fig.update_yaxes(title_text="Volúmenes vehiculares")
    
   # Retornar el gráfico para Streamlit
    return fig

def generar_grafico_barras(df_suma_por_hora):
    # Encontrar el índice del valor máximo en la columna "MIXTOS"
    indice_max = df_suma_por_hora["MIXTOS"].idxmax()
   
    # Obtener el valor máximo de la columna "MIXTOS"
    valor_max = df_suma_por_hora["MIXTOS"].max()

    # Crear el gráfico de barras
    fig = go.Figure()

    # Agregar las barras al gráfico
    fig.add_trace(go.Bar(
        x=df_suma_por_hora['rango_15_min'],
        y=df_suma_por_hora["MIXTOS"],
        marker_color="lightgrey"
    ))

    # Agregar etiqueta en la columna de mayor valor
    fig.add_annotation(
        x=df_suma_por_hora.loc[indice_max, 'rango_15_min'],  # Ubicación en el eje x
        y=valor_max,  # Ubicación en el eje y
        text=f"Hora pico: {valor_max}",  # Texto de la etiqueta
        showarrow=True,
        arrowhead=1
    )

    # Actualizar el diseño del gráfico
    fig.update_layout(
        xaxis=dict(
            title="Rango hora",
            tickangle=-90
        ),
        yaxis=dict(
            title="Volúmenes vehiculares mixtos"
        ),
        font=dict(
            family="Arial Narrow, sans-serif",
            size=12
        )
    )

    # Retornar el gráfico para Streamlit
    return fig