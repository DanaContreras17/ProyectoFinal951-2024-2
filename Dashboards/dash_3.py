import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output
import pandas as pd
import plotly.express as px
from mysql.connector import connect, Error


def obtener_datos_mysql():
    try:
        conexion = connect(host="localhost", port="3306", user="root",
                           password="12345678", database="libros_db")

        cursor = conexion.cursor()

        sql = """
        SELECT libros.titulo, autores.nombre AS autor, editoriales.nombre_editorial AS editorial,
               libros.formato, libros.precio
        FROM libros
        JOIN autores ON libros.id_autor = autores.id_autor
        JOIN editoriales ON libros.id_editorial = editoriales.id_editorial;
        """

        cursor.execute(sql)

        filas = cursor.fetchall()
        columnas = ["Nombre_libro", "Nombre_autor", "Editorial", "Formato", "Precio"]
        libros_df = pd.DataFrame(filas, columns=columnas)

        cursor.close()
        conexion.close()

        return libros_df

    except Error as e:
        print(f"Error: {e}")
        return None


libros_df = obtener_datos_mysql()

if libros_df is None:
    raise Exception("No se pudo obtener los datos desde la base de datos")

conteo_autores = libros_df["Nombre_autor"].value_counts().reset_index()
conteo_autores.columns = ["Nombre_autor", "Cantidad_libros"]


def grafico_formatos(df):
    conteo_formatos = df["Formato"].value_counts().reset_index()
    conteo_formatos.columns = ["Formato", "Cantidad_libros"]

    fig = px.pie(conteo_formatos, names="Formato", values="Cantidad_libros",
                 title="Distribución de Formatos de Libros",
                 template="plotly_dark",
                 color="Formato",
                 color_discrete_map={"Físico": "#9b59b6", "Ebook": "#8e44ad",
                                     "Audiobook": "#6c3483"})  # Colores morados
    return fig


def grafico_autores(conteo_autores):
    fig = px.bar(conteo_autores, x="Cantidad_libros", y="Nombre_autor",
                 title="Cantidad de Libros por Autor", orientation="h",
                 template="plotly_dark",
                 color="Cantidad_libros",
                 color_continuous_scale="Purples")
    fig.update_layout(yaxis={"categoryorder": "total ascending"},
                      xaxis_title="Cantidad de Libros",
                      yaxis_title="Autor",
                      showlegend=False)
    return fig


def grafico_precio_vs_libros(df):
    fig = px.scatter(df, x="Precio", y="Nombre_autor", color="Formato",
                     title="Precio vs. Autor por Formato",
                     template="plotly_dark")
    fig.update_layout(xaxis_title="Precio", yaxis_title="Autor")
    return fig


def filtros(df):
    opciones_formato = [{"label": formato, "value": formato} for formato in df["Formato"].unique()]
    opciones_autor = [{"label": autor, "value": autor} for autor in df["Nombre_autor"].unique()]

    dropdown_formato = dbc.Col([
        html.Label("Selecciona un formato", style={"color": "white"}),
        dcc.Dropdown(
            id="formato-dropdown",
            options=opciones_formato,
            value=[],  # Iniciar vacío
            multi=True,
            placeholder="Selecciona un formato"
        ),
    ], width=4)

    dropdown_autor = dbc.Col([
        html.Label("Selecciona un autor", style={"color": "white"}),
        dcc.Dropdown(
            id="autor-dropdown",
            options=opciones_autor,
            value=[],  # Iniciar vacío
            multi=True,
            placeholder="Selecciona un autor"
        ),
    ], width=4)

    return dropdown_formato, dropdown_autor
