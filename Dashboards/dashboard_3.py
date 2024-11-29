import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

def dashboard():
    df = pd.read_csv('datasets/libros_limpios.csv')

    autor_count = df['Nombre_autor'].value_counts().reset_index()
    autor_count.columns = ['Nombre_autor', 'Cantidad_libros']


    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    fig_formatos = px.bar(df, x='Formato', title='Comparativa de Formatos de Libros', color='Formato',
                          template="plotly_dark")

    fig_autores = px.bar(autor_count, x='Nombre_autor', y='Cantidad_libros',
                         title='Análisis de Autores Populares', color='Cantidad_libros', template="plotly_dark")

    app.layout = dbc.Container([
        html.H3('Dashboard de Análisis de Formatos y Autores', style={'textAlign': 'center'}),

        dbc.Row([
            dbc.Col([
                html.Label("Selecciona un formato", style={'color': 'white'}),
                dcc.Dropdown(
                    id='formato-dropdown',
                    options=[{'label': formato, 'value': formato} for formato in df['Formato'].unique()],
                    value=[],
                    multi=True,
                    placeholder="Selecciona un formato"
                ),
            ], width=4),
            dbc.Col([
                html.Label("Selecciona un autor", style={'color': 'white'}),
                dcc.Dropdown(
                    id='autor-dropdown',
                    options=[{'label': autor, 'value': autor} for autor in df['Nombre_autor'].unique()],
                    value=[],
                    multi=True,
                    placeholder="Selecciona un autor"
                ),
            ], width=4),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='grafico-formatos',
                    figure=fig_formatos
                ),
            ], width=6),

            dbc.Col([
                dcc.Graph(
                    id='grafico-autores',
                    figure=fig_autores
                ),
            ], width=6)
        ])
    ])

    @app.callback(
        [dash.dependencies.Output('grafico-formatos', 'figure'),
         dash.dependencies.Output('grafico-autores', 'figure')],
        [dash.dependencies.Input('formato-dropdown', 'value'),
         dash.dependencies.Input('autor-dropdown', 'value')]
    )
    def update_graph(selected_formats, selected_authors):
        filtered_df_formatos = df[df['Formato'].isin(selected_formats)] if selected_formats else df
        filtered_df_autores = autor_count[autor_count['Nombre_autor'].isin(selected_authors)] if selected_authors else autor_count

        fig_formatos = px.bar(filtered_df_formatos, x='Formato', title='Comparativa de Formatos de Libros', color='Formato',
                              template="plotly_dark")

        fig_autores = px.bar(filtered_df_autores, x='Nombre_autor', y='Cantidad_libros',
                             title='Análisis de Autores Populares', color='Cantidad_libros', template="plotly_dark")

        return fig_formatos, fig_autores

    if __name__ == '__main__':
        app.run_server(debug=True)

if __name__ == '__main__':
    dashboard()
