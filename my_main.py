from utils.general_utils import *
import utils.data_utils as data_utils
import pages.risk_diversification.risk_diversification_page as risk_diversification_page
from dash import Dash, Output, Input, State, MATCH, callback_context
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

# Inicio de la aplicacion
#app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Pagina para explorar temas de CSS de Dash: https://hellodash.pythonanywhere.com/adding-themes/dcc-components
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
vizro_bootstrap = "https://cdn.jsdelivr.net/gh/mckinsey/vizro@main/vizro-core/src/vizro/static/css/vizro-bootstrap.min.css?v=2"
app = Dash(__name__, external_stylesheets=[vizro_bootstrap, dbc.icons.FONT_AWESOME, dbc_css])
# app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, dbc.icons.FONT_AWESOME, dbc_css])
load_figure_template(["vizro", "vizro_dark"])


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

# Genera la pagina base
page_title_row, selector_row, content_row = risk_diversification_page.get_risk_diversification_page_layout()
risk_diversification_page_children_list = [page_title_row, selector_row, content_row]
page_row = dbc.Row(dbc.Col(risk_diversification_page_children_list, className="page-base-div"))
# Traigo los callbacks de la pagina
risk_diversification_page.get_risk_diversification_page_callbacks(app)

# Genera el menú lateral
sidebar_menu_div = get_sidebar_menu()

# Uno los 2 elementos (side menu y la pagina base)
container_row = dbc.Row([
    dbc.Col([sidebar_menu_div], width=2),
    dbc.Col([page_row], width=10)
])
# Añado los elementos en la página
app.layout = dbc.Container(children=[container_row], className="dbc", fluid=True)


if __name__ == '__main__':
    print("antes")
    app.run_server(debug=True, port=8060)
    print("Despues")
