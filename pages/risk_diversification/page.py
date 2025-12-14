from dash import register_page
from utils.global_variables import context
import pages.risk_diversification.page_components.titles as risk_diversification_titles
import pages.risk_diversification.page_components.warnings as risk_diversification_warnings
import pages.risk_diversification.page_components.selectors as risk_diversification_selectors
import pages.risk_diversification.page_components.body as risk_diversification_body
import pages.risk_diversification.data as risk_diversification_data
import dash_bootstrap_components as dbc
import utils.data_utils as data_utils

# Set the basic parameters
register_page(__name__, name="Diversificación del Riesgo", path="/")
# Fijo el numero de columnas que quiero en cada fila (lo que definira el numero de filas)
page_grid_columns = 1  # Esto lo pongo a mano
default_weight_criteria_column = 'payed_money_in_euros'
risk_diversification_criteria_dict_list = context['risk_diversification_criteria_dict_list'].copy()
page_title = "Diversifiación de Riesgos"

# Get the data
purchases_and_sales_enriched_df = data_utils.get_purchases_and_sales_enriched()

# Get Page components
page_title_row = risk_diversification_titles.get_page_title_row(page_title)
warning_row = risk_diversification_warnings.get_page_warning_row()
selector_row = risk_diversification_selectors.get_page_general_selector_row(purchases_and_sales_enriched_df, default_weight_criteria_column)
body_row = risk_diversification_body.get_body_row(purchases_and_sales_enriched_df, risk_diversification_criteria_dict_list, default_weight_criteria_column, page_grid_columns)

# Set the page layout with the components
layout = dbc.Row(dbc.Col([
    page_title_row,
    warning_row,
    selector_row,
    body_row
]))


