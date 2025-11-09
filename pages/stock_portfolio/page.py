from dash import register_page
import pages.stock_portfolio.page_components.titles as stock_portfolio_titles
import pages.stock_portfolio.page_components.warnings as stock_portfolio_warnings
import pages.stock_portfolio.page_components.selectors as stock_portfolio_selectors
import pages.stock_portfolio.page_components.body as stock_portfolio_body
import pages.stock_portfolio.data as stock_portfolio_data
import utils.data_utils as data_utils
import dash_bootstrap_components as dbc


# Page name and route
register_page(__name__, name="Cartera", path="/portfolio")

# Variables
## Fijo el numero de columnas que quiero en cada fila (lo que definira el numero de filas)
page_grid_columns = 1  # Esto lo pongo a mano
page_title = "Cartera de acciones"

# get the data
stock_portfolio_df = stock_portfolio_data.get_page_data()  # get the data to play with in the page
purchases_and_sales_log_df = data_utils.get_purchases_and_sales_log()

# create the elements
page_title_row = stock_portfolio_titles.get_page_title_row(page_title)
warning_row = stock_portfolio_warnings.get_page_empty_warning_row()
selector_row = stock_portfolio_selectors.get_page_general_selector_row(purchases_and_sales_log_df)
body_row = stock_portfolio_body.get_body_row(stock_portfolio_df, page_grid_columns)

# assign the elements to display
layout = dbc.Row(dbc.Col([page_title_row, warning_row, selector_row, body_row]))