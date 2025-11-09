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


def get_purchases_and_sales_log():
    data_base_path = get_data_path()
    data_path = os.path.join(data_base_path, "log_compra_venta.csv")
    compra_ventas_df = pd.read_csv(data_path, decimal=",")

    # Corrijo los registros de venta, para que computen como negativas algunas columnas
    sales_condition = (compra_ventas_df["Tipo de Valor"] == "Acción") & (compra_ventas_df["Acción"] == "Venta")
    sales_columns_to_alter = ["Acciones", "Dinero", "Dinero (EUR)"]
    compra_ventas_df.loc[sales_condition, sales_columns_to_alter] = compra_ventas_df.loc[sales_condition, sales_columns_to_alter] * -1

    return compra_ventas_df


def get_company_info():
    data_base_path = get_data_path()
    data_path = os.path.join(data_base_path, "info_empresas.csv")
    company_info_df = pd.read_csv(data_path, decimal=",")
    return company_info_df


def get_obtained_dividends():
    data_base_path = get_data_path()
    data_path = os.path.join(data_base_path, "log_dividendos.csv")
    obtained_dividends_df = pd.read_csv(data_path, decimal=",")
    obtained_dividends_df["stock_market_country"] = obtained_dividends_df["Mercado"].apply(
        lambda stock_market_id: get_country_from_stock_market(stock_market_id)
    )

    return obtained_dividends_df


def get_purchases_and_sales_enriched():
    purchases_and_sales_df = get_purchases_and_sales_log()
    company_info_df = get_company_info()

    purchases_and_sales_df['pk'] = purchases_and_sales_df['Mercado'].astype(str) + purchases_and_sales_df['Ticker'].astype(str)
    company_info_df = company_info_df.rename(columns={'PK': 'pk'})
    purchases_and_sales_enriched_df = purchases_and_sales_df.merge(
        company_info_df[['pk', 'Sector', 'Moneda del mercado', 'Pais', "ISIN", "REIT", "Meses Pago Dividendos"]],
        how="left", on='pk')
    return purchases_and_sales_enriched_df


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
        stock_currency = row['Moneda del mercado']

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
    company_df['latest_stock_price_in_euros'] = company_df.apply(lambda row: get_change_to_euros(row, currency_rates_obj), axis=1)

    return company_df[['Ticker', 'Mercado', 'latest_stock_price', 'latest_stock_price_in_euros']]
