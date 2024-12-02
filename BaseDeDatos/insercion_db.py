

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


            sql1 = "INSERT INTO autores (nombre) VALUES (%s)"
            autores = (autor,)
            cursor.execute(sql1, autores)
            autor_id = cursor.lastrowid


            sql2 = "INSERT INTO editoriales (nombre_editorial) VALUES (%s)"
            editoriales = (editorial,)
            cursor.execute(sql2, editoriales)
            editorial_id = cursor.lastrowid


            sql3 = "INSERT INTO libros (titulo, id_autor, id_editorial, formato, precio) VALUES (%s, %s, %s, %s, %s)"
            libros = (titulo, autor_id, editorial_id, formato, precio)
            cursor.execute(sql3, libros)

            conexion.commit()


        cursor.close()
        conexion.close()
        print("Insercion completada en MySQL")




    except Error as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    archivo_csv = "../DataFrames/libros_limpios.csv"
    insertar_db(archivo_csv)