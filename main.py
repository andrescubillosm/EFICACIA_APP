import dash
import dash_labs as dl
from dash import Dash, html, dcc, callback
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from dash.dependencies import Input, Output
from folium.plugins import MarkerCluster
import pandas as pd
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
from dash.exceptions import PreventUpdate
from folium import plugins
#se cambia plantilla por una mas similar en colores a la de eficacia ver https://bootswatch.com/
load_figure_template("litera")

url = 'https://raw.githubusercontent.com/andrescubillosm/grupo_108/main/EDA/geodata.csv'

gea = pd.read_csv(url, delimiter=";")
gea.head()

gea["Lat"] = gea["Lat"].apply(lambda x: x.replace(',', '.'))
gea["Lon"] = gea["Lon"].apply(lambda x: x.replace(',', '.'))
gea['Lat'] = gea['Lat'].astype(float)
gea['Lon'] = gea['Lon'].astype(float)


# función del mapa
def mapa():
    from folium.plugins import MarkerCluster

    latitude = 5
    longitude = -73

    map_tiendas = folium.Map(location=[latitude, longitude], zoom_start=6, tiles="Stamen Toner")

    marker_cluster = MarkerCluster().add_to(map_tiendas)

    for Lat, Lon, Ciudad, Cadena in list(
            zip(
                gea["Lat"],
                gea["Lon"],
                gea["Ciudad"],
                gea["Cadena"]
            )
    ):
        folium.Marker(location=(Lat, Lon),
                      popup=f"lat: {Lat}, lon : {Lon}, ciudad: {Ciudad}, cadena : {Cadena}").add_to(marker_cluster)

    minimap = plugins.MiniMap()
    map_tiendas.add_child(minimap)

    return map_tiendas

# imprime el mapa y lo guarda para us posterior interacción
location_map = mapa()
location_map.save('mapa_tiendas.html')


# DATOS DUMMY




map_fig = location_map

app = Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX]) # CAMBIAR EL STILO DE BOOTSTRAP


# Encabezado y logo y se llama desde el layout
heading = html.Div([
  html.Br(),
  html.Img(src='https://www.eficacia.com.co/wp-content/uploads/2020/05/logo.svg'),
  html.H1('Out of Stock Eficacia', className="bg-primary text-white p-2",
          style={'text-align':'center', 'font-size':36, 'marginTop':40,'marginBottom':40,}),
  ])


# esta varible corresponde al mapa y se llama desde el layout
mapa = html.Div(
    [dbc.Container ([
        html.H3('Retail Market Mapping', style={'font-size':22}),
        dbc.Row(
            [
            # ESta primera columana corresponde al mapa
                            html.Iframe(id='map',title= 'mapa', srcDoc = open('mapa_tiendas.html', 'r').read(),
                                width='auto', height='500'# tamaño del mapa
                                ),
            ],
        )],
            className="mt-2",

),])

# DATOS DUMMY Y FIGURAS

figure1 = dcc.Graph(
    figure={
        'data': [
            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
        ],
        'layout': {
            'title': 'Dash Data Visualization'
        }
    }
)

figure2 = dcc.Graph(
    figure={
        'data': [
            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
        ],
        'layout': {
            'title': 'Dash Data Visualization'
        }
    }
)



def make_figure(mean=0, std=1, template="pulse"):
    np.random.seed(2020)
    data1 = np.random.normal(mean, std, size=500)
    return px.histogram(data1, nbins=30, range_x=[-10, 10])


layout = html.Div(
    [
        dcc.Graph(id="histograms-graph", figure=make_figure()),
        html.P("Mean:"),
        dcc.Slider(
            id="histograms-mean", min=-3, max=3, value=1, marks={-3: "-3", 3: "3"}
        ),
        html.P("Standard Deviation:"),
        dcc.Slider(id="histograms-std", min=1, max=3, value=1, marks={1: "1", 3: "3"}),
    ]
)

fig = dcc.Graph(id='ejemplo',
    figure={
      'data': [
        {'x': [1, 2, 3, 4], 'y': [1, 8, 3, 7], 'type': 'line', 'name': 'Bicicletas'},
        {'x': [1, 2, 3, 4], 'y': [5, 2, 8, 8], 'type': 'bar', 'name': 'Bicicletas electricas'},
        ],
      'layout': {
      'title': 'Ejemplo básico en Dash'
        }
      })

fig2 = dcc.Graph(id='ejemplo2',
    figure={
      'data': [
        {'x': [1, 2, 3, 8], 'y': [1, 8, 3, 7], 'type': 'line', 'name': 'Bicicletas'},
        {'x': [1, 2, 3, 4], 'y': [5, 2, 8, 8], 'type': 'bar', 'name': 'Bicicletas electricas'},
        ],
      'layout': {
      'title': 'Ejemplo básico en Dash'
        }
      })

#tablas dinamica por cadena 
# contador de cadenas por regional 
pvTable = pd.pivot_table(gea, index=['Cadena'], columns=["Regional"], aggfunc='count', dropna= True, margins =True, observed= True, sort=True)

#ejemplos para graficos de columnas 
#trace1 = go.Bar(x=pv.index, y=pv[('Quantity', 'declinada')], name='Declinada')
#trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pendiente')], name='Pendiente')
#trace3 = go.Bar(x=pv.index, y=pv[('Quantity', 'presentada')], name='Presentada')
#trace4 = go.Bar(x=pv.index, y=pv[('Quantity', 'ganada')], name='Ganada')

#porbablemente este no vaya al final 
pvTable2 = pd.pivot_table(gea, index=['Cadena', 'Ciudad'], columns=["DiaEntregaPedido"], aggfunc='sum', dropna= True, margins =True, observed= True,sort=True)

#este tiene mejor resultado pero tiene muchas columnas 
pvTable3 = pd.pivot_table(gea, index=['Depto','Ciudad'], columns=["Cadena"], dropna= True, margins =True, sort=True)

#evaluar si funciona o no 
pvTable4 = pd.pivot_table(gea, index=['Regional','Cadena'], columns=["Formato"], aggfunc='count', dropna= True, margins =True, observed= True,sort=True)
# en la esta se desarrolla el layout por partes invocando variables

app.layout = html.Div([dbc.Container([heading], fluid=True),
             html.Div([dbc.Container([mapa], fluid=True)]),
             dbc.Container([
              # graficas en 2 columnas
                           dbc.Row(
                                   [
                                       dbc.Col([figure1],lg=6),
                                       dbc.Col([figure2],lg=6),
                                       dbc.Col([fig]),
                                       dbc.Col([layout],
                               ),
                       ]),
                       ])])


if __name__ == "__main__":
    app.run_server(debug=True)

