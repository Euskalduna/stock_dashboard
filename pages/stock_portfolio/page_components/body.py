import dash_bootstrap_components as dbc
from pages.stock_portfolio.page_components.panels.stock_portfolio import get_portfolio_table
import utils.general_utils as general_utils


def get_body_row(stock_portfolio_df, page_grid_columns):
    panel_type_id = "stock-portfolio-data-panel"
    panel_list = get_panels(stock_portfolio_df)

    # distribute panels in rows
    data_row_list = general_utils.get_panel_rows(panel_list, page_grid_columns, panel_type_id)
    body_row = dbc.Row(dbc.Col(data_row_list))
    return body_row


def get_panels(stock_portfolio_df):
    panel_list = []

    # Panel de la cartera
    panel_children = get_portfolio_table(stock_portfolio_df)

    panel_list.append({"panel_id": "portfolio", "panel": panel_children})

    return panel_list





