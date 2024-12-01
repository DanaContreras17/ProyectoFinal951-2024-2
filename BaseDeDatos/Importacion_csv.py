import pandas as pd


def cargar_datos_csv():

        df = pd.read_csv("libros_limpios.csv")

        print("\nTipos de datos en el df")
        print(df.dtypes)

        if 'precio' in df.columns: #Verificar que las columnas con valores numericos tengan el tipo correcto y si no es asi, convertirlo.
            df['precio'] = pd.to_numeric(df['precio'], errors='coerce')

        print("\nValores nulos en el df") #Aun que los datos se supone que ya estan limpios verificar en caso de.
        print(df.isnull().sum())

        print(df.info()) #Estructura final de los datos
        return df


if __name__ == "__main__":
    df = cargar_datos_csv()
