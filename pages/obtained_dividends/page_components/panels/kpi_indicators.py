import dash_bootstrap_components as dbc
import utils.data_utils as data_utils
import pages.obtained_dividends.data as obtained_dividends_data
import pages.obtained_dividends.page_components.titles as obtained_dividends_titles
import configs.chart_configs as chart_configs
import utils.general_utils as general_utils
import utils.charts as charts_utils


def get_kpi_indicators_panel(obtained_dividends_df):
    # Panel parameters
    # title = f"Indicadores Clave de Rendimiento (KPIs) de Dividendos Obtenidos"
    total_brute_obtained_dividends_col_indicator_id = {'type': 'kpi_indicator-container', 'index': "total_brute_obtained_dividends_kpi_indicator"}
    total_real_invested_col_indicator_id_1 = {'type': 'kpi_indicator-container', 'index': "total_real_invested_kpi_indicator_1"}
    total_brute_dividends_and_invested_ratio_col_indicator_id = {'type': 'kpi_indicator-container', 'index': "total_brute_obtained_dividends_and_total_real_invested_ratio_kpi_indicator"}
    total_net_dividends_col_indicator_id = {'type': 'kpi_indicator-container', 'index': "total_net_obtained_dividends_kpi_indicator"}
    total_real_invested_col_indicator_id_2 = {'type': 'kpi_indicator-container', 'index': "total_real_invested_kpi_indicator_2"}
    total_net_dividends_and_invested_ratio_col_indicator_id = {'type': 'kpi_indicator-container', 'index': "total_net_obtained_dividends_and_total_real_invested_ratio_kpi_indicator"}

    # Get data
    total_brute_obtained_dividends_indicator_id = "total_brute_obtained_dividends_kpi_indicator"
    total_net_obtained_dividends_indicator_id = "total_net_obtained_dividends_kpi_indicator"
    # NOTE:
    # Dinero Invertido = Dinero pagado por las acciones + Dinero pagado por las comisiones
    # Dinero Real Invertido = Dinero invertido - el dinero puesto por dividendos generados
    total_real_invested_indicator_id = "total_real_invested_kpi_indicator"
    total_brute_dividends_and_invested_ratio_indicator_id = "total_brute_obtained_dividends_and_total_real_invested_ratio_kpi_indicator"
    total_net_dividends_and_invested_ratio_indicator_id = "total_net_obtained_dividends_and_total_real_invested_ratio_kpi_indicator"

    total_brute_dividends_text_dict = {"text": "Dividendos Brutos Ganados (EUR)"}
    total_net_dividends_text_dict = {"text": "Dividendos Netos Ganados (EUR)"}
    total_real_invested_text_dict = {"text": "Total Real Invertido (EUR)"}
    total_brute_dividends_and_real_invested_ratio_text_dict = {"text": "Ratio (%)"}
    total_net_dividends_and_real_invested_ratio_text_dict = {"text": "Ratio (%)"}

    total_brute_obtained_dividends = obtained_dividends_df["brute_obtained_money_in_euros"].sum()
    total_net_obtained_dividends = obtained_dividends_df["net_obtained_money_in_euros"].sum()
    total_invested = 100000
    purchases_and_sales_enriched_df = data_utils.get_purchases_and_sales_enriched()
    total_invested = purchases_and_sales_enriched_df["payed_money_in_euros"].sum() + purchases_and_sales_enriched_df["payed_fee_in_euros"].sum()

    total_real_invested = total_invested - total_net_obtained_dividends

    # Get the elements configuration and other attributes
    kpi_chart_config = chart_configs.get_kpi_indicator_config()

    # Create the elements (KPIs)
    total_brute_dividends_html_component = charts_utils.get_kpi_indicator(
        kpi_id=total_brute_obtained_dividends_indicator_id,
        text_dict=total_brute_dividends_text_dict,
        value=total_brute_obtained_dividends,
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        # paper_bg_color="#f8f9fa"
    )

    total_net_dividends_html_component = charts_utils.get_kpi_indicator(
        kpi_id=total_net_obtained_dividends_indicator_id,
        text_dict=total_net_dividends_text_dict,
        value=total_net_obtained_dividends,
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        # paper_bg_color="#f8f9fa"
    )
    total_real_invested_html_component = charts_utils.get_kpi_indicator(
        kpi_id=total_real_invested_indicator_id,
        text_dict=total_real_invested_text_dict,
        value=total_real_invested,
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        # paper_bg_color="#f8f9fa"
    )
    total_brute_dividends_and_real_invested_ratio_html_component = charts_utils.get_kpi_indicator(
        kpi_id=total_brute_dividends_and_invested_ratio_indicator_id,
        text_dict=total_brute_dividends_and_real_invested_ratio_text_dict,
        value=round((total_brute_obtained_dividends / total_real_invested)*100, 2),
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        # paper_bg_color="#f8f9fa"
    )
    total_net_dividends_and_real_invested_ratio_html_component = charts_utils.get_kpi_indicator(
        kpi_id=total_net_dividends_and_invested_ratio_indicator_id,
        text_dict=total_net_dividends_and_real_invested_ratio_text_dict,
        value=round((total_net_obtained_dividends / total_real_invested)*100,2),
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        # paper_bg_color="#f8f9fa"
    )

    # Assembly of the panel elements
    row_element_dict_list_1 = [
        {"id": total_brute_obtained_dividends_col_indicator_id, "html_component": total_brute_dividends_html_component},
        {"id": total_real_invested_col_indicator_id_1, "html_component": total_real_invested_html_component},
        {"id": total_brute_dividends_and_invested_ratio_col_indicator_id, "html_component": total_brute_dividends_and_real_invested_ratio_html_component},
    ]

    row_element_dict_list_2 = [
        {"id": total_net_dividends_col_indicator_id, "html_component": total_net_dividends_html_component},
        {"id": total_real_invested_col_indicator_id_2, "html_component": total_real_invested_html_component},
        {"id": total_net_dividends_and_invested_ratio_col_indicator_id, "html_component": total_net_dividends_and_real_invested_ratio_html_component},
    ]

    # title_row = obtained_dividends_titles.get_page_common_panel_title_row(title)
    data_row_1 = general_utils.get_panel_row(row_element_dict_list_1)
    data_row_2 = general_utils.get_panel_row(row_element_dict_list_2)

    # return [title_row, data_row_1, data_row_2]
    return [data_row_1, data_row_2]
