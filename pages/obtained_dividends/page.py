from dash import register_page
import pages.obtained_dividends.page_components.titles as obtained_dividends_titles
# import pages.obtained_dividends.page_components.warnings as obtained_dividends_warnings
import pages.obtained_dividends.page_components.selectors as obtained_dividends_selectors
import pages.obtained_dividends.page_components.body as obtained_dividends_body
import pages.obtained_dividends.data as obtained_dividends_data
import dash_bootstrap_components as dbc
import utils.data_utils as data_utils


# Set the basic parameters
register_page(__name__, name="Dividendos Cobrados", path="/dividends")
## Fijo el numero de columnas que quiero en cada fila (lo que definira el numero de filas)
page_grid_columns = 1  # Esto lo pongo a mano
page_title = "Dividendos Cobrados"

# Get the data
obtained_dividends_df = data_utils.get_obtained_dividends()
purchases_and_sales_enriched_df = data_utils.get_purchases_and_sales_enriched()

# Get Page components
page_title_row = obtained_dividends_titles.get_page_title_row(page_title)
# warning_row = obtained_dividends_warnings.get_page_empty_warning_row()
selector_row = obtained_dividends_selectors.get_page_general_selector_row(obtained_dividends_df)
body_row = obtained_dividends_body.get_body_row(obtained_dividends_df, purchases_and_sales_enriched_df, page_grid_columns)

# Set the page layout with the components
layout = dbc.Row(dbc.Col([
    page_title_row,
    # warning_row,
    selector_row,
    body_row
]))

