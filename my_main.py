from utils.general_utils import *
from dash import Dash
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
from dash import Dash, page_container, callback, Input, Output, State, html
# import pages.risk_diversification.risk_diversification_page as risk_diversification_page
# import pages.stock_portfolio.stock_portfolio_page as stock_portfolio_page

# Inicio de la aplicacion
#app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Pagina para explorar temas de CSS de Dash: https://hellodash.pythonanywhere.com/adding-themes/dcc-components
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
vizro_bootstrap = "https://cdn.jsdelivr.net/gh/mckinsey/vizro@main/vizro-core/src/vizro/static/css/vizro-bootstrap.min.css?v=2"
# app = Dash(__name__, external_stylesheets=[vizro_bootstrap, dbc.icons.FONT_AWESOME, dbc_css], use_pages=True)
#app = Dash(__name__, use_pages=True)
# app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, dbc.icons.FONT_AWESOME, dbc_css])
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
# load_figure_template(["vizro", "vizro_dark"])



#
# color_mode_switch =  html.Span(
#     [
#         dbc.Label(className="fa fa-moon", html_for="switch"),
#         dbc.Switch( id="switch", value=True, className="d-inline-block ms-1", persistence=True),
#         dbc.Label(className="fa fa-sun", html_for="switch"),
#     ]
# )
#
#
# # The ThemeChangerAIO loads all 52  Bootstrap themed figure templates to plotly.io
# theme_controls = html.Div(
#     [ThemeChangerAIO(aio_id="theme", custom_themes={'vizro': vizro_bootstrap}), color_mode_switch],
#     className="hstack gap-3 mt-2"
# )
#






# Other themes https://www.bootstrapcdn.com/bootswatch/
# Cheatsheet https://hackerthemes.com/bootstrap-cheatsheet/


# Genera el menú lateral
sidebar_menu_div = get_sidebar_menu()

# Uno los 2 elementos (side menu y la pagina base)
container_row = dbc.Row([
    dcc.Store(id="sidebar-state", data=True),
    dbc.Col([sidebar_menu_div], id="sidebar-column", width=2, className="bg-white"),
    dbc.Col(
        [
            dbc.Button(html.I(className="bi bi-list"), id="sidebar-toggle", n_clicks=0, className="mb-3 bg-black"),
            page_container
        ],
        id="page-content-column",
        width=10,
        className="p-4"
    ),
], className="",)
# ], className="g-0",)
# Añado los elementos en la página
app.layout = dbc.Container(children=[container_row], className="dbc page-base-div", fluid=True)


@callback(
    [
        Output("sidebar-column", "style"),
        Output("page-content-column", "width"),
        Output("sidebar-state", "data"),
    ],
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar-state", "data")],
    prevent_initial_call=True
)
def toggle_sidebar(n_clicks, is_open):
    if is_open:
        # If sidebar is open, close it
        sidebar_style = {'display': 'none'}  # Hide the column
        content_width = 12  # Content takes full width
        new_state = False
    else:
        # If sidebar is closed, open it
        sidebar_style = {}  # Revert to default style (visible)
        content_width = 10  # Content is back to 10 columns
        new_state = True

    return sidebar_style, content_width, new_state



if __name__ == '__main__':
    print("antes")
    app.run(debug=True, port=8060)
    print("Despues")
