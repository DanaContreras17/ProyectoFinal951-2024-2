


from dash import html


# dcc --- Dash Core Components
# html --- Dash HTML Components
def welcome():
    #cuerpo de la pagina web
    body = html.Div(
        [
            html.H3("Programacion para la extraccion de datos"), # titulos
            html.Img(src="assets/imagenes/gandhi.png",
                     width=400, height=300, title="Python"),
            html.P("Los siguientes dashboards presentan un analisis acerca de una recopilacion de libros extraidos de la libreria Gandhi.", className="custom_p"), # parrafos
            html.Hr(), # linea horizontal que funciona como un separador
            html.H4("Integrantes del equipo:"),
            html.Ul(
                [
                    html.Li("Contreras Vazquez Dana Lizbeth"),
                    html.Li("Medrano Gonzalez Aaron Daniel"),
                    html.Li("Meza Gomez Jaqueline"),
                    html.Li("Saucedo Beltran Leonardo"),
                    html.Li("Verdugo Garcia Blanca Yuliana")
                ]
            ),
            html.Img(src="assets/imagenes/dana.png",
                     width=100, height=100, title="Python"),
            html.Img(src="assets/imagenes/jaqui.png",
                     width=100, height=100, title="Python"),
            html.Img(src="assets/imagenes/yuls.png",
                     width=100, height=100, title="Python"),
            html.Img(src="assets/imagenes/leo.png",
                     width=100, height=100, title="Python"),
            html.Img(src="assets/imagenes/medrano.png",
                     width=100, height=100, title="Python"),
        ],
        className="inicio-section"
    )
    return body


