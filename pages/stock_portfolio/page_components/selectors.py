from dash import dcc
import dash_bootstrap_components as dbc
# import pages.risk_diversification.risk_diversification_data as risk_diversification_data
import pandas as pd
import utils.data_utils as data_utils
from dash import html


def get_page_general_selector_row(purchases_and_sales_log_df):
    def get_option_dict_list(df, column, value_for_all):
        column_type = df[column].dtype
        option_value_list = list(df[column].unique())
        # this removes the "nans" of the value list
        option_value_list = [value for value in option_value_list if not pd.isnull(value)]
        option_value_list.sort()

        # # Add a value that represents the selection of all elements
        # if value_for_all:
        #     option_value_list.append("Todo")

        if column_type == str:
            option_dict_list = [{'label': option.capitalize(), 'value': option} for option in option_value_list]
        else:
            option_dict_list = [{'label': option, 'value': option} for option in option_value_list]
        return option_dict_list

    def get_currency_dropdown_options():
        option_value_list = ['Euro', 'Moneda local']
        option_dict_list = [{'label': option.capitalize(), "value": option} for option in option_value_list]
        return option_dict_list

    def get_dropdown_div(selector_id, title, options_dict_list, default_selected_value, one_line, multiple_options=False, close_on_select=True):
        title_component = html.H3(f"{title}: ")
        dropdown_component = dcc.Dropdown(
                options=options_dict_list,
                value=default_selected_value,
                clearable=False,
                id=selector_id,
                multi=multiple_options,
                closeOnSelect=close_on_select
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
    owner_option_dict_list = get_option_dict_list(purchases_and_sales_log_df, "owner", True)
    broker_option_dict_list = get_option_dict_list(purchases_and_sales_log_df, "broker", True)

    ## particular cases
    currency_option_dict_list = get_currency_dropdown_options()

    owner_dropdown = get_dropdown_div("owner_dropdown_selector", "Propietario", owner_option_dict_list, "Todo", False, True, False)
    broker_dropdown = get_dropdown_div("broker_dropdown_selector", "Broker", broker_option_dict_list, "Todo", False,True, False)
    currency_dropdown = get_dropdown_div("currency_dropdown_selector", "Moneda", currency_option_dict_list, "Euro", False, False, True)

    # Add the filters to the filter list
    selector_list.append(owner_dropdown)
    selector_list.append(broker_dropdown)
    selector_list.append(currency_dropdown)

    # wrap each filter in a Bootstrap Column
    for selector_div in selector_list:
        selector_col_list.append(dbc.Col([selector_div]))

    selector_row = dbc.Row(selector_col_list, className="selector-div")

    return selector_row

