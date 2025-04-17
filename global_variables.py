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
        # {'criteria_name': 'empresa', 'data_column': 'Ticker'},
        {'criteria_name': 'empresa', 'data_column': 'Nombre Empresa'},
        {'criteria_name': 'sector', 'data_column': 'Sector'},
        {'criteria_name': 'pais', 'data_column': 'Pais'},
        {'criteria_name': 'moneda', 'data_column': 'Moneda del mercado'},
    ]
    return risk_diversification_criteria_dict_list


def add_company_stock_prices():
    purchases_and_sales_enriched_df = data_utils.get_purchases_and_sales()
    purchases_and_sales_enriched_df = purchases_and_sales_enriched_df[purchases_and_sales_enriched_df['Ticker'].notna()]
    purchases_and_sales_enriched_df = purchases_and_sales_enriched_df[purchases_and_sales_enriched_df['Tipo de Valor'] == 'Acción']
    companies_stock_prices_df = purchases_and_sales_enriched_df[['Ticker', 'Mercado', 'Moneda del mercado']].drop_duplicates()
    companies_stock_prices_df = data_utils.get_companies_latest_stock_price(companies_stock_prices_df)
    return companies_stock_prices_df


context = initialize_context()
