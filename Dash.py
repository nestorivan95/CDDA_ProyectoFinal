import pandas as pd
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import ModelDash as Model # Importar las funciones del archivo Model.py

# Cargar el DataFrame desde el archivo
df = pd.read_csv('data/pumps_cleaned.csv')

# Crear la app de Dash con un tema Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Visualización de Pozos - Tanzania"

app.layout = dbc.Container([
    html.H1("🌍 Explorando Pozos en Tanzania", style={'text-align': 'center', 'color': '#2c3e50'}),
    html.Hr(),

    # Fila de estadísticas clave
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Pozos Funcionales", style={'text-align': 'center'}),
                dbc.CardBody(html.H4(id='functional-count', style={'text-align': 'center', 'color': 'green'}))
            ], style={'height': '100%'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Pozos en Reparación", style={'text-align': 'center'}),
                dbc.CardBody(html.H4(id='repair-count', style={'text-align': 'center', 'color': 'orange'}))
            ], style={'height': '100%'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Pozos No Funcionales", style={'text-align': 'center'}),
                dbc.CardBody(html.H4(id='non-functional-count', style={'text-align': 'center', 'color': 'red'}))
            ], style={'height': '100%'})
        ], width=4),
    ], className="mb-4"),

    # Fila de filtros
    dbc.Row([
        dbc.Col([
            html.Label("Seleccione un año:", className="form-label"),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': 'Todos', 'value': ''}] + 
                         [{'label': str(int(year)), 'value': int(year)} for year in sorted(df['construction_year_imputed'].dropna().unique())],
                value='',
                className="form-select"
            ),
        ], width=2),
         dbc.Col([
            html.Label("Estado del Pozo:", className="form-label"),
            dcc.Dropdown(
                id='status-group',
                options=[{'label': 'Todos', 'value': ''}] + 
                         [{'label': status, 'value': status} for status in sorted(df['status_group'].dropna().unique())],
                value='',
                className="form-select"
            ),
        ], width=2),  
        dbc.Col([
            html.Label("Calidad del agua:", className="form-label"),
            dcc.Dropdown(
                id='water-quality',
                options=[{'label': 'Todos', 'value': ''}] + 
                         [{'label': quality, 'value': quality} for quality in sorted(df['quality_group'].dropna().unique())],
                value='',
                className="form-select"
            ),
        ], width=2),
        dbc.Col([
            html.Label("Fuente de agua:", className="form-label"),
            dcc.Dropdown(
                id='source',
                options=[{'label': 'Todos', 'value': ''}] + 
                         [{'label': source, 'value': source} for source in sorted(df['source'].dropna().unique())],
                value='',
                className="form-select"
            ),
        ], width=2),
        dbc.Col([
            html.Label("Región:", className="form-label"),
            dcc.Dropdown(
                id='region',
                options=[{'label': 'Todos', 'value': ''}] + 
                         [{'label': region, 'value': region} for region in sorted(df['region'].dropna().unique())],
                value='',
                className="form-select"
            ),
        ], width=2),
        dbc.Col([
            html.Label("Rango de edad del pozo:", className="form-label"),
            dcc.RangeSlider(
                id='well-age',
                min=0,
                max=70,
                step=5,
                marks={i: str(i) for i in range(0, 101, 20)},
                tooltip={"placement": "bottom", "always_visible": True},
                value=[0, 70]
            ),
        ], width=2),
    ], className="mb-4"),

    # Fila de gráficos
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='map', style={'height': '300px'}),
        ], width=9),
        dbc.Col([
            dcc.Graph(id='pie-chart', style={'height': '300px'}),
        ], width=3),
    ], className="mb-4"),

    # Gráfico de líneas en la parte inferior
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='damaged-over-time', style={'height': '300px'}),
        ], width=12),
    ]),
], fluid=True)

# Callbacks para actualizar los números clave
@app.callback(
    [Output('functional-count', 'children'),
     Output('repair-count', 'children'),
     Output('non-functional-count', 'children')],
    [Input('year-dropdown', 'value')]
)
def update_counts(year):
    year = None if year == '' else year
    filtered_df = Model.filter_wells_for_plot(
        df,
        construction_year=year,
    )
    functional = filtered_df[filtered_df['status_group'] == 'functional'].shape[0]
    needs_repair = filtered_df[filtered_df['status_group'] == 'functional needs repair'].shape[0]
    non_functional = filtered_df[filtered_df['status_group'] == 'non functional'].shape[0]
    return functional, needs_repair, non_functional



# Callback para el gráfico de pozos dañados y funcionales
@app.callback(
    Output('damaged-over-time', 'figure'),
    Input('damaged-over-time', 'id')
)
def update_damaged_chart(_):
    functional_dict, non_functional_dict = Model.wells_by_year(df)
    functional_df = pd.DataFrame(list(functional_dict.items()), columns=['Year', 'Count'])
    functional_df['Status'] = 'Functional'

    non_functional_df = pd.DataFrame(list(non_functional_dict.items()), columns=['Year', 'Count'])
    non_functional_df['Status'] = 'Non Functional'

    combined_df = pd.concat([functional_df, non_functional_df])
    fig = px.line(combined_df, x='Year', y='Count', color='Status', title="Pozos Funcionales y Dañados a lo Largo del Tiempo")
    fig.update_layout(yaxis_title="Número de Pozos")
    return fig

# Callback para actualizar el mapa
@app.callback(
    Output('map', 'figure'),
    [Input('water-quality', 'value'),
     Input('region', 'value'),
     Input('well-age', 'value'),
     Input('status-group', 'value'),
     Input('year-dropdown', 'value'),
     Input('source', 'value')]
)
def update_map(water_quality, region, well_age, status_group, construction_year, source):
    # Cambiar entradas vacías ('') a None
    water_quality = None if water_quality == '' else water_quality
    region = None if region == '' else region
    status_group = None if status_group == '' else status_group
    construction_year = None if construction_year == '' else construction_year
    source = None if source == '' else source

    # Filtrar el DataFrame usando la función del modelo
    filtered_df = Model.filter_wells_for_plot(
        df,
        water_quality=water_quality,
        region=region,
        well_age=well_age,
        status_group=status_group,
        construction_year=construction_year,
        source=source
    )
    
    # Crear el mapa con los datos filtrados
    fig = px.scatter_mapbox(
        filtered_df,
        lat='latitude',
        lon='longitude',
        color='status_group',
        mapbox_style='open-street-map',
        title="Mapa de Pozos - Tanzania",
        height=600,
        zoom=4,
        center={"lat": -12, "lon": 35.0},  # Centro en Tanzania
        color_discrete_map={'functional': 'green', 'non functional': 'red', 'functional needs repair':'yellow'}
    )
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('water-quality', 'value'),
     Input('region', 'value'),
     Input('well-age', 'value'),
     Input('status-group', 'value'),
     Input('year-dropdown', 'value'),
     Input('source', 'value')]
)
def update_pie_chart(water_quality, region, well_age, status_group, construction_year, source):
    # Cambiar entradas vacías ('') a None
    water_quality = None if water_quality == '' else water_quality
    region = None if region == '' else region
    status_group = None if status_group == '' else status_group
    construction_year = None if construction_year == '' else construction_year
    source = None if source == '' else source

    # Filtrar el DataFrame usando la función del modelo
    filtered_df = Model.filter_wells_for_plot(
        df,
        water_quality=water_quality,
        region=region,
        well_age=well_age,
        status_group=status_group,
        construction_year=construction_year,
        source=source
    )

    # Calcular porcentajes
    counts = filtered_df['status_group'].value_counts()

    # Personalizar colores
    color_map = {
        'functional': 'green',
        'functional needs repair': 'yellow',
        'non functional': 'red'
    }

    # Crear gráfico de pastel
    fig = px.pie(
        names=counts.index,
        values=counts.values,
        title="Distribución de Pozos por Estado",
        color=counts.index,  # Asignar colores basados en los nombres
        color_discrete_map=color_map  # Mapear los nombres a colores específicos
    )

    # Ajustar la posición de la leyenda
    fig.update_layout(
        legend=dict(
            orientation='h',  # Leyenda horizontal
            yanchor='top',  # Anclar en la parte superior
            y=-0.2,  # Ubicarla un poco debajo del gráfico
            xanchor='center',  # Centrar horizontalmente
            x=0.5  # Colocar en el centro del gráfico
        )
    )

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)