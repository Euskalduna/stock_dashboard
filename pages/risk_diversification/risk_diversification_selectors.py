from dash import dcc
import dash_bootstrap_components as dbc
# import pages.risk_diversification.risk_diversification_data as risk_diversification_data
import pandas as pd
import utils.data_utils as data_utils
from dash import html

def get_page_general_selector_row(risk_diversification_criteria_dict_list):
    def get_diversification_checklist_options(risk_diversification_criteria_dict_list):
        option_value_list = [risk_criteria_dict['criteria_name'] for risk_criteria_dict in risk_diversification_criteria_dict_list]
        option_dict_list = [{'label': option.capitalize(), "value": option} for option in option_value_list]
        return option_dict_list

    def get_owner_dropdown_options():
        df = data_utils.get_purchases_and_sales_log()
        option_value_list = list(df['Propietario'].unique())
        option_value_list.append("Todo")
        # Esto es para limpiar la lista de valores de posibles "nans"
        option_value_list = [value for value in option_value_list if not pd.isnull(value)]
        option_value_list.sort()
        option_dict_list = [{'label': option.capitalize(), 'value': option} for option in option_value_list]
        return option_dict_list

    def get_broker_dropdown_options():
        df = data_utils.get_purchases_and_sales_log()
        option_value_list = list(df['Broker'].unique())
        option_value_list.append("Todo")
        # Esto es para limpiar la lista de valores de posibles "nans"
        option_value_list = [value for value in option_value_list if not pd.isnull(value)]
        option_value_list.sort()
        option_dict_list = [{'label': option.capitalize(), 'value': option} for option in option_value_list]
        return option_dict_list

    diversification_option_dict_list = get_diversification_checklist_options(risk_diversification_criteria_dict_list)
    owner_option_dict_list = get_owner_dropdown_options()
    broker_option_dict_list = get_broker_dropdown_options()

    selector_row = dbc.Row([
        # dbc.Col([dcc.Dropdown(
        #     options=[option_dict['value'] for option_dict in owner_option_dict_list],
        #     value='Todo',
        #     clearable=False,
        #     id="owner_dropdown_selector",
        # )
        # ], width=2),

        dbc.Col([
            dbc.Row(dbc.Col([html.H3("Propietario: ")])),
            dbc.Row(dbc.Col(
                [dcc.Dropdown(
                    options=[option_dict['value'] for option_dict in owner_option_dict_list],
                    value='Todo',
                    clearable=False,
                    id="owner_dropdown_selector",
                )]
            )),
        ], width=2),

        dbc.Col([
            dbc.Row(dbc.Col([html.H3("Broker: ")])),
            dbc.Row(dbc.Col(
                [dcc.Dropdown(
                    options=[option_dict['value'] for option_dict in broker_option_dict_list],
                    value='Todo',
                    clearable=False,
                    id="broker_dropdown_selector",
                )]
            )),
        ], width=2),

        # TODO: Cuando tenga la forma de scar los pesos por cotizacion, QUITAR LA CLASSNAME="d-none"!!!
        dbc.Col([
            dbc.Row(dbc.Col([html.H3("Peso: ")])),
            dbc.Row(dbc.Col(
                [dcc.Dropdown(
                    options=[
                        {'label': 'Dinero Invertido (Euros)', 'value': 'Dinero (EUR)'},
                        {'label': 'Peso de Cotizacion (Euros)', 'value': 'Ultimo Valor (EUR)'}
                        # {'label': 'Peso de Cotizacion (Euros)', 'value': 'Dinero'}
                    ],
                    value='Dinero (EUR)',
                    clearable=False,
                    id="weight_dropdown_selector",
                )])
            ),
        ], width=2, className=""),

        dbc.Col([dcc.Checklist(
            options=diversification_option_dict_list,
            inline=True,
            value=[option_dict['value'] for option_dict in diversification_option_dict_list],
            id="diversification_section_checklist",
            labelStyle={'display': 'inline-block', 'margin-right': '2%', 'padding-right': '1%'})
        ], width=3)
    ], className="selector-div")
    return selector_row


def get_data_panel_data_checklist(checklist_id):
    selector_row = dbc.Row([
        dbc.Col([dcc.Checklist(
            options=[{'label': 'Grafico', 'value': 'chart'}, {'label': 'Tabla', 'value': 'table'}],
            inline=True,
            value=['chart', 'table'],
            id=checklist_id
        )])
    ])
    return selector_row
