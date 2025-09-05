from utils.global_variables import context
import utils.data_utils as data_utils


def get_stock_portfolio_data(filter_dict_list=[], columns_to_keep_list=[], user_column_names_dict={}):
    # I get the base data
    purchases_and_sales_enriched_df = data_utils.get_purchases_and_sales_enriched()
    company_stock_prices_df = context['company_stock_prices_df']

    # I apply the filters
    for filter_dict in filter_dict_list:
        column_to_filter = filter_dict['column_to_apply_filter']
        values_to_keep_list = filter_dict['values_to_keep']
        if 'Todo' not in values_to_keep_list:
            purchases_and_sales_enriched_df = purchases_and_sales_enriched_df[purchases_and_sales_enriched_df[column_to_filter].isin(values_to_keep_list)]

    # I clean the Dataset to remove the Nulls and the registers that are not Stocks
    purchases_and_sales_enriched_df = purchases_and_sales_enriched_df[purchases_and_sales_enriched_df['Ticker'].notna()]
    purchases_and_sales_enriched_df = purchases_and_sales_enriched_df[purchases_and_sales_enriched_df['Tipo de Valor'] == 'Acción']
    #purchases_and_sales_enriched_df['Acciones'] = purchases_and_sales_enriched_df.apply(lambda row: row['Acciones'] * -1 if row['Acción'] == 'Venta' else row['Acciones'], axis=1)
    #purchases_and_sales_enriched_df['Dinero'] = purchases_and_sales_enriched_df.apply(lambda row: row['Dinero']*-1 if row['Acción'] == 'Venta' else row['Dinero'], axis=1)

    # I prepare the portfolio table
    ## Sum all the purchases and sales
    stock_portfolio_df = purchases_and_sales_enriched_df.groupby(['Mercado', 'Ticker', 'Nombre Empresa']).sum()[['Acciones', 'Dinero', 'Dinero (EUR)', 'Dinero pagado en Comisión', 'Dinero pagado en comisión (EUR)']]
    ## I re-add certain lost columns that are important to keep and others that I want to keep
    stock_portfolio_df = stock_portfolio_df.reset_index()

    stock_portfolio_df = stock_portfolio_df.merge(purchases_and_sales_enriched_df[['Ticker', 'Mercado', "ISIN", "Moneda del mercado", "Pais", "REIT", "Sector", "Meses Pago Dividendos"]], on=['Ticker', 'Mercado'])
    stock_portfolio_df = stock_portfolio_df.drop_duplicates()
    ## Get the statistics of the invested money
    stock_portfolio_df['invested_money_with_comissions'] = stock_portfolio_df.apply(lambda row: row['Dinero'] + row['Dinero pagado en Comisión'], axis=1)
    stock_portfolio_df['invested_money_with_comissions_in_euros'] = stock_portfolio_df.apply(lambda row: row['Dinero'] + row['Dinero pagado en comisión (EUR)'], axis=1)

    stock_portfolio_df['mean_price'] = stock_portfolio_df.apply(lambda row: row['Dinero']/row['Acciones'], axis=1)
    stock_portfolio_df['mean_price_in_euros'] = stock_portfolio_df.apply(lambda row: row['Dinero (EUR)']/row['Acciones'], axis=1)

    stock_portfolio_df['mean_price_with_comissions'] = stock_portfolio_df.apply(lambda row: row['invested_money_with_comissions']/row['Acciones'], axis=1)
    stock_portfolio_df['mean_price_with_comissions_in_euros'] = stock_portfolio_df.apply(lambda row: row['invested_money_with_comissions_in_euros']/row['Acciones'], axis=1)

    ## Get the current stock price of the portfolio
    stock_portfolio_df = stock_portfolio_df.merge(company_stock_prices_df, on=['Ticker', 'Mercado'])
    stock_portfolio_df['company_value'] = stock_portfolio_df.apply(lambda row: row['Acciones'] * row['latest_stock_price'], axis=1)
    stock_portfolio_df['company_value_in_euros'] = stock_portfolio_df.apply(lambda row: row['Acciones'] * row['latest_stock_price_in_euros'], axis=1)

    # always_to_keep_column_list_part_1 = [
    #     "Ticker", "Mercado", "Nombre Empresa", "Acciones",
    #
    # ]
    # if currency_criteria_column == "Euro":
    #     currency_columns_list = [
    #         "Dinero (EUR)", "Dinero pagado en comisión (EUR)",
    #         "invested_money_with_comissions_in_euros", "mean_price_in_euros",
    #         "mean_price_with_comissions_in_euros", "company_value_in_euros"
    #     ]
    # else:
    #     currency_columns_list = [
    #         "Dinero", "Moneda del pago", "Dinero pagado en Comisión",
    #         "Moneda de la comisión", "invested_money_with_comissions",
    #         "mean_price", "mean_price_with_comissions", "company_value"
    #     ]
    # # Columns that I want to keep, but I want them to be the LAST in the showed table
    # always_to_keep_column_list_part_2 = [
    #     "ISIN", "Pais", "REIT", "Sector", "Meses Pago Dividendos"
    # ]


    # I select the columns to keep
    if len(columns_to_keep_list) == 0:
        columns_to_keep_list = stock_portfolio_df.columns
    stock_portfolio_df = stock_portfolio_df[columns_to_keep_list]

    stock_portfolio_df = stock_portfolio_df.rename(user_column_names_dict, axis=1)
    return stock_portfolio_df
