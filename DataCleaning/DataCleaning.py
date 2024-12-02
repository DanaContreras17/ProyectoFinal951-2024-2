import pandas as pd


def limpiar_datos(archivo_csv, ruta_salida):
    df = pd.read_csv(archivo_csv)

    #VERIFICAR DATOS
    print(df.head())
    print("Nombres de las columnas:")
    print(df.columns)
    print("Valores faltantes por columna:")
    print(df.isnull().sum())

    #MODIFICAR O QUITAR DATOS

    #ELIMINAR
    df = df.dropna()
    #DUPLICADOS
    df = df.drop_duplicates()

    #CORREGIMOS LOS TIPOS DE DATOS, CONVERTIMOS LA COLUMNA "PRECIO" A VALORES NUMERICOS
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')

    #CON ESTA SE RELLENO LOS VALORES FALTANTES EN "PRECIO" (AUNQUE NO FUE NECESARIO)
    df['precio'] = df['precio'].fillna(df['precio'].mean())

    #SIRVE PARA FILTRAR DATOS DONDE EL PRECIO SEA MAYOR A 0
    df = df[df['precio'] > 0]

    # MODIFICAMOS EL NOMBRE DE LAS COLUMNAS PARA QUE SE ENTIENDARA MEJOR
    df = df.rename(columns={'titulo': 'Nombre_libro',
                            'autor': 'Nombre_autor',
                            'editorial': 'Editorial',
                            'formato': 'Formato',
                            "precio": "Precio" })

    #GUARDAR EL DATA FRAME ACTUALIZADO Y YA LIMPIESITO
    df.to_csv(ruta_salida, index=False)
    df.to_csv("DataCleaning/datasets/libros_limpios.csv", index=False)


    print("Limpiezitos y guardaditos 'datasets/libros_limpios.csv'")


if __name__ == "__main__":
    archivo_csv = "../DataFrames/libros.csv"
    ruta_salida = "../DataFrames/libros_limpios.csv"
    limpiar_datos(archivo_csv, ruta_salida)


# NOTAS MIAS PARA FUTURO
# (en caso de agregar más columnas para modificar):
# Convertir 'Fecha_Publicación' a tipo datetime, si existe
# df['Fecha_Publicación'] = pd.to_datetime(df['Fecha_Publicación'], errors='coerce')

# Corregir 'stock' a tipo numérico, si es necesario ajustar la columna 'stock'
# df['Stock'] = pd.to_numeric(df['Stock'], errors='coerce')