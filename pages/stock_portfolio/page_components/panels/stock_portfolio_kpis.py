import configs.chart_configs as chart_configs
import utils.general_utils as general_utils
import utils.charts as charts_utils


def get_stock_portfolio_kpis_panel(stock_portfolio_df, obtained_dividends_df):
    # Panel parameters
    stock_portfolio_money_invested_value_id = {'type': 'stock_portfolio_kpi-container', 'index': "stock_portfolio_money_invested_value"}
    stock_portfolio_money_and_dividends_invested_value_id = {'type': 'stock_portfolio_kpi-container', 'index': "stock_portfolio_money_and_dividends_invested_value"}
    stock_portfolio_current_value_id_1 = {'type': 'stock_portfolio_kpi-container', 'index': "stock_portfolio_current_value_1"}
    stock_portfolio_current_value_id_2 = {'type': 'stock_portfolio_kpi-container', 'index': "stock_portfolio_current_value_2"}
    stock_portfolio_money_invested_vs_current_value_relative_difference_id = {'type': 'stock_portfolio_kpi-container', 'index': "stock_portfolio_money_invested_vs_current_value_relative_difference"}
    stock_portfolio_money_invested_vs_current_value_absolute_difference_id = {'type': 'stock_portfolio_kpi-container', 'index': "stock_portfolio_money_invested_vs_current_value_absolute_difference"}
    stock_portfolio_money_and_dividends_invested_vs_current_value_relative_difference_id = {'type': 'stock_portfolio_kpi-container', 'index': "stock_portfolio_money_and_dividends_invested_vs_current_value_relative_difference"}
    stock_portfolio_money_and_dividends_invested_vs_current_value_absolute_difference_id = {'type': 'stock_portfolio_kpi-container', 'index': "stock_portfolio_money_and_dividends_invested_vs_current_value_absolute_difference"}

    # Get data
    # ids
    stock_portfolio_money_invested_indicator_id = "stock_portfolio_money_invested_kpi"
    stock_portfolio_money_and_dividends_invested_indicator_id = "stock_portfolio_money_and_dividends_invested_kpi"
    stock_portfolio_current_value_indicator_id = "stock_portfolio_current_value_kpi"
    stock_portfolio_money_invested_vs_current_value_relative_difference_indicator_id = "stock_portfolio_money_invested_vs_current_value_relative_difference_kpi"
    stock_portfolio_money_invested_vs_current_value_absolute_difference_indicator_id = "stock_portfolio_money_invested_vs_current_value_absolute_difference_kpi"
    stock_portfolio_money_and_dividends_invested_vs_current_value_relative_difference_indicator_id = "stock_portfolio_money_and_dividends_invested_vs_current_value_relative_difference_kpi"
    stock_portfolio_money_and_dividends_invested_vs_current_value_absolute_difference_indicator_id = "stock_portfolio_money_and_dividends_invested_vs_current_value_absolute_difference_kpi"

    # Titles
    stock_portfolio_money_invested_text_dict = {"text": "Dinero Invertido (EUR)"}
    stock_portfolio_money_and_dividends_invested_text_dict = {"text": "Dinero Invertido + Dividendos (EUR)"}
    stock_portfolio_current_value_text_dict = {"text": "Valor Actual de la Cartera (EUR)"}
    stock_portfolio_money_invested_vs_current_value_relative_difference_text_dict = {"text": "Variación (%)"}
    stock_portfolio_money_invested_vs_current_value_absolute_difference_text_dict = {"text": "Variación (EUR)"}
    stock_portfolio_money_and_dividends_invested_vs_current_value_relative_difference_text_dict = {"text": "Variación (%)"}
    stock_portfolio_money_and_dividends_invested_vs_current_value_absolute_difference_text_dict = {"text": "Variación (EUR)"}

    # Values
    total_net_obtained_dividends = obtained_dividends_df["net_obtained_money_in_euros"].sum()
    money_and_dividends_invested = stock_portfolio_df["payed_money_in_euros"].sum() + stock_portfolio_df["payed_fee_in_euros"].sum()
    money_invested = money_and_dividends_invested - total_net_obtained_dividends
    stock_portfolio_current_value_in_euros = stock_portfolio_df["company_value_in_euros"].sum()

    stock_portfolio_money_invested_vs_current_value_absolute_difference = stock_portfolio_current_value_in_euros - money_invested
    stock_portfolio_money_and_dividends_invested_vs_current_value_absolute_difference = stock_portfolio_current_value_in_euros - money_and_dividends_invested
    stock_portfolio_money_invested_vs_current_value_relative_difference = round(stock_portfolio_money_invested_vs_current_value_absolute_difference / money_invested * 100 if money_invested != 0 else 0, 2)
    stock_portfolio_money_and_dividends_invested_vs_current_value_relative_difference = round(stock_portfolio_money_and_dividends_invested_vs_current_value_absolute_difference / money_and_dividends_invested * 100 if money_and_dividends_invested != 0 else 0, 2)

    # Get the elements configuration and other attributes
    kpi_chart_config = chart_configs.get_kpi_indicator_config()

    money_invested_html_component = charts_utils.get_kpi_indicator(
        kpi_id=stock_portfolio_money_invested_indicator_id,
        text_dict=stock_portfolio_money_invested_text_dict,
        value=money_invested,
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        # paper_bg_color="#f8f9fa"
    )

    money_and_dividends_invested_html_component = charts_utils.get_kpi_indicator(
        kpi_id=stock_portfolio_money_and_dividends_invested_indicator_id,
        text_dict=stock_portfolio_money_and_dividends_invested_text_dict,
        value=money_and_dividends_invested,
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        # paper_bg_color="#f8f9fa"
    )

    stock_portfolio_current_value_html_component = charts_utils.get_kpi_indicator(
        kpi_id=stock_portfolio_current_value_indicator_id,
        text_dict=stock_portfolio_current_value_text_dict,
        value=stock_portfolio_current_value_in_euros,
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        # paper_bg_color="#f8f9fa"
    )

    stock_portfolio_money_invested_vs_current_value_relative_difference_html_component = charts_utils.get_kpi_indicator(
        kpi_id=stock_portfolio_money_invested_vs_current_value_relative_difference_indicator_id,
        text_dict=stock_portfolio_money_invested_vs_current_value_relative_difference_text_dict,
        value=stock_portfolio_money_invested_vs_current_value_relative_difference,
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        number_value_format={
            "valueformat": ",.2f",
            "font_color": "green" if stock_portfolio_money_invested_vs_current_value_relative_difference >= 0 else "red",
            "font_size": 65
        }
        # paper_bg_color="#f8f9fa"
    )

    stock_portfolio_money_invested_vs_current_value_absolute_difference_html_component = charts_utils.get_kpi_indicator(
        kpi_id=stock_portfolio_money_invested_vs_current_value_absolute_difference_indicator_id,
        text_dict=stock_portfolio_money_invested_vs_current_value_absolute_difference_text_dict,
        value=stock_portfolio_money_invested_vs_current_value_absolute_difference,
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        number_value_format={
            "valueformat": ",.0f",
            "font_color": "green" if stock_portfolio_money_invested_vs_current_value_absolute_difference >= 0 else "red",
            "font_size": 65
        }
        # paper_bg_color="#f8f9fa"
    )

    stock_portfolio_money_and_dividends_invested_vs_current_value_relative_difference_html_component = charts_utils.get_kpi_indicator(
        kpi_id=stock_portfolio_money_and_dividends_invested_vs_current_value_relative_difference_indicator_id,
        text_dict=stock_portfolio_money_and_dividends_invested_vs_current_value_relative_difference_text_dict,
        value=stock_portfolio_money_and_dividends_invested_vs_current_value_relative_difference,
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        number_value_format={
            "valueformat": ",.2f",
            "font_color": "green" if stock_portfolio_money_invested_vs_current_value_relative_difference >=0 else "red",
            "font_size": 65
        }
        # paper_bg_color="#f8f9fa"
    )

    stock_portfolio_money_invested_and_dividends_vs_current_value_absolute_difference_html_component = charts_utils.get_kpi_indicator(
        kpi_id=stock_portfolio_money_and_dividends_invested_vs_current_value_absolute_difference_indicator_id,
        text_dict=stock_portfolio_money_and_dividends_invested_vs_current_value_absolute_difference_text_dict,
        value=stock_portfolio_money_and_dividends_invested_vs_current_value_absolute_difference,
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        number_value_format={
            "valueformat": ",.0f",
            "font_color": "green" if stock_portfolio_money_and_dividends_invested_vs_current_value_absolute_difference >= 0 else "red",
            "font_size": 65
        }
        # paper_bg_color="#f8f9fa"
    )

    # Assembly of the panel elements
    row_element_dict_list_1 = [
        {"id": stock_portfolio_money_invested_value_id, "html_component": money_invested_html_component},
        {"id": stock_portfolio_current_value_id_1, "html_component": stock_portfolio_current_value_html_component},
        {"id": stock_portfolio_money_invested_vs_current_value_relative_difference_id, "html_component": stock_portfolio_money_invested_vs_current_value_relative_difference_html_component},
        {"id": stock_portfolio_money_invested_vs_current_value_absolute_difference_id, "html_component": stock_portfolio_money_invested_vs_current_value_absolute_difference_html_component},
    ]

    row_element_dict_list_2 = [
        {"id": stock_portfolio_money_and_dividends_invested_value_id, "html_component": money_and_dividends_invested_html_component},
        {"id": stock_portfolio_current_value_id_2, "html_component": stock_portfolio_current_value_html_component},
        {"id": stock_portfolio_money_and_dividends_invested_vs_current_value_relative_difference_id, "html_component": stock_portfolio_money_and_dividends_invested_vs_current_value_relative_difference_html_component},
        {"id": stock_portfolio_money_and_dividends_invested_vs_current_value_absolute_difference_id, "html_component": stock_portfolio_money_invested_and_dividends_vs_current_value_absolute_difference_html_component},
    ]

    # title_row = obtained_dividends_titles.get_page_common_panel_title_row(title)
    data_row_1 = general_utils.get_panel_row(row_element_dict_list_1)
    data_row_2 = general_utils.get_panel_row(row_element_dict_list_2)

    # return [title_row, data_row_1, data_row_2]
    return [data_row_1, data_row_2]
