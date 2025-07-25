from dash import dcc
from dash.dash_table import DataTable
from dash.dash_table.Format import Format, Group, Scheme

import utils.data_utils as data_utils
import pages.stock_portfolio.stock_portfolio_data as stock_portfolio_data
import pages.stock_portfolio.stock_portfolio_titles as stock_portfolio_titles
import pages.stock_portfolio.stock_portfolio_selectors as stock_portfolio_selectors

import pages.risk_diversification.risk_diversification_data as risk_diversification_data
import pages.risk_diversification.risk_diversification_selectors as risk_diversification_selectors
import plotly.express as px
import dash_bootstrap_components as dbc


def get_body_row():
    # get body_panel
    panel_children = get_panel()  # Esto va a devolver un [elemento, elemento2, elemento3]

    # get the body's layout / get the distribution of the panels in the body
    col_id = {'type': 'stock-portfolio-data-panel', 'index': 'portfolio'}
    data_row_list = [dbc.Row(dbc.Col(panel_children, id=col_id))]
    body_row = dbc.Row(dbc.Col(data_row_list))
    return body_row


def get_panel(filter_dict_list=[], columns_to_keep_list=[], user_column_names_dict={}):
    # Parametría
    title = f""
    # visualization_checklist_id = {'type': 'visualization-checklist', 'index': risk_criteria_name}
    table_id = {'type': 'table-container', 'index': 'portfolio_table'}

    # get_data
    stock_portfolio_df = stock_portfolio_data.get_stock_portfolio_data(filter_dict_list, columns_to_keep_list, user_column_names_dict)
    non_numeric_column_list = ['Propietario', 'Mercado', 'Ticker', 'Nombre']

    # Creacion de elementos
    table_html_component = get_stock_portfolio_table(stock_portfolio_df, non_numeric_column_list)

    # Montaje
    title_row = stock_portfolio_titles.get_page_common_panel_title_row(title)
    # selector_row = stock_portfolio_selectors.get_data_panel_data_checklist(visualization_checklist_id)
    data_row = get_panel_body_row(table_html_component, table_id)
    return [title_row, data_row]


def get_panel_body_row(table, table_id):
    data_row = dbc.Row([
        dbc.Col([table], id=table_id)
    ])
    return data_row


## TODO: MUEVO ESTO A UN ARCHIVO DE PANEL COMPONENTS / CHARTS / TABLES??????? y ahi creo todas las graficas tablas y demás que me apetezca????
def get_stock_portfolio_table(stock_portfolio_df, non_numeric_column_list):
    def get_configurated_table_columns(df, non_numeric_column_list):
        table_column_dict_list = []

        for column in df.columns:
            if column == "Acciones":
                format_weight = Format(decimal_delimiter=',', group_delimiter='.', group=Group.yes, groups=[3])
            else:
                format_weight = Format(decimal_delimiter=',', group_delimiter='.', group=Group.yes, groups=[3], precision=2, scheme=Scheme.fixed)

            column_type = 'text' if column == non_numeric_column_list else 'numeric'
            column_format = format_weight if column_type == 'numeric' else None

            table_column_dict_list.append({'id': column, 'name': column, 'type': column_type, 'format': column_format})

        return table_column_dict_list

    # Creacion de tabla
    ## Orden y seleccion de columnas
    # stock_portfolio_df = stock_portfolio_df[['Mercado', 'Ticker', 'Nombre Empresa', 'Acciones', 'Dinero', 'Dinero(EUR)', 'Dinero pagado en Comisión', 'Dinero pagado en comisión (EUR)', 'latest_stock_price_in_euros', 'invested_money_with_comissions', 'invested_money_with_comissions_in_euros', 'mean_price', 'mean_price_in_euros', 'mean_price_with_comissions', 'mean_price_with_comissions_in_euros', 'company_value', 'company_value_in_euros']]
    #TODO: pongo aqui el filtro de cosas a mantener como columnas de la tabla o lo pongo en el UPDATE de los datos????? ---------> Lo he puesto en el UPDATE!!!!!
    # stock_portfolio_df = stock_portfolio_df[
    #     ['Mercado', 'Nombre Empresa', 'Acciones', 'Dinero (EUR)',
    #      'Dinero pagado en comisión (EUR)', 'latest_stock_price_in_euros',
    #      'invested_money_with_comissions_in_euros', 'mean_price_in_euros',
    #      'mean_price_with_comissions_in_euros', 'company_value_in_euros']]

    # stock_portfolio_df = stock_portfolio_df[
    #     ['Mercado', 'Nombre Empresa', 'Acciones', 'Dinero',
    #      'Dinero pagado en Comisión', 'latest_stock_price',
    #      'invested_money_with_comissions', 'mean_price',
    #      'mean_price_with_comissions', 'company_value']]

    table_data = stock_portfolio_df.to_dict('records')
    # table_columns = [{"name": i, "id": i} for i in weight_by_criteria_df.columns]
    table_columns = get_configurated_table_columns(stock_portfolio_df, non_numeric_column_list)

    weight_by_criteria_table_html_component = DataTable(data=table_data,
                                                        columns=table_columns,
                                                        page_size=15,
                                                        # filter_action="native",
                                                        sort_action="native",
                                                        id="stock-portfolio-table",
                                                        style_table={'overflowX': 'auto'},
                                                        style_data={"whiteSpace": "normal", "height": "auto"},
                                                        style_header={"whiteSpace": "normal",
                                                                      "height": "auto"},
                                                        style_cell={"minWidth": 100}
                                                        )

    return weight_by_criteria_table_html_component
