from dash import html
import utils.data_utils as data_utils
import configs.chart_configs as chart_configs
import utils.general_utils as general_utils
import utils.charts as charts_utils


def get_dividends_kpis_panel(obtained_dividends_df, purchases_and_sales_enriched_df):
    # Panel parameters
    # title = f"Indicadores Clave de Rendimiento (KPIs) de Dividendos Obtenidos"
    total_gross_obtained_dividends_col_indicator_id = {'type': 'dividends_kpi-container', 'index': "total_gross_obtained_dividends_kpi"}
    total_real_invested_col_indicator_id = {'type': 'dividends_kpi-container', 'index': "total_real_invested_kpi_1"}
    total_gross_dividends_and_invested_ratio_col_indicator_id = {'type': 'dividends_kpi-container', 'index': "total_gross_obtained_dividends_and_total_real_invested_ratio_kpi"}
    total_net_dividends_col_indicator_id = {'type': 'dividends_kpi-container', 'index': "total_net_obtained_dividends_kpi"}
    total_net_dividends_and_invested_ratio_col_indicator_id = {'type': 'dividends_kpi-container', 'index': "total_net_obtained_dividends_and_total_real_invested_ratio_kpi"}
    empty_kpi_element_id = {'type': 'dividends_kpi-container', 'index': "empty_kpi_element"}

    # Get data
    total_gross_obtained_dividends_indicator_id = "total_gross_obtained_dividends_kpi"
    total_net_obtained_dividends_indicator_id = "total_net_obtained_dividends_kpi"
    # NOTE:
    # Dinero Invertido = Dinero pagado por las acciones + Dinero pagado por las comisiones
    # Dinero Real Invertido = Dinero invertido - el dinero puesto por dividendos generados
    total_real_invested_indicator_id = "total_real_invested_kpi"
    total_gross_dividends_and_invested_ratio_indicator_id = "total_gross_obtained_dividends_and_total_real_invested_ratio_kpi"
    total_net_dividends_and_invested_ratio_indicator_id = "total_net_obtained_dividends_and_total_real_invested_ratio_kpi"

    total_gross_dividends_text_dict = {"text": "Dividendos Brutos Ganados (EUR)"}
    total_net_dividends_text_dict = {"text": "Dividendos Netos Ganados (EUR)"}
    total_real_invested_text_dict = {"text": "Total Real Invertido (EUR)"}
    total_gross_dividends_and_real_invested_ratio_text_dict = {"text": "Ratio (%)"}
    total_net_dividends_and_real_invested_ratio_text_dict = {"text": "Ratio (%)"}

    total_gross_obtained_dividends = obtained_dividends_df["gross_obtained_money_in_euros"].sum()
    total_net_obtained_dividends = obtained_dividends_df["net_obtained_money_in_euros"].sum()
    total_invested = purchases_and_sales_enriched_df["payed_money_in_euros"].sum() + purchases_and_sales_enriched_df["payed_fee_in_euros"].sum()
    total_real_invested = total_invested - total_net_obtained_dividends

    # Get the elements configuration and other attributes
    kpi_chart_config = chart_configs.get_kpi_indicator_config()

    # Create the elements (KPIs)
    total_gross_dividends_html_component = charts_utils.get_kpi_indicator(
        kpi_id=total_gross_obtained_dividends_indicator_id,
        text_dict=total_gross_dividends_text_dict,
        value=total_gross_obtained_dividends,
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
    total_gross_dividends_and_real_invested_ratio_html_component = charts_utils.get_kpi_indicator(
        kpi_id=total_gross_dividends_and_invested_ratio_indicator_id,
        text_dict=total_gross_dividends_and_real_invested_ratio_text_dict,
        value=round((total_gross_obtained_dividends / total_real_invested)*100, 2),
        mode=kpi_chart_config['mode'],
        domain_dict=kpi_chart_config['domain_dict'],
        height=kpi_chart_config['height'],
        margin_dict=kpi_chart_config['margin_dict'],
        number_value_format={"valueformat": ",.2f", "font_size": 65}
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
        number_value_format={"valueformat": ",.2f", "font_size": 65}
        # paper_bg_color="#f8f9fa"
    )

    # Assembly of the panel elements
    row_element_dict_list_1 = [
        {"id": total_gross_obtained_dividends_col_indicator_id, "html_component": total_gross_dividends_html_component},
        {"id": total_real_invested_col_indicator_id, "html_component": total_real_invested_html_component},
        {"id": total_gross_dividends_and_invested_ratio_col_indicator_id, "html_component": total_gross_dividends_and_real_invested_ratio_html_component},
    ]

    row_element_dict_list_2 = [
        {"id": total_net_dividends_col_indicator_id, "html_component": total_net_dividends_html_component},
        {"id": empty_kpi_element_id, "html_component": html.Div()},  # Empty element for spacing
        {"id": total_net_dividends_and_invested_ratio_col_indicator_id, "html_component": total_net_dividends_and_real_invested_ratio_html_component},
    ]

    # title_row = obtained_dividends_titles.get_page_common_panel_title_row(title)
    data_row_1 = general_utils.get_panel_row(row_element_dict_list_1)
    data_row_2 = general_utils.get_panel_row(row_element_dict_list_2)

    # return [title_row, data_row_1, data_row_2]
    return [data_row_1, data_row_2]
