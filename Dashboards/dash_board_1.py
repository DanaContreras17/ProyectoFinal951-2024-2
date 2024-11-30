import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd


file_path = 'datasets/libros_limpios.csv'
libros_df = pd.read_csv(file_path)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])



def grafica_pastel_formato(df):
    formato_count = df['Formato'].value_counts().reset_index()
    formato_count.columns = ['Formato', 'Cantidad']

    fig = px.pie(formato_count, names="Formato", values="Cantidad",
                 title="Distribución de Libros por Formato",
                 color="Formato",
                 color_discrete_map={
                     'Tapa dura': '#800080',
                     'Multiformato': '#9b4dca',
                     'Tapa blanda': '#af69cd',
                     'Digital': '#c8a2d3'
                 })
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color="white"),
        title_font=dict(size=24, family="Arial, sans-serif", color="white", weight="bold"),
        margin=dict(t=40, b=40, l=40, r=40),
        shapes=[dict(type='rect', x0=0, x1=1, y0=0, y1=1, line=dict(color="white", width=2))]
    )
    return fig



def grafica_barras_precio(df):
    fig = px.histogram(df, x="Precio", nbins=20,
                       title="Distribución de Precios de Libros",
                       labels={"Precio": "Precio de Libro"},
                       color_discrete_sequence=['#9b4dca'])
    fig.update_layout(
        xaxis_title="Precio",
        yaxis_title="Número de Libros",
        template="plotly_dark",
        font=dict(color="white"),
        bargap=0.2,
        title_font=dict(size=24, family="Arial, sans-serif", color="white", weight="bold"),
        margin=dict(t=40, b=40, l=40, r=40),
        plot_bgcolor='black',
        paper_bgcolor='black',
        shapes=[dict(type='rect', x0=0, x1=1, y0=0, y1=1, line=dict(color="white", width=2))]
    )
    return fig



def grafica_precio_formato_editorial(df):
    fig = px.bar(df, x="Editorial", y="Precio", color="Formato",
                 title="Distribución de Precios por Formato y Editorial",
                 labels={"Precio": "Precio", "Editorial": "Editorial", "Formato": "Formato"},
                 template="plotly_dark", barmode='group',
                 color_discrete_map={
                     'Tapa dura': '#800080',  # Morado oscuro
                     'Multiformato': '#9b4dca',  # Morado medio
                     'Tapa blanda': '#af69cd',  # Morado claro
                     'Digital': '#c8a2d3'  # Lavanda claro
                 })
    fig.update_layout(
        title_font=dict(size=24, family="Arial, sans-serif", color="white", weight="bold"),
        margin=dict(t=40, b=40, l=40, r=40),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color="white"),
        shapes=[dict(type='rect', x0=0, x1=1, y0=0, y1=1, line=dict(color="white", width=2))],
        xaxis=dict(tickangle=45),
        yaxis=dict(tickprefix="$")
    )
    return fig



def tarjeta_filtro():
    control = dbc.Card(
        [
            html.Div([
                dbc.Label("Selecciona Formato para las Gráficas", style={"color": "black"}),
                dcc.Dropdown(
                    options=[{'label': formato, 'value': formato} for formato in libros_df['Formato'].unique()],
                    value=libros_df['Formato'].unique()[0],
                    id='formato-dropdown',
                    style={
                        'width': '100%',
                        'background-color': '#9b4dca',  # Color de fondo morado
                        'color': 'black',  # Letras negras
                        'border-radius': '10px',
                        'border': '1px solid #888',
                        'box-shadow': '0 4px 6px rgba(0,0,0,0.2)',
                        'font-family': 'Arial, sans-serif',
                        'font-size': '16px',
                        'padding': '10px'
                    }
                )
            ]),

            html.Div([
                dbc.Label("Filtrar Gráfica de Distribución por Formato", style={"color": "black"}),
                dcc.Dropdown(
                    options=[{'label': formato, 'value': formato} for formato in libros_df['Formato'].unique()],
                    value='Tapa dura',
                    id='formato-dropdown-2',
                    style={
                        'width': '100%',
                        'background-color': '#af69cd',
                        'color': 'black',
                        'border-radius': '10px',
                        'border': '1px solid #888',
                        'box-shadow': '0 4px 6px rgba(0,0,0,0.2)',
                        'font-family': 'Arial, sans-serif',
                        'font-size': '16px',
                        'padding': '10px'
                    }
                )
            ])
        ],
        style={
            'background-color': '#f1e0ff',
            'padding': '15px',
            'border-radius': '10px',
            'box-shadow': '0 4px 8px rgba(0,0,0,0.1)'
        }
    )
    return control



def dashboard():

    fig_editoriales = grafica_barras_precio(libros_df)
    fig_autores = grafica_pastel_formato(libros_df)
    fig_precio_editorial = grafica_precio_formato_editorial(libros_df)


    body = dbc.Container([

        # Fila de título
        dbc.Row([
            dbc.Col(html.H1("Análisis de Precios y Formato de Libros", className="text-center"),
                    style={'background-color': '#800080', 'padding': '20px', 'border-radius': '10px',
                           'color': 'white', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'font-weight': 'bold'}, width=12)
        ], style={'margin-bottom': '30px'}),


        dbc.Row([
            dbc.Col(html.Div([tarjeta_filtro()]), width=4),
            dbc.Col(
                html.Div([
                    dbc.Row(dcc.Graph(figure=fig_editoriales, id="figLine")),
                    dbc.Row(dcc.Graph(figure=fig_precio_editorial, id="figBox"))
                ]), width=8
            ),
        ], style={'margin-bottom': '30px'}),


        dbc.Row([
            dbc.Col(dcc.Graph(id="grafica-pastel-formato", figure=fig_autores), width=12)
        ], style={'padding-top': '20px'})
    ], fluid=True, style={'background-color': '#2e1a47', 'padding': '30px', 'border-radius': '10px'})

    return body



def callbacks_d1(app):
    @app.callback(
        Output('figLine', 'figure'),
        Output('figBox', 'figure'),
        Output('grafica-pastel-formato', 'figure'),
        Input('formato-dropdown', 'value'),
        Input('formato-dropdown-2', 'value')
    )
    def update_grafica(formato_seleccionado, formato_seleccionado_2):
        df_filtrado_1 = libros_df[libros_df['Formato'] == formato_seleccionado]
        df_filtrado_2 = libros_df[libros_df['Formato'] == formato_seleccionado_2]

        df_filtrado_final = pd.concat([df_filtrado_1, df_filtrado_2]).drop_duplicates()

        fig_editoriales = grafica_barras_precio(df_filtrado_final)
        fig_autores = grafica_pastel_formato(df_filtrado_final)
        fig_precio_editorial = grafica_precio_formato_editorial(df_filtrado_final)

        return fig_editoriales, fig_precio_editorial, fig_autores

    return app

if __name__ == '__main__':
    app.layout = dashboard()
    app.run_server(debug=True)