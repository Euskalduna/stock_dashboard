from forex_python.converter import CurrencyRates

import pandas as pd
import numpy as np
import yfinance as yf




def get_purchases_and_sales_log():
    compra_ventas_df = pd.read_csv("data/log_compra_venta.csv", decimal=",")
    # compra_ventas_df = pd.read_csv("data/log_compra_venta_AITA.csv", decimal=",")
    return compra_ventas_df


def get_company_info():
    company_info_df = pd.read_csv("data/info_empresas.csv", decimal=",")
    # company_info_df = pd.read_csv("data/info_empresas_AITA.csv", decimal=",")
    return company_info_df


def get_purchases_and_sales():
    purchases_and_sales_df = get_purchases_and_sales_log()
    company_info_df = get_company_info()

    purchases_and_sales_df['pk'] = purchases_and_sales_df['Mercado'].astype(str) + purchases_and_sales_df['Ticker'].astype(str)
    company_info_df = company_info_df.rename(columns={'PK': 'pk'})
    purchases_and_sales_enriched_df = purchases_and_sales_df.merge(
        company_info_df[['pk', 'Sector', 'Moneda del mercado', 'Pais']],
        how="left", on='pk')
    return purchases_and_sales_enriched_df


def get_risk_diversification_data(weight_criteria_column, risk_criteria_dict):
    def calculate_weight_by_group(df, group, weight_criteria):
        df_grouped = df.groupby(group).sum()[weight_criteria].reset_index().copy()
        df_grouped['weight'] = (df_grouped[weight_criteria] / df_grouped[weight_criteria].sum() * 100).round(2)
        # df_grouped['weight_to_display'] = df_grouped['weight'].apply(lambda value: f'{value} %')
        return df_grouped

    compra_ventas_df = get_purchases_and_sales_log()
    company_info_df = get_company_info()


    # TRANSFORMACIONES DE DATOS
    ## UNIONES DE DATOS
    compra_ventas_df['pk'] = compra_ventas_df['Mercado'].astype(str) + compra_ventas_df['Ticker'].astype(str)
    company_info_df = company_info_df.rename(columns={'PK': 'pk'})
    compra_ventas_enriched_df = compra_ventas_df.merge(company_info_df[['pk', 'Sector', 'Moneda del mercado', 'Pais']],
                                                       how="left", on='pk')

    # CALCULOS
    # df['Dinero (EUR)'] = df.loc[df['Acción'] == 'Venta', 'Dinero (EUR)'].apply(lambda value: value * -1) # Tengo que compensar de alguna forma las ventas que he hecho, pero este no funciona INVESTIGAR MÁS!!!
    weight_by_criteria_df = calculate_weight_by_group(
        compra_ventas_enriched_df,
        group=[risk_criteria_dict['data_column']],
        weight_criteria=weight_criteria_column
    )
    weight_by_criteria_df[weight_criteria_column] = weight_by_criteria_df[weight_criteria_column].round(2)
    weight_by_criteria_df = weight_by_criteria_df.sort_values(by=['weight'], ascending=False)
    return weight_by_criteria_df


def get_companies_latest_stock_price(company_df):
    def get_yahoo_finance_market(real_market_name, yahoo_finance_stock_market_dict_list):
        for yahoo_finance_stock_market_dict in yahoo_finance_stock_market_dict_list:
            if real_market_name == yahoo_finance_stock_market_dict['real_market']:
                return yahoo_finance_stock_market_dict['yahoo_finance_market']
        return ''

    def get_change_to_euros(row):
        latest_stock_price = row['latest_stock_price']
        stock_currency = row['Moneda del mercado']

        if stock_currency == 'EUR':
            latest_stock_price = currency_rates_obj.convert(stock_currency, 'EUR', latest_stock_price)
        return  latest_stock_price

    # TODO: Esta lista de diccionarios deberia de tenerlo en una variable global llamada context o algo así.
    yahoo_finance_stock_market_dict_list = [
        {'real_market': 'BME', 'yahoo_finance_market': 'MC'},
        {'real_market': 'EPA', 'yahoo_finance_market': 'PA'},
        {'real_market': 'LON', 'yahoo_finance_market': 'L'},
        {'real_market': 'HKG', 'yahoo_finance_market': 'HK'},
    ]

    # I prepare the DF to be able to search in Yahoo Finance API
    company_df['Mercado_yahoo_finance'] = company_df['Mercado'].apply(lambda value: get_yahoo_finance_market(value, yahoo_finance_stock_market_dict_list))
    company_df['Yahoo_finance_ticker'] = company_df.apply(lambda row: f"{row['Ticker']}.{row['Mercado_yahoo_finance']}" if row['Mercado'] not in ['NASDAQ', 'NYSE'] else row['Ticker'], axis=1)
    companies_to_search_list = list(company_df['Yahoo_finance_ticker'].unique())

    # Get latest stock price
    stock_price_by_company_df = yf.Tickers(companies_to_search_list).history(period="1d")['Close'].transpose()
    # Meter todos los valores en 1 sola columna llamada "latest_stock_price"
    stock_price_by_company_df['latest_stock_price'] = stock_price_by_company_df[stock_price_by_company_df.columns].stack().reset_index(level=1, drop=True)
    stock_price_by_company_df['latest_stock_price_date'] = stock_price_by_company_df.apply(lambda row: row.index[row.notna()][0] if row.notnull().any() else np.nan, axis=1)
    stock_price_by_company_df['latest_stock_price_date'] = pd.to_datetime(stock_price_by_company_df['latest_stock_price_date']).dt.strftime('%Y-%m-%d')
    stock_price_by_company_df = stock_price_by_company_df.reset_index()
    stock_price_by_company_df = stock_price_by_company_df.rename({'Ticker': 'Yahoo_finance_ticker'}, axis=1)
    company_df = company_df.merge(stock_price_by_company_df[['Yahoo_finance_ticker', 'latest_stock_price', 'latest_stock_price_date']], on=['Yahoo_finance_ticker'], how='left')

    # Adjust the london market price (it is in pennies and i want it in pounds)
    company_df['latest_stock_price'] = company_df.apply(lambda row: row['latest_stock_price']/100 if row['Mercado'] == 'LON' else row['latest_stock_price'], axis=1)

    # Change the stock price to EUR
    currency_rates_obj = CurrencyRates()
    company_df['latest_stock_price_in_euros'] = company_df.apply(lambda row: get_change_to_euros(row), axis=1)

    return company_df[['Ticker', 'Mercado', 'latest_stock_price', 'latest_stock_price_in_euros']]
