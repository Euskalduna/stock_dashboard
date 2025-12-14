import dash_bootstrap_components as dbc
from pages.obtained_dividends.page_components.panels.dividends_kpis import get_dividends_kpis_panel
from pages.obtained_dividends.page_components.panels.dividends_by_company import get_dividends_by_company_panel
from pages.obtained_dividends.page_components.panels.dividend_evolution import get_dividend_evolution_panel
from pages.obtained_dividends.page_components.panels.dividends_pivot_table import get_dividend_pivot_table
import utils.general_utils as general_utils


def get_body_row(obtained_dividends_df, purchases_and_sales_enriched_df, page_grid_columns):
    panel_type_id = "obtained-dividends-data-panel"
    panel_list = get_panels(obtained_dividends_df, purchases_and_sales_enriched_df) #---> #TODO: Tengo que crear N paneles. como lo hago para que sea dinamico????
                                                        #TODO: primero voy a crearlos a manija, si veo patrón común y ya lo generalizo
    # distribute panels in rows
    data_row_list = general_utils.get_panel_rows(panel_list, page_grid_columns, panel_type_id)
    body_row = dbc.Row(dbc.Col(data_row_list))
    return body_row


def get_panels(obtained_dividends_df, purchases_and_sales_enriched_df):
    panel_list = []

    # KPIs
    dividends_kpi_panel_children = get_dividends_kpis_panel(
        obtained_dividends_df,
        purchases_and_sales_enriched_df
    )

    # Panel del PIE CHART
    weight_criteria_column = "gross_obtained_money_in_euros"
    dividends_by_company_panel_children = get_dividends_by_company_panel(obtained_dividends_df, weight_criteria_column)

    # Panel del BAR CHART
    data_column = "gross_obtained_money_in_euros"
    first_group_by_colum = "payment_year"
    second_group_by_column = None
    # data_column = "Dinero BRUTO Cobrado"
    # second_group_by_column = "Moneda de lo cobrado"
    dividend_evolution_panel_children = get_dividend_evolution_panel(
        obtained_dividends_df,
        data_column,
        first_group_by_colum,
        second_group_by_column
    )

    # Panel de la TABLA
    # WIP

    # Panel de la TABLA PIVOTE
    dividend_pivot_table_panel_children = get_dividend_pivot_table(obtained_dividends_df)

    panel_list.append({"panel_id": "dividends_kpi_panel", "panel": dividends_kpi_panel_children})
    panel_list.append({"panel_id": "dividend_weight_by_company_panel", "panel": dividends_by_company_panel_children})
    panel_list.append({"panel_id": "dividend_evolution_panel", "panel": dividend_evolution_panel_children})
    panel_list.append({"panel_id": "dividend_pivot_table_panel", "panel": dividend_pivot_table_panel_children})

    return panel_list
