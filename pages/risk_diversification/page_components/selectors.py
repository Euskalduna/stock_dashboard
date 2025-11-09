from dash import dcc
import dash_bootstrap_components as dbc
# import pages.risk_diversification.risk_diversification_data as risk_diversification_data
import pandas as pd
import utils.data_utils as data_utils
from dash import html


def get_page_general_selector_row(purchases_and_sales_enriched_df, risk_diversification_criteria_dict_list, default_weight_criteria_column):
    def get_diversification_checklist_options(risk_diversification_criteria_dict_list):
        option_value_list = [risk_criteria_dict['criteria_name'] for risk_criteria_dict in risk_diversification_criteria_dict_list]
        option_dict_list = [{'label': option.capitalize(), "value": option} for option in option_value_list]
        return option_dict_list

    def get_option_dict_list(df, column, value_for_all):
        column_type = df[column].dtype
        option_value_list = list(df[column].unique())
        # this removes the "nans" of the value list
        option_value_list = [value for value in option_value_list if not pd.isnull(value)]
        option_value_list.sort()

        # Add a value that represents the selection of all elements
        if value_for_all:
            option_value_list.append("Todo")

        if column_type == str:
            option_dict_list = [{'label': option.capitalize(), 'value': option} for option in option_value_list]
        else:
            option_dict_list = [{'label': option, 'value': option} for option in option_value_list]
        return option_dict_list

    def get_weight_option_dict_list():
        option_dict_list = []
        option_dict_list.append({'label': 'Dinero Invertido (Euros)', 'value': 'Dinero (EUR)'})
        option_dict_list.append({'label': 'Peso de Cotizacion (Euros)', 'value': 'Ultimo Valor (EUR)'})
        return option_dict_list

    def get_dropdown_div(selector_id, title, options_dict_list, default_selected_value, one_line):
        title_component = html.H3(f"{title}: ")
        dropdown_component = dcc.Dropdown(
                options=options_dict_list,
                value=default_selected_value,
                clearable=False,
                id=selector_id,
            )

        if one_line:
            dropdown_div = html.Div([
                dbc.Row([
                    dbc.Col([title_component]),
                    dbc.Col([dropdown_component])
                ])
            ])
        else:
            dropdown_div = html.Div([
                dbc.Row(dbc.Col([title_component])),
                dbc.Row(dbc.Col([dropdown_component]))
            ])

        return dropdown_div

    selector_list = []
    selector_col_list = []

    # get the option dict lists
    ## general cases
    owner_option_dict_list = get_option_dict_list(purchases_and_sales_enriched_df, "Propietario", True)
    broker_option_dict_list = get_option_dict_list(purchases_and_sales_enriched_df, "Broker", True)

    ## particular cases
    weight_option_dict_list = get_weight_option_dict_list()
    diversification_option_dict_list = get_diversification_checklist_options(risk_diversification_criteria_dict_list)

    # generate the filters
    ## general cases
    owner_dropdown = get_dropdown_div("owner_dropdown_selector", "Propietario", owner_option_dict_list, "Todo", False)
    broker_dropdown = get_dropdown_div("broker_dropdown_selector", "Broker", broker_option_dict_list, "Todo", False)
    weight_dropdown = get_dropdown_div("weight_dropdown_selector", "Peso", weight_option_dict_list, default_weight_criteria_column, False)

    ## particular cases
    diversification_section_checklist = dcc.Checklist(
        options=diversification_option_dict_list,
        inline=True,
        value=[option_dict['value'] for option_dict in diversification_option_dict_list],
        id="diversification_section_checklist",
        labelStyle={'display': 'inline-block', 'marginRight': '2%', 'paddingRight': '1%'}
    )

    # Add the filters to the filter list
    selector_list.append(owner_dropdown)
    selector_list.append(broker_dropdown)
    selector_list.append(weight_dropdown)
    selector_list.append(diversification_section_checklist)

    # wrap each filter in a Bootstrap Column
    for selector_div in selector_list:
        selector_col_list.append(dbc.Col([selector_div]))

    selector_row = dbc.Row(selector_col_list, className="selector-div")
    return selector_row


def get_data_panel_data_checklist(checklist_id):
    selector_row = dbc.Row([
        dbc.Col([dcc.Checklist(
            options=[{'label': 'Gráfico', 'value': 'chart'}, {'label': 'Tabla', 'value': 'table'}],
            inline=True,
            value=['chart', 'table'],
            id=checklist_id
        )])
    ])
    return selector_row
