import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Dash, callback, Input, Output

data = pd.read_csv("datasets/libros_limpios.csv")

def grafica_barras_editorial(data, start_idx, end_idx):
    editoriales_count = data['Editorial'].value_counts().iloc[start_idx:end_idx].reset_index()
    editoriales_count.columns = ['Editorial', 'Número de Libros']
    fig = px.bar(editoriales_count, x='Editorial', y='Número de Libros',
                 title=f"Top {start_idx + 1}-{end_idx} Editoriales con más Libros",
                 template="plotly_dark")
    fig.update_traces(marker=dict(color='#cca9dd'))
    fig.update_layout(bargap=0.6)
    return fig

def grafica_pastel_autores(data, start_idx, end_idx):
    autores_count = data['Nombre_autor'].value_counts().iloc[start_idx:end_idx].reset_index()
    autores_count.columns = ['Autor', 'Número de Libros']

    fig = px.pie(autores_count, names='Autor', values='Número de Libros',
                 title=f"Top {start_idx + 1}-{end_idx} Autores con más Libros",
                 template="plotly_dark")
    fig.update_traces(marker=dict(
        colors=['#e6ccef', '#cb9bde', '#af69cd', '#9032bb', '#7900ac', '#6d00a1', '#620096', '#56008c', '#4b0081',
                '#d29bfd']))
    return fig

def grafica_precio_autor_rango(rango_precio_autor):
    fig = px.bar(rango_precio_autor, x='Nombre_autor', y=['min', 'max'],
                 title="Rango de Precios por Autor (Top 10)",
                 template="plotly_dark",
                 labels={'min': 'Precio Mínimo', 'max': 'Precio Máximo'})
    fig.update_traces(
        marker=dict(color=['#e0aaff' for _ in range(len(rango_precio_autor))]),
        selector=dict(name='min')
    )
    fig.update_traces(
        marker=dict(color=['#3c096c' for _ in range(len(rango_precio_autor))]),
        selector=dict(name='max')
    )
    fig.update_layout(
        xaxis_title="Autor",
        yaxis_title="Precio",
        showlegend=True,
        margin=dict(l=0, r=0, t=40, b=40),
        plot_bgcolor="#000000",
        paper_bgcolor="#000000",
        barmode='group',
        xaxis={'categoryorder': 'total descending'}
    )
    return fig

def filtro_editoriales(data):
    top_editoriales_count = data['Editorial'].value_counts().head(30)
    num_grupos = len(top_editoriales_count) // 5 + (1 if len(top_editoriales_count) % 5 != 0 else 0)
    opciones = [{'label': f"Grupo {i + 1}", 'value': i} for i in range(num_grupos)]

    filtro = dbc.Card(
        [
            html.Div([
                dbc.Label("Selecciona un grupo de editoriales", style={"color": "white"}),
                dcc.Dropdown(
                    options=opciones,
                    value=0,
                    id="ddGrupoEditoriales",
                    style={"width": "200px", "color": "black", "backgroundColor": "#FFFFFF", "border": "1px solid #ccc"}
                )
            ])
        ],
        style={"width": "300px", "padding": "10px", "backgroundColor": "#444444"}
    )
    return filtro

def filtro_autores(data):
    top_autores_count = data['Nombre_autor'].value_counts().head(30)
    num_grupos = len(top_autores_count) // 5 + (1 if len(top_autores_count) % 5 != 0 else 0)
    opciones = [{'label': f"Grupo {i + 1}", 'value': i} for i in range(num_grupos)]

    filtro = dbc.Card(
        [
            html.Div([
                dbc.Label("Selecciona un grupo de autores", style={"color": "white"}),
                dcc.Dropdown(
                    options=opciones,
                    value=0,
                    id="ddGrupoAutores",
                    style={"width": "200px", "color": "black", "backgroundColor": "#FFFFFF", "border": "1px solid #ccc"}
                )
            ])
        ],
        style={"width": "300px", "padding": "10px", "backgroundColor": "#444444"}
    )
    return filtro

def dashboard():
    fig_editoriales = grafica_barras_editorial(data, 0, 5)
    fig_autores = grafica_pastel_autores(data, 0, 5)

    top_autores = data['Nombre_autor'].value_counts().head(10).index
    data_top_autores = data[data['Nombre_autor'].isin(top_autores)]
    rango_precio_autor = data_top_autores.groupby('Nombre_autor')['Precio'].agg(['min', 'max']).reset_index()
    fig_precio_autor = grafica_precio_autor_rango(rango_precio_autor)

    body = html.Div([
        dbc.Row([
            dbc.Col(html.Div([html.H3("Análisis de Editoriales y Autores", style={"color": "white", "textAlign": "center"}), html.Hr()]),
                    width=12, style={"backgroundColor": "#333333"}),
            dbc.Col(html.Div([filtro_editoriales(data), dcc.Graph(figure=fig_editoriales, id="figBar")]), width=6,
                    style={"backgroundColor": "#333333"}),
            dbc.Col(html.Div([filtro_autores(data), dcc.Graph(figure=fig_autores, id="figPie")]), width=6,
                    style={"backgroundColor": "#333333"})
        ]),
        dbc.Row([
            dbc.Col(html.Div([html.H3("Rango de Precios por Autor (Top 10)", style={"color": "white", "textAlign": "center"}), html.Hr()]),
                    width=5, style={"backgroundColor": "#333333"}),
            dbc.Col(html.Div([dcc.Graph(figure=fig_precio_autor, id="figPrecioAutor")]), width=8,
                    style={"backgroundColor": "#333333"})
        ])
    ], style={"background-color": "#333333", "padding": "20px"})

    return body

@callback(
    Output(component_id="figBar", component_property="figure"),
    Input(component_id="ddGrupoEditoriales", component_property="value")
)
def update_grafica_editoriales(grupo):
    start_idx = grupo * 5
    end_idx = (grupo + 1) * 5
    fig = grafica_barras_editorial(data, start_idx, end_idx)
    return fig

@callback(
    Output(component_id="figPie", component_property="figure"),
    Input(component_id="ddGrupoAutores", component_property="value")
)
def update_grafica_autores(grupo):
    start_idx = grupo * 5
    end_idx = (grupo + 1) * 5
    fig = grafica_pastel_autores(data, start_idx, end_idx)
    return fig

if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
    app.layout = dashboard()
    app.run_server(debug=True)
