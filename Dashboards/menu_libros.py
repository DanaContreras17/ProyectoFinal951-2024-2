
from welcome_libros import welcome
#from dashboard_uno import dashboard
#from dashboard_2 import dashboard as d2
#from dashboard_3 import dashboard as d3
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, Dash, callback


@callback(Output("page-content", "children"), #lo va a agregar como un hijo "children"
          [Input("url", "pathname")])

def render_page_content(pathname):
    if pathname == "/":
        #en vez de esto, mandariamos a llmar las funciones de todas las graficas y eso
        return welcome()
    elif pathname == "/dash-1":
        #return dashboard()
        print("dashboard1")
    elif pathname == "/dash-2":
        # return d2()
        print("dashboard2")
    elif pathname == "/dash-3":
        # return d3()
        return html.P("Oh cool, this is page 3!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


def menu_dashboard():
    # the style arguments for the sidebar. We use position:fixed and a fixed width


    sidebar = html.Div(
        [
            html.H2("Dashboard", className="display-6 custom-h2"), #className tipo de letra
            html.Hr(),
            html.P(
                "Visualizacion de datos clave sobre libros, autores y editoriales.", className="lead"
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Inicio", href="/", active="exact"), #opciones del menu
                    dbc.NavLink("Dashboard 1", href="/dash-1", active="exact"), #href cambios de pagina
                    dbc.NavLink("Dashboard 2", href="/dash-2", active="exact"), #active color del bloquecito
                    dbc.NavLink("Dashboard 3", href="/dash-3", active="exact"),
                    dbc.NavLink("Github", href="https://www.github.com",
                                active="exact", target="_blank"), #target para abrir en otra pestana
                ],
                vertical=True,
                pills=True,
            ),
        ],
        className="SIDEBAR_STYLE",
    )

    content = html.Div(id="page-content", className="CONTENT_STYLE")

    return html.Div([dcc.Location(id="url"), sidebar, content])


if __name__ == "__main__":
    # TEMAS
    app = Dash(external_stylesheets=[dbc.themes.LUX],
               suppress_callback_exceptions=True)
    app.layout = menu_dashboard()
    app.run(debug=True)