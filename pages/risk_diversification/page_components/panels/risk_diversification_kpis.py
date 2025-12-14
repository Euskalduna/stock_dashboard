import configs.chart_configs as chart_configs
import utils.general_utils as general_utils
import utils.charts as charts_utils


def get_risk_diversification_kpis_panel(purchases_and_sales_enriched_df):
    # Panel parameters
    company_count_id = {'type': 'risk_diversification_kpi-container', 'index': "company_count"}
    sector_count_id = {'type': 'risk_diversification_kpi-container', 'index': "company_count"}
    country_count_id = {'type': 'risk_diversification_kpi-container', 'index': "country_count"}
    currency_count_id = {'type': 'risk_diversification_kpi-container', 'index': "currency_count"}

    # Get data
    # ids
    company_count_indicator_id = "risk_diversification_company_count_kpi"
    sector_count_indicator_id = "risk_diversification_sector_count_kpi"
    country_count_indicator_id = "risk_diversification_country_count_kpi"
    currency_count_indicator_id = "risk_diversification_currency_count_kpi"

    # Titles
    company_count_text_dict = {"text": "Nº de Compañías"}
    sector_count_text_dict = {"text": "Nº de Sectores"}
    country_count_text_dict = {"text": "Nº de Países"}
    currency_count_text_dict = {"text": "Nº de Monedas"}

    # Values
    company_count = purchases_and_sales_enriched_df['company_name'].nunique()
    sector_count = purchases_and_sales_enriched_df['sector'].nunique()
    country_count = purchases_and_sales_enriched_df['country'].nunique()
    currency_count = purchases_and_sales_enriched_df['payment_currency'].nunique()


    # Get the elements configuration and other attributes
    kpi_chart_config = chart_configs.get_kpi_indicator_config()

    company_count_html_component = charts_utils.get_kpi_indicator(
        kpi_id=company_count_indicator_id,
        text_dict=company_count_text_dict,
        value=company_count,
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        # paper_bg_color="#f8f9fa"
    )

    sector_count_html_component = charts_utils.get_kpi_indicator(
        kpi_id=sector_count_indicator_id,
        text_dict=sector_count_text_dict,
        value=sector_count,
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        # paper_bg_color="#f8f9fa"
    )

    country_count_html_component = charts_utils.get_kpi_indicator(
        kpi_id=country_count_indicator_id,
        text_dict=country_count_text_dict,
        value=country_count,
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        # paper_bg_color="#f8f9fa"
    )

    currency_count_html_component = charts_utils.get_kpi_indicator(
        kpi_id=currency_count_indicator_id,
        text_dict=currency_count_text_dict,
        value=currency_count,
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        # paper_bg_color="#f8f9fa"
    )

    # Assembly of the panel elements
    row_element_dict_list_1 = [
        {"id": company_count_id, "html_component": company_count_html_component},
        {"id": sector_count_id, "html_component": sector_count_html_component},
        {"id": country_count_id, "html_component": country_count_html_component},
        {"id": currency_count_id, "html_component": currency_count_html_component},
    ]

    # title_row = obtained_dividends_titles.get_page_common_panel_title_row(title)
    data_row_1 = general_utils.get_panel_row(row_element_dict_list_1)

    # return [title_row, data_row_1, data_row_2]
    return [data_row_1]
