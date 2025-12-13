import utils.data_utils as data_utils

# Esta clase se inicializa al compilar el proyecto y no se vuelve a llamar a la clase
# La idea es que se acceda a esta variable "context" para leer cosas o para escribir cosas pequeñas
# importando "context" en aquellas otras clases que se necesite


def initialize_context():
    context = {}
    context['risk_diversification_criteria_dict_list'] = add_risk_diversification_criteria()
    context['company_stock_prices_df'] = add_company_stock_prices()
    return context


def add_risk_diversification_criteria():
    risk_diversification_criteria_dict_list = [
        {'criteria_name': 'company', 'data_column': 'company_name'},
        {'criteria_name': 'sector', 'data_column': 'sector'},
        {'criteria_name': 'country', 'data_column': 'country'},
        {'criteria_name': 'currency', 'data_column': 'market_currency'},
    ]
    return risk_diversification_criteria_dict_list


def add_company_stock_prices():
    purchases_and_sales_enriched_df = data_utils.get_purchases_and_sales_enriched()
    purchases_and_sales_enriched_df = purchases_and_sales_enriched_df[purchases_and_sales_enriched_df['ticker'].notna()]
    purchases_and_sales_enriched_df = purchases_and_sales_enriched_df[purchases_and_sales_enriched_df['stock_type'] == 'Acción']
    company_stock_prices_df = purchases_and_sales_enriched_df[['ticker', 'market', 'market_currency']].drop_duplicates()
    company_stock_prices_df = data_utils.get_companies_latest_stock_price(company_stock_prices_df)
    return company_stock_prices_df


context = initialize_context()
