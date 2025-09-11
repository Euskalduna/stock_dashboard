from dash import register_page
import pages.stock_portfolio.stock_portfolio_titles as stock_portfolio_titles
import pages.stock_portfolio.stock_portfolio_warnings as stock_portfolio_warnings
import pages.stock_portfolio.stock_portfolio_selectors as stock_portfolio_selectors
import pages.stock_portfolio.stock_portfolio_body as stock_portfolio_body
import pages.stock_portfolio.stock_portfolio_data as stock_portfolio_data
import dash_bootstrap_components as dbc


register_page(__name__)

# Fijo el numero de columnas que quiero en cada fila (lo que definira el numero de filas)
page_grid_columns = 1  # Esto lo pongo a mano
page_title = "Cartera de acciones"
stock_portfolio_df = stock_portfolio_data.get_page_data()  # get the data to play with in the page

page_title_row = stock_portfolio_titles.get_page_title_row(page_title)
warning_row = stock_portfolio_warnings.get_page_empty_warning_row()
selector_row = stock_portfolio_selectors.get_page_general_selector_row()
body_row = stock_portfolio_body.get_body_row(stock_portfolio_df, page_grid_columns)

layout = dbc.Row(dbc.Col([page_title_row, warning_row, selector_row, body_row]))