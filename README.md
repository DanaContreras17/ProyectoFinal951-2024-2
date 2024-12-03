# **Análisis de Libros: ETL y Dashboards Interactivos**

## **Descripción del Proyecto**

Este proyecto aborda los desafíos que enfrentan las editoriales, librerías y autores para estructurar, analizar y visualizar datos clave sobre libros. Mediante un proceso ETL (Extracción, Transformación y Carga), se procesan datos obtenidos de la página web de Gandhi para crear dashboards interactivos que facilitan la toma de decisiones basadas en datos.

### **Problemas que resuelve**
- **Desorganización de la información:** Los datos sobre libros suelen estar dispersos y sin estructura.
- **Dificultad para identificar patrones:** Falta de herramientas que permitan visualizar tendencias y relaciones en los datos.
- **Carencia de análisis basado en datos:** Decisiones comerciales se toman basándose en intuiciones en lugar de datos estructurados.

### **Características principales**
- Extracción de datos mediante web scraping.
- Limpieza y transformación de datos en un formato relacional para almacenarlos en MySQL.
- Creación de dashboards interactivos para:
  - Analizar precios y formatos de libros.
  - Examinar publicaciones de editoriales y autores.
  - Identificar tendencias en formatos y publicaciones.

### **Propósito general**
Proveer una herramienta integral para el sector editorial que facilite el análisis de datos sobre libros, optimizando estrategias de precios, distribución y promoción. Esto permite una mejor comprensión del mercado y fomenta decisiones estratégicas basadas en datos.

---


### **Requisitos previos**
- Python 3.8 o superior.
- MySQL.
- Librerías de Python.
  
## **Instalación**

- Clonar el repositorio.
- Instalar las librerías en caso de ser necesario.
- Descargar la base de datos que se encuentra en la carpeta “BaseDeDatos”, el archivo se encuentra como “libros_db.sql”.

## **Uso del proyecto**
Para correr el proyecto se debe de usar el archivo “main.py”. En este se encuentra el menú de todo el proyecto, teniendo de opciones: 

1. Web Scraping.
2. Data Cleaning.
3. Inserción a la Base de Datos.
4. Visualización de dashboards.
5. Salir.

Al correr el archivo hay que ingresar una de las opciones para ver cada proceso. La recomendación sería hacerlo todo por orden del 1-4. 

## **Estructura del proyecto**
ProyectoFinal951-2024-2

- BaseDeDatos.
- Datasets.
  - Libros_limpios.csv (archivo predeterminado).
- Conexion_mysql.py (archivo de base).
- importacion_csv.py (archivo para pruebas).
- insercion_db.py (codigo para la insercion a la BD).
- libros_db.sql (BD).
- Pruebas_db.sql (pruebas en mysql).

Dashboards

- assets.
  - css.
    - Custom.css (archivo con los estilos personalizados para los dashboards).
  - Imagenes (directorio en donde se encuentran las imagenes que usamos para el Dash.
- Datasets.
  - libros_limpios.csv (archivo predeterminado).
- dash1_sql.py
- dash2_sql.py
- dash3.py
- menu_libros.py (codigo principal para correr el dash y visualizar los dashboards).
- welcome_libros.py (codigo para el inicio o bienvenida del dash).
 
DataCleaning

- Datasets.
  - libros.csv (archivo predeterminado).
- DataCleaning.py (codigo para la limpieza de datos).

DataFrames

- libros.csv (archivo predeterminado).
- libros_limpios.csv (archivo predeterminado).

WebScraping

- Datasets.
  - libros.csv (archivo predeterminado)
- libros.py (codigo para realizar el web scraping)
- main.py (archivo principal que conecta todos los módulos y permite interactuar con el proyecto a través de un menú.)
- README.md (archivo de documentacion).

## **Problemas conocidos y recomendaciones**

1. Problemas con web scraping: Puede que al correr el web scraping, este extraiga solo 12 datos o datos menores a la cantidad que se tiene como parámetro que es 400.
Solución: Ajustar los valores de time.sleep() en el código según la velocidad de la conexión y/o tener la base de datos corrida en MySQL y con los datos ya insertados (esto se puede hacer gracias a los archivos.csv cargados predeterminadamente en el proyecto).

2. Conexión a la base de datos: Primero tienes que asegurarte que los datos de conexión a la base de datos en el archivo insercion_db.py sean correctos. Esto garantizará que el proyecto pueda interactuar con la base de datos MySQL de manera adecuada.

3. Inserción a la base de datos: Antes de ejecutar la inserción, primero se tiene que descargar la base de datos y haber configurado la conexión correctamente.











