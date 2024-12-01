import mysql.connector
from mysql.connector import Error

def conectar_a_base_de_datos():
    try:

        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MezaG2004",
            database="Libros"
        )

        if conexion.is_connected():
            print("Se logro conectar")
            info_servidor = conexion.get_server_info()
            print("Versión del servidor MySQL:", info_servidor)

        return conexion

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return None

    finally:
        if conexion.is_connected():
            conexion.close()
            print("Conexión cerrada.")


conectar_a_base_de_datos()