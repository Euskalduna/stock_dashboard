from utils.global_variables import context
import utils.data_utils as data_utils


def get_stock_portfolio(purchases_and_sales_enriched_df, filter_dict_list=[], columns_to_keep_list=[], user_column_names_dict={}):
    # I get the base data
    company_stock_prices_df = context['company_stock_prices_df']

    # Get the registers to keep
    filtered_obtained_dividends_df = data_utils.get_data_filtered_by_dropdowns(purchases_and_sales_enriched_df, filter_dict_list)

    # I clean the Dataset to remove the Nulls and the registers that are not Stocks
    filtered_obtained_dividends_df = filtered_obtained_dividends_df[filtered_obtained_dividends_df['ticker'].notna()]
    filtered_obtained_dividends_df = filtered_obtained_dividends_df[filtered_obtained_dividends_df['stock_type'] == 'Acción']
    #purchases_and_sales_enriched_df['Acciones'] = purchases_and_sales_enriched_df.apply(lambda row: row['Acciones'] * -1 if row['Acción'] == 'Venta' else row['Acciones'], axis=1)
    #purchases_and_sales_enriched_df['Dinero'] = purchases_and_sales_enriched_df.apply(lambda row: row['Dinero']*-1 if row['Acción'] == 'Venta' else row['Dinero'], axis=1)

    # I put as negatives the "sales"
    sales_condition = (filtered_obtained_dividends_df["stock_type"] == "Acción") & (filtered_obtained_dividends_df["action"] == "Venta")
    sales_columns_to_alter = ["stock_quantity", "payed_money", "payed_money_in_euros"]
    filtered_obtained_dividends_df.loc[sales_condition, sales_columns_to_alter] = filtered_obtained_dividends_df.loc[sales_condition, sales_columns_to_alter] * -1

    # I prepare the portfolio table
    ## Sum all the purchases and sales
    stock_portfolio_df = filtered_obtained_dividends_df.groupby(['market', 'ticker', 'company_name']).sum()[['stock_quantity', 'payed_money', 'payed_money_in_euros', 'payed_fee', 'payed_fee_in_euros']]
    ## I remove the companies that have been completely selled
    stock_portfolio_df = stock_portfolio_df[stock_portfolio_df["stock_quantity"] != 0]

    ## I re-add certain lost columns that are important to keep and others that I want to keep
    stock_portfolio_df = stock_portfolio_df.reset_index()

    stock_portfolio_df = stock_portfolio_df.merge(filtered_obtained_dividends_df[['ticker', 'market', "isin", "market_currency", "country", "reit", "sector", "dividend_payment_months"]], on=['ticker', 'market'])
    stock_portfolio_df = stock_portfolio_df.drop_duplicates()

    ## Get the statistics of the invested money
    stock_portfolio_df['invested_money_with_comissions'] = stock_portfolio_df.apply(lambda row: row['payed_money'] + row['payed_fee'], axis=1)
    stock_portfolio_df['invested_money_with_comissions_in_euros'] = stock_portfolio_df.apply(lambda row: row['payed_money_in_euros'] + row['payed_fee_in_euros'], axis=1)

    stock_portfolio_df['mean_price'] = stock_portfolio_df.apply(lambda row: row['payed_money']/row['stock_quantity'], axis=1)
    stock_portfolio_df['mean_price_in_euros'] = stock_portfolio_df.apply(lambda row: row['payed_money_in_euros']/row['stock_quantity'], axis=1)

    stock_portfolio_df['mean_price_with_comissions'] = stock_portfolio_df.apply(lambda row: row['invested_money_with_comissions']/row['stock_quantity'], axis=1)
    stock_portfolio_df['mean_price_with_comissions_in_euros'] = stock_portfolio_df.apply(lambda row: row['invested_money_with_comissions_in_euros']/row['stock_quantity'], axis=1)

    ## Get the current stock price of the portfolio
    stock_portfolio_df = stock_portfolio_df.merge(company_stock_prices_df, on=['ticker', 'market'])
    stock_portfolio_df['company_value'] = stock_portfolio_df.apply(lambda row: row['stock_quantity'] * row['latest_stock_price'], axis=1)
    stock_portfolio_df['company_value_in_euros'] = stock_portfolio_df.apply(lambda row: row['stock_quantity'] * row['latest_stock_price_in_euros'], axis=1)


    # I select the columns to keep
    if len(columns_to_keep_list) == 0:
        columns_to_keep_list = stock_portfolio_df.columns
    stock_portfolio_df = stock_portfolio_df[columns_to_keep_list]

    stock_portfolio_df = stock_portfolio_df.rename(user_column_names_dict, axis=1)
    return stock_portfolio_df
