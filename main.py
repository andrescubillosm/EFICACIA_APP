import dash
import dash_labs as dl
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster
import pandas as pd
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

load_figure_template("minty")

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


    return map_tiendas

# imprime el mapa y lo guarda para us posterior interacción
location_map = mapa()
location_map.save('mapa_tiendas.html')


# DATOS DUMMY




map_fig = location_map

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY]) # CAMBIAR EL STILO DE BOOTSTRAP


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
                                width='auto', height='500',# tamaño del mapa
                                style={"border":"1px black solid"}),
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


# en la esta se desarrolla el layout por partes invocando variables

app.layout = html.Div([dbc.Container([heading], fluid=True),
             dbc.Container([mapa], fluid=True),
             dbc.Container([
             html.Div( # graficas en 2 columnas
                           [dbc.Row(
                                   [
                                       dbc.Col([figure1]),
                                       dbc.Col([figure2]),
                                   ],
                               ),
                           ]
                       )]),
             html.Div(  # graficas en 2 columnas
                           [dbc.Row(
                                   [
                                       dbc.Col([fig]),
                                       dbc.Col([fig2])
                                   ],
                               ),
                           ]
                       )
])



if __name__ == "__main__":
    app.run_server(debug=True)

