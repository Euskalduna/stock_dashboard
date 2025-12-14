from utils.global_variables import context
from dash import Output, Input, MATCH, callback_context
from app import app

import pages.risk_diversification.page_components.warnings as risk_diversification_warnings
import utils.data_utils as data_utils
from pages.risk_diversification.page_components.panels.risk_diversification import get_risk_diversification


#TODO: debo estandarizar la nomenclatura de los IDs

@app.callback(
    [Output({'type': 'risk-diversification-data-panel', 'index': MATCH}, 'children')],
    [Input("owner_dropdown_selector", "value"),
     Input("broker_dropdown_selector", "value"),
     Input("weight_dropdown_selector", "value")]
)
def update_page_data(selected_options_owner, selected_options_broker, selected_options_weight):
    """
    Borra y vuelve a poner Generar los datos en función de los valores seleccionados en los INPUTs
    """
    def get_new_data_divs_to_draw(
            purchases_and_sales_enriched_df, risk_diversification_criteria_dict_list, weight_criteria_column, case_to_update
    ):
        def get_risk_criteria_dict(risk_type, risk_diversification_criteria_dict_list):
            try:
                risk_criteria_dict = next(
                    risk_criteria_dict for risk_criteria_dict in risk_diversification_criteria_dict_list if
                    risk_criteria_dict.get("criteria_name") == risk_type)

            except StopIteration:
                print(f"RISK {risk_type} NOT FOUND !!!")
                raise Exception

            return risk_criteria_dict

        new_data_div_list = []

        if case_to_update == "company":
            risk_type = "company"
            risk_criteria_dict = get_risk_criteria_dict(risk_type, risk_diversification_criteria_dict_list)

            risk_by_company_panel_children = get_risk_diversification(
                purchases_and_sales_enriched_df,
                risk_criteria_dict,
                weight_criteria_column=weight_criteria_column
            )
            new_data_div_list.append(risk_by_company_panel_children)

        elif case_to_update == "sector":
            risk_type = "sector"
            risk_criteria_dict = get_risk_criteria_dict(risk_type, risk_diversification_criteria_dict_list)

            risk_by_sector_panel_children = get_risk_diversification(
                purchases_and_sales_enriched_df,
                risk_criteria_dict,
                weight_criteria_column=weight_criteria_column
            )
            new_data_div_list.append(risk_by_sector_panel_children)

        elif case_to_update == "country":
            risk_type = "country"
            risk_criteria_dict = get_risk_criteria_dict(risk_type, risk_diversification_criteria_dict_list)

            risk_by_country_panel_children = get_risk_diversification(
                purchases_and_sales_enriched_df,
                risk_criteria_dict,
                weight_criteria_column=weight_criteria_column
            )
            new_data_div_list.append(risk_by_country_panel_children)

        elif case_to_update == "currency":
            risk_type = "currency"
            risk_criteria_dict = get_risk_criteria_dict(risk_type, risk_diversification_criteria_dict_list)

            risk_by_currency_panel_children = get_risk_diversification(
                purchases_and_sales_enriched_df,
                risk_criteria_dict,
                weight_criteria_column=weight_criteria_column
            )
            new_data_div_list.append(risk_by_currency_panel_children)

        else:
            print(f"{case_to_update}--> AQUI NO HABRÍA QUE HABER LLEGADO!!!!")

        return new_data_div_list


    # Get filters
    column_filter_list = []
    owner_column_filter_dict = {'column_to_filter': 'owner', 'values_to_keep': selected_options_owner}
    broker_column_filter_dict = {'column_to_filter': 'broker', 'values_to_keep': selected_options_broker}

    column_filter_list.append(owner_column_filter_dict)
    column_filter_list.append(broker_column_filter_dict)

    # Get selections
    weight_criteria_column = selected_options_weight  # es el valor de una columna del DF ????

    # Get the ID of the Panel to update / overwrite its children attribute
    case_to_update = callback_context.outputs_grouping[0]['id']['index']

    # Get the data
    risk_diversification_criteria_dict_list = context['risk_diversification_criteria_dict_list'].copy()
    purchases_and_sales_enriched_df = data_utils.get_purchases_and_sales_enriched(column_filter_list)
    purchases_and_sales_enriched_df = purchases_and_sales_enriched_df[purchases_and_sales_enriched_df['ticker'].notna()]
    purchases_and_sales_enriched_df = purchases_and_sales_enriched_df[purchases_and_sales_enriched_df['stock_type'] == 'Acción']

    # Get the new content for the panel
    new_risk_diversification_div_list = get_new_data_divs_to_draw(
        purchases_and_sales_enriched_df,
        risk_diversification_criteria_dict_list,
        weight_criteria_column,
        case_to_update
    )

    return new_risk_diversification_div_list


@app.callback(
    [Output("page_warning_row", 'children')],
    [Input("weight_dropdown_selector", "value")]
)
def update_page_warning_row(selected_options_weight):
    """
    Borra o inserta un texto en la linea de "Warnings" general de la página
    """
    weight_criteria_column = selected_options_weight  # es el valor de una columna del DF ????
    #case_to_update = callback_context.outputs_grouping[0]['id']['index']
    print(weight_criteria_column)

    warning_col = risk_diversification_warnings.get_empty_warning_col()
    if weight_criteria_column == "latest_stock_value_in_euros":
        text = "ADVERTENCIA: los precios de las acciones tienen un RETRASO DE 1 O 2 DÍAS, por ser de la API gratuita de Yahoo"
        warning_col = risk_diversification_warnings.get_warning_col(text)
    return [warning_col]
