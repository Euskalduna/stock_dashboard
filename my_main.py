from app import app
from utils.general_utils import *
from dash import page_container, callback, Input, Output, State, html

# --------------------------------------------------------------------------------------------------------------
# IMPORTANTE: Aunque parece que no hace nada es necesario para que funcionen los callbacks !!!!!
import pages.risk_diversification.callbacks as risk_diversification_callbacks
import pages.stock_portfolio.callbacks as stock_portfolio_callbacks
# --------------------------------------------------------------------------------------------------------------


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
