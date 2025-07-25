import pandas as pd
from dash import Dash, html, dcc, dash_table, Output, Input, State, MATCH, ALL, callback_context, page_registry,page_container
import dash_bootstrap_components as dbc
import plotly.express as px
import math

"""
-----------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------
--------------------------------------------HTML COMPONENT UTILS-------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------
"""


def get_sidebar_menu():
    sidebar_menu_div = html.Div(
        [
            html.H1("Paginas"),
            dbc.Nav(
                [
                    dbc.NavLink(page["name"], href=page["relative_path"], active="exact") for page in page_registry.values()
                ],
                vertical=True,
                pills=True,
            )
        ],
        #className="p-4 bg-light",  # Add some padding and a light background
    )

    return sidebar_menu_div
