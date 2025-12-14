from dash import html
import dash_bootstrap_components as dbc


def get_page_warning_row(children=()):
    empty_warning_row = dbc.Row(id="page_warning_row", children=children)
    return empty_warning_row


def get_empty_warning_col():
    warning_col = dbc.Col()
    return warning_col


def get_warning_col(text):
    warning_col = dbc.Col(html.H3(text, className="mild-warning-div"))
    return warning_col
