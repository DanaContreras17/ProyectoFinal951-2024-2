import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from mysql.connector import connect, Error


def obtener_datos_mysql():
    try:

        conexion = connect(host="localhost", port="3306", user="root",
                           password="MezaG2004", database="libros_db")

        cursor = conexion.cursor()

        sql = """
        SELECT libros.titulo, autores.nombre AS autor, editoriales.nombre_editorial AS editorial,
               libros.formato, libros.precio
        FROM libros
        JOIN autores ON libros.id_autor = autores.id_autor
        JOIN editoriales ON libros.id_editorial = editoriales.id_editorial;
        """

        cursor.execute(sql)

        rows = cursor.fetchall()
        columnas = ["Nombre_libro", "Nombre_autor", "Editorial", "Formato", "Precio"]
        libros_df = pd.DataFrame(rows, columns=columnas)

        cursor.close()
        conexion.close()

        return libros_df

    except Error as e:
        print(f"Error: {e}")
        return None


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

libros_df = obtener_datos_mysql()

if libros_df is None:
    raise Exception("No se pudo obtener los datos desde la base de datos")


def grafica_pastel_formato(df):
    formato_count = df["Formato"].value_counts().reset_index()
    formato_count.columns = ["Formato", "Cantidad"]

    fig = px.pie(formato_count, names="Formato", values="Cantidad",
                 title="Distribución de Libros por Formato",
                 color="Formato",
                 color_discrete_map={
                     "Tapa dura": "#4B0082",  # Morado oscuro
                     "Multiformato": "#6A0DAD",  # Morado más oscuro
                     "Tapa blanda": "#800080",  # Morado más intenso
                     "Digital": "#9932CC"
                 })
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        title_font=dict(size=24, family="Arial, sans-serif", color="white", weight="bold"),
        margin=dict(t=40, b=40, l=40, r=40),
        shapes=[dict(type="rect", x0=0, x1=1, y0=0, y1=1, line=dict(color="white", width=2))]
    )
    return fig


def grafica_barras_precio(df):
    fig = px.histogram(df, x="Precio", nbins=20,
                       title="Distribución de Precios de Libros",
                       labels={"Precio": "Precio de Libro"},
                       color_discrete_sequence=["#6A0DAD"])
    fig.update_layout(
        xaxis_title="Precio",
        yaxis_title="Número de Libros",
        template="plotly_dark",
        font=dict(color="white"),
        bargap=0.2,
        title_font=dict(size=24, family="Arial, sans-serif", color="white", weight="bold"),
        margin=dict(t=40, b=40, l=40, r=40),
        plot_bgcolor="black",
        paper_bgcolor="black",
        shapes=[dict(type="rect", x0=0, x1=1, y0=0, y1=1, line=dict(color="white", width=2))]
    )
    return fig


def grafica_precio_formato_editorial(df):
    fig = px.bar(df, x="Editorial", y="Precio", color="Formato",
                 title="Distribución de Precios por Formato y Editorial",
                 labels={"Precio": "Precio", "Editorial": "Editorial", "Formato": "Formato"},
                 template="plotly_dark", barmode="group",
                 color_discrete_map={
                     "Tapa dura": "#4B0082",  # Morado oscuro
                     "Multiformato": "#6A0DAD",  # Morado más oscuro
                     "Tapa blanda": "#800080",  # Morado más intenso
                     "Digital": "#9932CC"
                 })
    fig.update_layout(
        title_font=dict(size=24, family="Arial, sans-serif", color="white", weight="bold"),
        margin=dict(t=40, b=40, l=40, r=40),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        shapes=[dict(type="rect", x0=0, x1=1, y0=0, y1=1, line=dict(color="white", width=2))],
        xaxis=dict(tickangle=45),
        yaxis=dict(tickprefix="$")
    )
    return fig


def tarjeta_filtro():
    control = dbc.Card(
        [
            html.Div([
                dbc.Label("Selecciona Formato para las Gráficas", style={"color": "#9b4dca", "font-weight": "bold"}),
                dcc.Dropdown(
                    options=[{"label": formato, "value": formato} for formato in libros_df["Formato"].unique()],
                    value=libros_df["Formato"].unique()[0],
                    id="formato-dropdown",
                    style={
                        "width": "100%",
                        "background-color": "#9b4dca",
                        "color": "black",
                        "border-radius": "15px",
                        "border": "1px solid #888",
                        "box-shadow": "0 4px 10px rgba(0,0,0,0.2)",
                        "font-family": "Arial, sans-serif",
                        "font-size": "16px",
                        "padding": "12px",
                        "font-weight": "bold"
                    }
                )
            ]),

            html.Div([
                dbc.Label("Filtrar Gráfica de Distribución por Formato",
                          style={"color": "#9b4dca", "font-weight": "bold"}),
                dcc.Dropdown(
                    options=[{"label": formato, "value": formato} for formato in libros_df["Formato"].unique()],
                    value="Tapa dura",
                    id="formato-dropdown-2",
                    style={
                        "width": "100%",
                        "background-color": "#af69cd",
                        "color": "black",
                        "border-radius": "15px",
                        "border": "1px solid #888",
                        "box-shadow": "0 4px 10px rgba(0,0,0,0.2)",
                        "font-family": "Arial, sans-serif",
                        "font-size": "16px",
                        "padding": "12px",
                        "font-weight": "bold"
                    }
                )
            ])
        ],
        style={
            "background-color": "#f1e0ff",
            "padding": "20px",
            "border-radius": "15px",
            "box-shadow": "0 4px 15px rgba(0,0,0,0.15)",
            "margin-bottom": "30px"
        }
    )
    return control


def dashboard():
    fig_editoriales = grafica_barras_precio(libros_df)
    fig_autores = grafica_pastel_formato(libros_df)
    fig_precio_editorial = grafica_precio_formato_editorial(libros_df)

    body = dbc.Container([

        dbc.Row([
            dbc.Col(html.H1("Análisis de Precios y Formato de Libros", className="text-center"),
                    style={"background-color": "#9b4dca", "padding": "20px", "border-radius": "15px",
                           "color": "white", "box-shadow": "0 4px 10px rgba(0,0,0,0.2)", "font-weight": "bold"},
                    width=12)
        ], style={"margin-bottom": "30px"}),

        dbc.Row([
            dbc.Col(html.Div([tarjeta_filtro()]), width=4),
            dbc.Col(
                html.Div([
                    dbc.Row(dcc.Graph(figure=fig_editoriales, id="figLine")),
                    dbc.Row(dcc.Graph(figure=fig_precio_editorial, id="figBox"))
                ]), width=8
            ),
        ], style={"margin-bottom": "30px"}),

        dbc.Row([
            dbc.Col(dcc.Graph(id="grafica-pastel-formato", figure=fig_autores), width=12),
        ])

    ])

    return body


def callbacks_d1(app):
    @app.callback(
        Output("figLine", "figure"),
        Output("figBox", "figure"),
        Output("grafica-pastel-formato", "figure"),
        Input("formato-dropdown", "value"),
        Input("formato-dropdown-2", "value")
    )
    def update_grafica(formato_seleccionado, formato_seleccionado_2):
        df_filtrado_1 = libros_df[libros_df["Formato"] == formato_seleccionado]
        df_filtrado_2 = libros_df[libros_df["Formato"] == formato_seleccionado_2]

        df_filtrado_final = pd.concat([df_filtrado_1, df_filtrado_2]).drop_duplicates()

        fig_editoriales = grafica_barras_precio(df_filtrado_final)
        fig_autores = grafica_pastel_formato(df_filtrado_final)
        fig_precio_editorial = grafica_precio_formato_editorial(df_filtrado_final)

        return fig_editoriales, fig_precio_editorial, fig_autores

    return app


app.layout = dashboard()
app = callbacks_d1(app)

if __name__ == "__main__":
    app.run_server(debug=True)