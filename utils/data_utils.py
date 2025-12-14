import sys

from forex_python.converter import CurrencyRates

import pandas as pd
import numpy as np
import yfinance as yf
import os


def get_data_path():
    # Determina la ruta base, funciona tanto en desarrollo como en el .exe compilado
    if getattr(sys, "frozen", False):
        # Si la aplicación está 'congelada' (es un .exe)
        data_base_path = os.path.dirname(sys.executable)
    else:
        # Si está en modo de desarrollo (ejecutando el .py)
        # data_base_path = os.path.dirname(os.path.abspath(__file__))
        data_base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_base_path = os.path.join(data_base_path, "data")
    return data_base_path


def get_purchases_and_sales_log(filter_dict_list=[]):
    data_base_path = get_data_path()
    data_path = os.path.join(data_base_path, "log_compra_venta.csv")
    compra_ventas_df = pd.read_csv(data_path, decimal=",")

    # Traduzco los nombres de las columnas para tenerlos en "programmer friendly"
    titles_data_path = os.path.join(data_base_path, "titles_log_compra_venta.csv")
    titles_compra_ventas_df = pd.read_csv(titles_data_path, decimal=",")
    compra_ventas_df = compra_ventas_df.rename(
        columns=dict(
            zip(
                titles_compra_ventas_df['Nombre Columna Excel'],
                titles_compra_ventas_df['Nombre Columna Programa']
            )
        )
    )

    # Corrijo los registros de venta, para que computen como negativas algunas columnas
    sales_condition = (compra_ventas_df["stock_type"] == "Acción") & (compra_ventas_df["action"] == "Venta")
    # TODO: esto hay que revisarlo para MÁS COLUMNAS
    sales_columns_to_alter = ["stock_quantity", "payed_money", "payed_money_in_euros"]
    compra_ventas_df.loc[sales_condition, sales_columns_to_alter] = compra_ventas_df.loc[sales_condition, sales_columns_to_alter] * -1

    filtered_compra_ventas_df = get_data_filtered_by_dropdowns(compra_ventas_df, filter_dict_list)
    filtered_compra_ventas_df = filtered_compra_ventas_df.round(2)  # makes that all numeric columns have 2 decimals
    # Drop rows where year is NaN. It will be interpreted as no dividend was paid.
    filtered_compra_ventas_df = filtered_compra_ventas_df[~filtered_compra_ventas_df['year'].isna()]
    filtered_compra_ventas_df['year'] = filtered_compra_ventas_df['year'].astype(int)
    return filtered_compra_ventas_df


def get_company_info(filter_dict_list=[]):
    data_base_path = get_data_path()
    data_path = os.path.join(data_base_path, "info_empresas.csv")
    company_info_df = pd.read_csv(data_path, decimal=",")

    # Traduzco los nombres de las columnas para tenerlos en "programmer friendly"
    titles_data_path = os.path.join(data_base_path, "titles_info_empresas.csv")
    titles_company_info_df = pd.read_csv(titles_data_path, decimal=",")
    company_info_df = company_info_df.rename(
        columns=dict(
            zip(
                titles_company_info_df['Nombre Columna Excel'],
                titles_company_info_df['Nombre Columna Programa']
            )
        )
    )
    filtered_company_info_df = get_data_filtered_by_dropdowns(company_info_df, filter_dict_list)
    return filtered_company_info_df


def get_obtained_dividends(filter_dict_list=[]):
    data_base_path = get_data_path()
    data_path = os.path.join(data_base_path, "log_dividendos.csv")
    obtained_dividends_df = pd.read_csv(data_path, decimal=",")

    # Traduzco los nombres de las columnas para tenerlos en "programmer friendly"
    titles_data_path = os.path.join(data_base_path, "titles_log_dividendos.csv")
    titles_obtained_dividends_df = pd.read_csv(titles_data_path, decimal=",")
    obtained_dividends_df = obtained_dividends_df.rename(
        columns=dict(
            zip(
                titles_obtained_dividends_df['Nombre Columna Excel'],
                titles_obtained_dividends_df['Nombre Columna Programa']
            )
        )
    )

    obtained_dividends_df["stock_market_country"] = obtained_dividends_df["market"].apply(
        lambda stock_market_id: get_country_from_stock_market(stock_market_id)
    )

    filtered_obtained_dividends_df = get_data_filtered_by_dropdowns(obtained_dividends_df, filter_dict_list)
    filtered_obtained_dividends_df = filtered_obtained_dividends_df.round(2) # makes that all numeric columns have 2 decimals
    # Drop rows where payment_year is NaN. It will be interpreted as no dividend was paid.
    filtered_obtained_dividends_df = filtered_obtained_dividends_df[~filtered_obtained_dividends_df['payment_year'].isna()]
    filtered_obtained_dividends_df['payment_year'] = filtered_obtained_dividends_df['payment_year'].astype(int)
    filtered_obtained_dividends_df['payment_month'] = filtered_obtained_dividends_df['payment_month'].astype(int)
    return filtered_obtained_dividends_df


def get_purchases_and_sales_enriched(filter_dict_list=[]):
    purchases_and_sales_df = get_purchases_and_sales_log()
    company_info_df = get_company_info()

    purchases_and_sales_df['pk'] = purchases_and_sales_df['market'].astype(str) + purchases_and_sales_df['ticker'].astype(str)
    company_info_df = company_info_df.rename(columns={'PK': 'pk'})
    purchases_and_sales_enriched_df = purchases_and_sales_df.merge(
        company_info_df[['pk', 'sector', 'market_currency', 'country', "isin", "reit", "dividend_payment_months"]],
        how="left", on='pk')

    filtered_purchases_and_sales_enriched_df = get_data_filtered_by_dropdowns(purchases_and_sales_enriched_df, filter_dict_list)

    return filtered_purchases_and_sales_enriched_df


def get_country_from_stock_market(stock_market_code):
    stock_market_to_country_dict = {
        "NASDAQ": 'USA',
        "NYSE": 'USA',
        "BME": 'España',
        "LON": 'UK',
        "EPA": 'Francia',
        "HKG": 'Hong Kong',
        "XETRA": 'Alemania',
        "JSE": 'Sudáfrica',
        "TSX": 'Canadá',
        "ASX": 'Australia'
    }

    try:
        # If it does not find the stock_market, it returns NONE
        country = stock_market_to_country_dict.get(stock_market_code.upper())
        return country
    except AttributeError:
        return None


def get_data_filtered_by_dropdowns(df, filter_dict_list):
    filtered_data_df = df
    for filter_dict in filter_dict_list:
        column_to_filter = filter_dict['column_to_filter']
        values_to_keep_list = filter_dict['values_to_keep']

        if values_to_keep_list:
            filtered_data_df = df[df[column_to_filter].isin(values_to_keep_list)]

    return filtered_data_df


def get_month_dict():
    return {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre'
    }


def get_companies_latest_stock_price(company_df):
    def get_yahoo_finance_market(real_market_name, yahoo_finance_stock_market_dict_list):
        for yahoo_finance_stock_market_dict in yahoo_finance_stock_market_dict_list:
            if real_market_name == yahoo_finance_stock_market_dict['real_market']:
                return yahoo_finance_stock_market_dict['yahoo_finance_market']
        return ''

    def get_change_to_euros(row, currency_rates_obj):
        latest_stock_price = row['latest_stock_price']
        stock_currency = row['market_currency']

        if stock_currency == 'EUR':
            latest_stock_price = currency_rates_obj.convert(stock_currency, 'EUR', latest_stock_price)
        return latest_stock_price

    # TODO: Esta lista de diccionarios deberia de tenerlo en una variable global llamada context o algo así.
    yahoo_finance_stock_market_dict_list = [
        {'real_market': 'BME', 'yahoo_finance_market': 'MC'},
        {'real_market': 'EPA', 'yahoo_finance_market': 'PA'},
        {'real_market': 'LON', 'yahoo_finance_market': 'L'},
        {'real_market': 'HKG', 'yahoo_finance_market': 'HK'},
    ]

    # I prepare the DF to be able to search in Yahoo Finance API
    company_df['yahoo_finance_market'] = company_df['market'].apply(lambda value: get_yahoo_finance_market(value, yahoo_finance_stock_market_dict_list))
    company_df['yahoo_finance_ticker'] = company_df.apply(lambda row: f"{row['ticker']}.{row['yahoo_finance_market']}" if row['market'] not in ['NASDAQ', 'NYSE'] else row['ticker'], axis=1)
    companies_to_search_list = list(company_df['yahoo_finance_ticker'].unique())

    # Get latest stock price
    stock_price_by_company_df = yf.Tickers(companies_to_search_list).history(period="1d")['Close'].transpose()
    # Meter todos los valores en 1 sola columna llamada "latest_stock_price"
    stock_price_by_company_df['latest_stock_price'] = stock_price_by_company_df[stock_price_by_company_df.columns].stack().reset_index(level=1, drop=True)
    stock_price_by_company_df['latest_stock_price_date'] = stock_price_by_company_df.apply(lambda row: row.index[row.notna()][0] if row.notnull().any() else np.nan, axis=1)
    stock_price_by_company_df['latest_stock_price_date'] = pd.to_datetime(stock_price_by_company_df['latest_stock_price_date']).dt.strftime('%Y-%m-%d')
    stock_price_by_company_df = stock_price_by_company_df.reset_index()
    stock_price_by_company_df = stock_price_by_company_df.rename({'Ticker': 'yahoo_finance_ticker'}, axis=1)
    company_df = company_df.merge(stock_price_by_company_df[['yahoo_finance_ticker', 'latest_stock_price', 'latest_stock_price_date']], on=['yahoo_finance_ticker'], how='left')

    # Adjust the london market price (it is in pennies and i want it in pounds)
    company_df['latest_stock_price'] = company_df.apply(lambda row: row['latest_stock_price']/100 if row['market'] == 'LON' else row['latest_stock_price'], axis=1)

    # Change the stock price to EUR
    currency_rates_obj = CurrencyRates()
    company_df['latest_stock_price_in_euros'] = company_df.apply(lambda row: get_change_to_euros(row, currency_rates_obj), axis=1)

    return company_df[['ticker', 'market', 'latest_stock_price', 'latest_stock_price_in_euros']]
