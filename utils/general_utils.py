import pandas as pd
from dash import Dash, html, dcc, dash_table, Output, Input, State, MATCH, ALL, callback_context
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
            dbc.Collapse(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2("Menu", className="display-4"),
                            html.Hr(),
                            html.P('This is a test'),
                            # dbc.Nav(
                            #     [
                            #         dbc.Navlink o link 1
                            #         dbc.Navlink o link 2
                            #         dbc.Navlink o link 3
                            #     ],
                            #     vertical=True,
                            #     pills=True
                            # )
                        ],
                        # className="h-100 "
                    ),
                    className="h-100"
                ),
                is_open=True,
                dimension="width",
                className="h-100 bg-primary"
            )
        ],
        className="h-100 bg-danger"
    )
    return sidebar_menu_div
