import streamlit      as st
import pandas         as pd
import plotly.express as px
# Definimos los parámetros de configuración de la aplicación
st.set_page_config(
  page_title            = "Dashboard Exportaciones", #Título de la página
  page_icon             = "📊", # Ícono
  layout                = "wide", # Forma de layout ancho o compacto
  initial_sidebar_state = "expanded" # Definimos si el sidebar aparece expandido o colapsado
)
# Definimos el titulo te la pagina
st.title("Subir un archivo CSV y visualizar datos")
# Input para subir el archivo
uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")
# Verifica que se haya seleccionado el archivo
if uploaded_file is not None:
  # Leer el archivo con pandas
  datos_archivo = pd.read_csv(uploaded_file)
  with st.sidebar:
    # Filtro de Mes
    filtro_mes     = st.selectbox('Mes',options=datos_archivo['Mes'].unique(),index=0)
    valor_asociado = datos_archivo.loc[datos_archivo['Mes'] == filtro_mes, 'Numero Mes'].values[0]
  # Obtemos el valor seleccionados para aplicar el filtro
  if filtro_mes:
    datos_archivo_filtro = datos_archivo[datos_archivo['Mes'] <= filtro_mes]
  # Obtenemos los datos del mes seleccionado
  mes_seleccionado = datos_archivo_filtro[datos_archivo_filtro['Mes'] == filtro_mes]
  # Obtenemos los datos del mes anterior
  if filtro_mes:
    if valor_asociado > 1:
      mes_anterior = datos_archivo_filtro[datos_archivo_filtro['Mes'] == datos_archivo.iloc[valor_asociado - 1]['Mes']]
    else:
      mes_anterior = datos_archivo_filtro[datos_archivo_filtro['Mes'] == filtro_mes]
  st.header('Tablero de control de Exportaciones e Importaciones')
  # Declaramos 2 columnas de igual tamaño
  c1,c2, = st.columns(2)
  # Cramos la grafica de variacion de exportaciones en la primer columna
  with c1:
    exp_mes_actual   = mes_seleccionado['Exportaciones'].sum()
    exp_mes_anterior = mes_anterior['Exportaciones'].sum()
    variacion        = exp_mes_anterior - exp_mes_actual
    st.metric(
      f"Exportaciones",
      f'{exp_mes_actual:,.0f} Toneladas',
      f'{variacion:,.0f}'
    )
  # Cramos la grafica de variacion de importaciones en la primer columna
  with c2:
    imp_mes_actual   = mes_seleccionado['Importaciones'].sum()
    imp_mes_anterior = mes_anterior['Importaciones'].sum()
    variacion        = imp_mes_actual - imp_mes_anterior
    st.metric(
      f"Importacioness",
      f'{imp_mes_actual:.0f} Toneladas',
      f'{variacion:.1f}'
    )
  # Declaramos 2 columnas en una proporción de 50% y 50%
  c1,c2 = st.columns([50,50])
  # Cramos la grafica de linea en la primer columna
  with c1:
    dfVentasMes = datos_archivo.groupby('Mes', sort=False).agg({'Exportaciones': 'sum'}).reset_index()
    fig = px.line(
        dfVentasMes,
        x     = 'Mes',
        y     = 'Exportaciones',
        title = 'Exportaciones por mes'
    )
    st.plotly_chart(fig, use_container_width=True)
  # Cramos la grafica de linea en la segunda columna
  with c2:
    dfVentasMes = datos_archivo.groupby('Mes', sort=False).agg({'Importaciones': 'sum'}).reset_index()
    fig = px.line(
        dfVentasMes,
        x     = 'Mes',
        y     = 'Importaciones',
        title = 'Importaciones por mes'
    )
    st.plotly_chart(fig, use_container_width=True)
  # Declaramos 2 columnas de igual tamaño
  c1,c2 = st.columns(2)  # Si solo necesitas una columna, usa una coma y asegúrate de que sea una tupla
  # Cramos la grafica de barras en la primer columna
  with c1:
    exportaciones_bar = datos_archivo.groupby('Mes', sort=False).agg({'Exportaciones': 'sum'}).reset_index()
    fig = px.bar(
      exportaciones_bar,
      x         = 'Mes',
      y         = 'Exportaciones',
      title     = f'Exportaciones por mes',
      color     = 'Mes',
      text_auto = ',.0f'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
   # Cramos la grafica de barras en la primer columna
  with c2:
    importaciones_bar = datos_archivo.groupby('Mes', sort=False).agg({'Importaciones': 'sum'}).reset_index()
    fig = px.bar(
      importaciones_bar,
      x         = 'Mes',
      y         = 'Importaciones',
      title     = f'Importaciones por mes',
      color     = 'Mes',
      text_auto = ',.0f'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
