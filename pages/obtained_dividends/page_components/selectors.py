from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import utils.data_utils as data_utils
import datetime


def get_page_general_selector_row(obtained_dividends_df):
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

    def get_month_dict_list():
        month_dict = data_utils.get_month_dict()
        option_dict_list = [{'label': value.capitalize(), 'value': key} for key, value in month_dict.items()]
        # option_dict_list.append({'label': "Todo", 'value': "Todo"})
        return option_dict_list

    def get_currency_option_dict_list():
        option_value_list = ['Euro', 'Moneda local']
        option_dict_list = [{'label': option.capitalize(), "value": option} for option in option_value_list]
        return option_dict_list

    def get_revenue_type_option_dict_list():
        option_value_list = ['Bruto', 'Neto']
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
    owner_option_dict_list = get_option_dict_list(obtained_dividends_df, "Propietario", True)
    broker_option_dict_list = get_option_dict_list(obtained_dividends_df, "Broker", True)
    stock_market_option_dict_list = get_option_dict_list(obtained_dividends_df, "Mercado", True)
    country_option_dict_list = get_option_dict_list(obtained_dividends_df, "stock_market_country", True)
    year_option_dict_list = get_option_dict_list(obtained_dividends_df, "Año Cobro", False)

    ## particular cases
    month_option_dict_list = get_month_dict_list()
    currency_option_dict_list = get_currency_option_dict_list()
    revenue_type_option_dict_list = get_revenue_type_option_dict_list()

    # # Default values
    # owner_option_default_values = obtained_dividends_df["Propietario"].unique()
    # broker_option_default_values = obtained_dividends_df["Broker"].unique()
    # # get the current year
    # # current_year = datetime.datetime.now().year
    # year_option_default_values = obtained_dividends_df["Año Cobro"].unique()
    # month_option_default_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # country_option_default_values = obtained_dividends_df["stock_market_country"].unique()
    # stock_market_option_default_values = obtained_dividends_df["Mercado"].unique()

    # Default values
    owner_option_default_values = []
    broker_option_default_values = []
    # get the current year
    # current_year = datetime.datetime.now().year
    year_option_default_values = []
    month_option_default_values = []
    country_option_default_values = []
    stock_market_option_default_values = []

    # generate the filters
    owner_dropdown = get_dropdown_div("owner_dropdown_selector", "Propietario", owner_option_dict_list, owner_option_default_values, False, True, False)
    broker_dropdown = get_dropdown_div("broker_dropdown_selector", "Broker", broker_option_dict_list, broker_option_default_values, False, True, False)
    year_dropdown = get_dropdown_div("year_dropdown_selector", "Año", year_option_dict_list, year_option_default_values, False, True, False)
    month_dropdown = get_dropdown_div("month_dropdown_selector", "Mes", month_option_dict_list, month_option_default_values, False,True, False)
    country_dropdown = get_dropdown_div("country_dropdown_selector", "País de la cotización", country_option_dict_list, country_option_default_values, False, True, False)
    stock_market_dropdown = get_dropdown_div("stock_market_dropdown_selector", "Bolsa de la cotización", stock_market_option_dict_list, stock_market_option_default_values, False, True, False)
    currency_dropdown = get_dropdown_div("currency_dropdown_selector", "Moneda", currency_option_dict_list, "Euro", False, False, True)
    revenue_type_dropdown = get_dropdown_div("revenue_type_dropdown_selector", "Bruto o Neto", revenue_type_option_dict_list, "Bruto", False, False, True)

    # Add the filters to the filter list
    selector_list.append(owner_dropdown)
    selector_list.append(broker_dropdown)
    selector_list.append(year_dropdown)
    selector_list.append(month_dropdown)
    selector_list.append(country_dropdown)
    selector_list.append(stock_market_dropdown)
    selector_list.append(currency_dropdown)
    selector_list.append(revenue_type_dropdown)

    # wrap each filter in a Bootstrap Column
    for selector_div in selector_list:
        selector_col_list.append(dbc.Col([selector_div]))

    selector_row = dbc.Row(selector_col_list, className="selector-div")
    return selector_row
