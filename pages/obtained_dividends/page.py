from dash import register_page
import pages.obtained_dividends.page_components.titles as obtained_dividends_titles
# import pages.obtained_dividends.page_components.warnings as obtained_dividends_warnings
import pages.obtained_dividends.page_components.selectors as obtained_dividends_selectors
import pages.obtained_dividends.page_components.body as obtained_dividends_body
import pages.obtained_dividends.data as obtained_dividends_data
import dash_bootstrap_components as dbc


register_page(__name__, name="Dividendos Cobrados", path="/dividends")

page_grid_columns = 1  # Esto lo pongo a mano
page_title = "Dividendos Cobrados"
obtained_dividends_df = obtained_dividends_data.get_page_data()

page_title_row = obtained_dividends_titles.get_page_title_row(page_title)
# warning_row = obtained_dividends_warnings.get_page_empty_warning_row()
selector_row = obtained_dividends_selectors.get_page_general_selector_row(obtained_dividends_df)
body_row = obtained_dividends_body.get_body_row(obtained_dividends_df, page_grid_columns)

layout = dbc.Row(dbc.Col([
    page_title_row,
    # warning_row,
    selector_row,
    body_row
]))

