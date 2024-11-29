

import pandas as pd
from mysql.connector import connect, Error

def insertar_db(archivo_csv):
    try:
        archivo = pd.read_csv(archivo_csv)

        conexion = connect(host="localhost", port="3306", user="root",
                           password="12345678", database="libros_db")
        cursor = conexion.cursor()

        #Para ir recorriendo las filas del archivo csv
        for index, fila in archivo.iterrows():
            titulo = fila["Nombre_libro"]
            autor = fila["Nombre_autor"]
            editorial = fila["Editorial"]
            formato = fila["Formato"]
            precio = fila["Precio"]



    except Error as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    insertar_db("datasets/libros_limpios.csv")