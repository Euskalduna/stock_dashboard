from dash import html
import dash_bootstrap_components as dbc


def get_page_title_row(title):
    title_row = dbc.Row(dbc.Col(html.H1(title)))
    return title_row


def get_page_common_panel_title_row(title):
    title_row = dbc.Row([dbc.Col([html.H2(title)])])
    return title_row