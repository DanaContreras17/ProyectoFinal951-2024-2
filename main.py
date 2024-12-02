
import threading
import WebScraping.libros as ws
import DataCleaning.DataCleaning as dc
import BaseDeDatos.insercion_db as ib
import time
from mysql.connector import connect, Error


def comprobar_si_hay_datos():
    try:
        conexion = connect(host="localhost", port="3306", user="root",
                           password="12345678", database="libros_db")
        cursor = conexion.cursor()
        sql = "SELECT COUNT(*) FROM libros"
        cursor.execute(sql)
        resultado = cursor.fetchone()
        conexion.close()
        return resultado[0] > 0

    except Error as e:
        print(e)
        return False


def ejecutar_dash():
    import Dashboards.menu_libros as da
    da.app.run(debug=True, use_reloader=False)


def menu():
    while True:
        op = int(input("\nMenu de procesos del proyecto\n"
                                     "\n1)Web Scraping\n2)Data Cleaning\n3)Insercion a la Base de Datos"
                                     "\n4)Visualizacion de dashboards\n5)Salir\nIngresa:"))
        if op == 1:
            busqueda = "libros"
            max_results = 400
            ws.scraping(busqueda, max_results)
        elif op == 2:
            archivo_csv = "DataFrames/libros.csv"
            ruta_salida = "DataFrames/libros_limpios.csv"
            dc.limpiar_datos(archivo_csv, ruta_salida)
        elif op == 3:
            archivo_csv = "DataFrames/libros_limpios.csv"
            ib.insertar_db(archivo_csv)
        elif op == 4:
            if comprobar_si_hay_datos():
                print("Cargando dashboards")
                hilo_dash = threading.Thread(target=ejecutar_dash)
                hilo_dash.daemon = True
                hilo_dash.start()
                time.sleep(5)
            else:
                print("\nPrimero debes insertar los datos en la base de datos para poder ver los dashboards."
                      "\nLa base de datos esta en la carpeta 'BaseDeDatos' con el nombre de 'libros_db.sql' para descargarla.")
        elif op == 5:
            print("\nHasta luego y lindo dia:)")
            break
        else:
            print("\nNo se encontro ninguna de las opciones")



if __name__ == "__main__":
    menu()