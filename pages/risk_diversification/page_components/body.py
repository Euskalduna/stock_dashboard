import dash_bootstrap_components as dbc
from pages.risk_diversification.page_components.panels.risk_diversification import get_risk_diversification
from pages.risk_diversification.page_components.panels.risk_diversification_kpis import get_risk_diversification_kpis_panel
import utils.general_utils as general_utils


def get_body_row(purchases_and_sales_enriched_df, risk_diversification_criteria_dict_list, weight_criteria_column, page_grid_columns):
    panel_type_id = "risk-diversification-data-panel"
    # get body_panel
    panel_list = get_panels(purchases_and_sales_enriched_df, risk_diversification_criteria_dict_list, weight_criteria_column)
    # get_body_rows
    data_row_list = general_utils.get_panel_rows(panel_list, page_grid_columns, panel_type_id)
    body_row = dbc.Row(dbc.Col(data_row_list))
    return body_row


def get_panels(purchases_and_sales_enriched_df, risk_diversification_criteria_dict_list, weight_criteria_column):
    def get_risk_criteria_dict(risk_type, risk_diversification_criteria_dict_list):
        try:
            risk_criteria_dict = next(risk_criteria_dict for risk_criteria_dict in risk_diversification_criteria_dict_list if risk_criteria_dict.get("criteria_name") == risk_type)

        except StopIteration:
            print(f"RISK {risk_type} NOT FOUND !!!")
            raise Exception

        return risk_criteria_dict

    panel_list = []

    # KPIs
    risk_diversification_kpis_panel_children = get_risk_diversification_kpis_panel(purchases_and_sales_enriched_df)

    # Risk by Company
    risk_type = "company"
    risk_criteria_dict = get_risk_criteria_dict(risk_type, risk_diversification_criteria_dict_list)

    risk_by_company_panel_children = get_risk_diversification(
        purchases_and_sales_enriched_df,
        risk_criteria_dict,
        weight_criteria_column
    )

    # Risk by Sector
    risk_type = "sector"
    risk_criteria_dict = get_risk_criteria_dict(risk_type, risk_diversification_criteria_dict_list)
    risk_by_sector_panel_children = get_risk_diversification(
        purchases_and_sales_enriched_df,
        risk_criteria_dict,
        weight_criteria_column
    )

    # Risk by Country
    risk_type = "country"
    risk_criteria_dict = get_risk_criteria_dict(risk_type, risk_diversification_criteria_dict_list)
    risk_by_country_panel_children = get_risk_diversification(
        purchases_and_sales_enriched_df,
        risk_criteria_dict,
        weight_criteria_column
    )

    # Risk by Currency
    risk_type = "currency"
    risk_criteria_dict = get_risk_criteria_dict(risk_type, risk_diversification_criteria_dict_list)
    risk_by_currency_panel_children = get_risk_diversification(
        purchases_and_sales_enriched_df,
        risk_criteria_dict,
        weight_criteria_column
    )

    panel_list.append({"panel_id": "risk_diversification_kpi", "panel": risk_diversification_kpis_panel_children})
    panel_list.append({"panel_id": "company", "panel": risk_by_company_panel_children})
    panel_list.append({"panel_id": "sector", "panel": risk_by_sector_panel_children})
    panel_list.append({"panel_id": "country", "panel": risk_by_country_panel_children})
    panel_list.append({"panel_id": "currency", "panel": risk_by_currency_panel_children})

    return panel_list
