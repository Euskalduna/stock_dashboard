from dash import Output, Input, MATCH, callback_context
from app import app

import pages.stock_portfolio.page_components.body as stock_portfolio_body
import pages.stock_portfolio.data as stock_portfolio_data
import utils.data_utils as data_utils
from pages.stock_portfolio.page_components.panels.stock_portfolio import get_portfolio_table

# @app.callback(
#     [Output({'type': 'stock-portfolio-data-panel', 'index': MATCH}, 'children')],
#     [Input("owner_dropdown_selector", "value"),
#      Input("broker_dropdown_selector", "value"),
#      Input("currency_dropdown_selector", "value")]
# )
# def update_page_data_old(selected_options_owner, selected_options_broker, selected_options_currency):
#     """
#     Borra y vuelve a poner Generar los datos en función de los valores seleccionados en los INPUTs
#     """
#     print("HOLAAAA")
#
#     def get_columns_by_currency(currency_criteria_column):
#         # TODO: hacer algo para que esto sea dinamico y no esté Hardcodeado!!!!!
#         # Columns that I want to keep but I want them to be the FIRST in the showed table
#         always_to_keep_column_list_part_1 = [
#             "Nombre Empresa", "Mercado", "Ticker", "Acciones",
#         ]
#         if currency_criteria_column == "Euro":
#             currency_columns_list = [
#                 "Dinero (EUR)", "Dinero pagado en comisión (EUR)",
#                 "invested_money_with_comissions_in_euros", "mean_price_in_euros",
#                 "mean_price_with_comissions_in_euros", "company_value_in_euros"
#             ]
#         else:
#             currency_columns_list = [
#                 "Moneda del mercado", "Dinero", "Dinero pagado en Comisión",
#                 "invested_money_with_comissions",
#                 "mean_price", "mean_price_with_comissions", "company_value"
#             ]
#         # Columns that I want to keep, but I want them to be the LAST in the showed table
#         always_to_keep_column_list_part_2 = [
#             "ISIN", "Pais", "REIT", "Sector", "Meses Pago Dividendos"
#         ]
#         columns_to_keep_list = always_to_keep_column_list_part_1 + currency_columns_list + always_to_keep_column_list_part_2
#         return columns_to_keep_list
#
#     def get_user_column_names():
#         user_column_names_dict = {
#             'Nombre Empresa': 'Nombre',
#             'Ticket': 'Ticket',
#             'Mercado': 'Mercado',
#             'Acciones': 'Acciones',
#             'Dinero (EUR)': 'Dinero (EUR)',
#             'Dinero pagado en comisión (EUR)': 'Dinero pagado en comisión (EUR)',
#             'invested_money_with_comissions_in_euros': 'Dinero invertido (con comisiones) (EUR)',
#             'mean_price_in_euros': 'Precio Medio (EUR)',
#             'mean_price_with_comissions_in_euros': 'Precio Medio (con comisiones) (EUR)',
#             'company_value_in_euros': 'Valor acciones (EUR)',
#             'invested_money_with_comissions': 'Dinero invertido (con comisiones)',
#             'mean_price': 'Precio Medio',
#             'mean_price_with_comissions': 'Precio Medio (con comisiones)',
#             'company_value': 'Valor acciones',
#             'ISIN': 'ISIN',
#             'Pais': 'Pais',
#             'REIT': 'REIT',
#             'Sector': 'Sector',
#             'Meses Pago Dividendos': 'Meses Pago Dividendos',
#             'Moneda del mercado': 'Moneda del mercado',
#             'Dinero pagado en Comisión': 'Dinero pagado en Comisiones',
#         }
#         return user_column_names_dict
#
#     def get_new_data_divs_to_draw(stock_portfolio_df, filter_dict_list, columns_to_keep_list, user_column_names_dict, case_to_update):
#         new_data_div_list = []
#         if case_to_update == 'portfolio':
#             # Get de div of each sector of the page (that is supposed to contain data)
#             panel_children = stock_portfolio_body.get_panel(stock_portfolio_df)
#
#             panel_children = get_portfolio_table(
#                 stock_portfolio_df,
#                 columns_to_keep_list,
#                 user_column_names_dict,
#                 filter_dict_list=filter_dict_list
#             )
#             new_stock_portfolio_div_list.append(panel_children)
#         else:
#             print(f"{case_to_update}--> AQUI NO HABRÍA QUE HABER LLEGADO!!!!")
#
#         return new_data_div_list
#
#     # Get the data
#     # stock_portfolio_df = stock_portfolio_data.get_page_data()
#     stock_portfolio_df = stock_portfolio_data.get_stock_portfolio_data()
#     ## Consigo el diccionario que se utilizará para renombrar las columnas con un nombre "User friendly"
#     user_column_names_dict = get_user_column_names()
#
#     # Get filters
#     column_filter_list = []
#     owner_column_filter_dict = {'column_to_filter': 'owner', 'values_to_keep': selected_options_owner}
#     broker_column_filter_dict = {'column_to_filter': 'broker', 'values_to_keep': selected_options_broker}
#
#     column_filter_list.append(owner_column_filter_dict)
#     column_filter_list.append(broker_column_filter_dict)
#
#     # Get selections
#     currency_criteria_column = selected_options_currency
#     ## A partir de las selecciones, pongo qué columnas se han de mostrar
#     columns_to_keep_list = get_columns_by_currency(currency_criteria_column)
#
#     # Get the ID of the Panel to update / overwrite its children attribute
#     case_to_update = callback_context.outputs_grouping[0]['id']['index']
#
#     # Get the new content for the panel
#     ## Get the new data to draw in the browser
#     new_stock_portfolio_div_list = get_new_data_divs_to_draw(
#         stock_portfolio_df,
#         column_filter_list,
#         columns_to_keep_list,
#         user_column_names_dict,
#         case_to_update
#     )
#
#     return new_stock_portfolio_div_list



@app.callback(
    [Output({'type': 'stock-portfolio-data-panel', 'index': MATCH}, 'children')],
    [Input("owner_dropdown_selector", "value"),
     Input("broker_dropdown_selector", "value"),
     Input("currency_dropdown_selector", "value")]
)
def update_page_data(selected_options_owner, selected_options_broker, selected_options_currency):
    """
    Borra y vuelve a poner Generar los datos en función de los valores seleccionados en los INPUTs
    """
    print("HOLAAAA")

    def get_columns_by_currency(currency_criteria_column):
        # TODO: hacer algo para que esto sea dinamico y no esté Hardcodeado!!!!!
        # Columns that I want to keep but I want them to be the FIRST in the showed table
        always_to_keep_column_list_part_1 = [
            "Nombre Empresa", "Mercado", "Ticker", "Acciones",
        ]
        if currency_criteria_column == "Euro":
            currency_columns_list = [
                "Dinero (EUR)", "Dinero pagado en comisión (EUR)",
                "invested_money_with_comissions_in_euros", "mean_price_in_euros",
                "mean_price_with_comissions_in_euros", "company_value_in_euros"
            ]
        else:
            currency_columns_list = [
                "Moneda del mercado", "Dinero", "Dinero pagado en Comisión",
                "invested_money_with_comissions",
                "mean_price", "mean_price_with_comissions", "company_value"
            ]
        # Columns that I want to keep, but I want them to be the LAST in the showed table
        always_to_keep_column_list_part_2 = [
            "ISIN", "Pais", "REIT", "Sector", "Meses Pago Dividendos"
        ]
        columns_to_keep_list = always_to_keep_column_list_part_1 + currency_columns_list + always_to_keep_column_list_part_2
        return columns_to_keep_list

    def get_user_column_names():
        user_column_names_dict = {
            'Nombre Empresa': 'Nombre',
            'Ticket': 'Ticket',
            'Mercado': 'Mercado',
            'Acciones': 'Acciones',
            'Dinero (EUR)': 'Dinero (EUR)',
            'Dinero pagado en comisión (EUR)': 'Dinero pagado en comisión (EUR)',
            'invested_money_with_comissions_in_euros': 'Dinero invertido (con comisiones) (EUR)',
            'mean_price_in_euros': 'Precio Medio (EUR)',
            'mean_price_with_comissions_in_euros': 'Precio Medio (con comisiones) (EUR)',
            'company_value_in_euros': 'Valor acciones (EUR)',
            'invested_money_with_comissions': 'Dinero invertido (con comisiones)',
            'mean_price': 'Precio Medio',
            'mean_price_with_comissions': 'Precio Medio (con comisiones)',
            'company_value': 'Valor acciones',
            'ISIN': 'ISIN',
            'Pais': 'Pais',
            'REIT': 'REIT',
            'Sector': 'Sector',
            'Meses Pago Dividendos': 'Meses Pago Dividendos',
            'Moneda del mercado': 'Moneda del mercado',
            'Dinero pagado en Comisión': 'Dinero pagado en Comisiones',
        }
        return user_column_names_dict

    def get_new_data_divs_to_draw(stock_portfolio_df, case_to_update):
        new_data_div_list = []
        if case_to_update == 'portfolio':
            # Get de div of each sector of the page (that is supposed to contain data)
            panel_children = get_portfolio_table(
                stock_portfolio_df
            )
            new_data_div_list.append(panel_children)
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
    currency_criteria_column = selected_options_currency
    ## A partir de las selecciones, pongo qué columnas se han de mostrar
    # columns_to_keep_list = get_columns_by_currency(currency_criteria_column)

    # Get the data
    purchases_and_sales_enriched_df = data_utils.get_purchases_and_sales_enriched(filter_dict_list=column_filter_list)
    stock_portfolio_df = stock_portfolio_data.get_stock_portfolio(purchases_and_sales_enriched_df)
    # TODO: aqui deberia de eliminar las columnas que no quiero mostrar segun la moneda seleccionada

    # Get the ID of the Panel to update / overwrite its children attribute
    case_to_update = callback_context.outputs_grouping[0]['id']['index']

    # Get the new content for the panel
    ## Get the new data to draw in the browser
    new_stock_portfolio_div_list = get_new_data_divs_to_draw(
        stock_portfolio_df,
        case_to_update
    )

    return new_stock_portfolio_div_list

