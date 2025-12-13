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


def get_panel_rows(panel_list, page_grid_columns, panel_type_id):
    """
    It receives the list of panels and returns the list of rows with the columns inside
    Each panel is a dictionary with the following structure:
        {"panel_id": "company", "panel": risk_by_company_panel_children}

    The page_grid_columns indicates how many columns per row the page will have.
    The panel_type_id is used to set the id of each panel column to be able to call it in the callbacks.

    :param panel_list: list of dicts with the structure described above. Each dict represents a panel to be added to the body.
    :param page_grid_columns: is an integer that indicates how many columns per row the page will have.
    :param panel_type_id: is a string that indicates the type of the panel, used to set the id of each panel column.
    :return: a list of dbc.Row objects with the panels as columns.
    """

    data_row_list = []
    column_by_row_list = []

    for index, panel_dict in enumerate(panel_list):
        is_last_risk_criteria = ((index + 1) == len(panel_list))
        is_new_row_required = ((index + 1) % page_grid_columns == 0) or is_last_risk_criteria

        col_id = {"type": panel_type_id, "index": panel_dict["panel_id"]}
        column_by_row_list.append(dbc.Col(panel_dict["panel"], id=col_id, className="data-div"))

        if is_new_row_required:
            data_row_list.append(dbc.Row(column_by_row_list))
            column_by_row_list = []
    return data_row_list


def get_panel_row(row_element_dict_list, data_row_style=None, column_size_proportions=None):
    """
    It recieves a list of dicts with the following structure:
        {"id": html_element_id, "html_component": html_element_component}
    and creates a dbc.Row with the elements as columns, assigning the same width or the width
    passed by the user.

    This function is used mainly in the "panels" of the pages.

    :param row_element_dict_list: list of dicts with the said structure. Each dict represents an element to be added to the row.
    :param data_row_style: it sets the style of the row (optional). For example set the height (or min height) of the row.
    :param column_size_proportions: list of integers representing the size of each column (optional). If not provided, all columns will have the same size.
    :return: dbc.Row object with the elements as columns.
    """

    column_list = []
    max_columns_in_row = 12

    if column_size_proportions is None:
        column_size = int(max_columns_in_row / len(row_element_dict_list))
        column_size_proportions = [column_size] * len(row_element_dict_list)

    for index, row_element_dict in enumerate(row_element_dict_list):
        html_element_id = row_element_dict["id"]
        html_element_component = row_element_dict["html_component"]
        column_size = column_size_proportions[index]

        column_list.append(
            dbc.Col(
                [html_element_component],
                id=html_element_id,
                className=f"col-md-{column_size}",
            )
        )

    if data_row_style is None:
        data_row = dbc.Row(column_list)
    else:
        data_row = dbc.Row(column_list, style=data_row_style)

    return data_row
