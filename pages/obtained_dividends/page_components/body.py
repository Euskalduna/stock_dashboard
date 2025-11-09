import datetime
import time # Import the time module

import pages.obtained_dividends.page_components.charts_and_tables as obtained_dividends_charts_and_tables
import pages.obtained_dividends.page_components.titles as obtained_dividends_titles
import pages.obtained_dividends.data as obtained_dividends_data
import utils.data_utils as data_utils
import dash_bootstrap_components as dbc
import dash_pivottable


def get_body_row(obtained_dividends_df, page_grid_columns):
    def get_panels(obtained_dividends_df):
        panel_list = []

        # KPIs
        total_brute_obtained_dividends_panel_children = get_kpi_indicators_panel(
            obtained_dividends_df
        )

        # Panel del PIE CHART
        weight_criteria_column = "Dinero BRUTO (EUR)" # TODO: --> Esto tendría que cogerlo de algún lado (vendría del callback del selector) ????
        dividends_by_company_panel_children = get_dividends_by_company_panel(obtained_dividends_df, weight_criteria_column)

        # Panel del BAR CHART
        data_column = "Dinero BRUTO (EUR)"
        first_group_by_colum = "Año Cobro"
        second_group_by_column = None
        # data_column = "Dinero BRUTO Cobrado"
        # second_group_by_column = "Moneda de lo cobrado"
        dividend_evolution_panel_children = get_dividend_evolution_panel(
            obtained_dividends_df,
            data_column,
            first_group_by_colum,
            second_group_by_column
        )

        # Panel de la TABLA


        # Panel de la TABLA PIVOTE
        dividend_pivot_table_panel_children = get_dividend_pivot_table(obtained_dividends_df)

        panel_list.append({"panel_id": "total_brute_obtained_dividends_panel", "panel": total_brute_obtained_dividends_panel_children})
        panel_list.append({"panel_id": "dividend_weight_by_company_panel", "panel": dividends_by_company_panel_children})
        panel_list.append({"panel_id": "dividend_evolution_panel", "panel": dividend_evolution_panel_children})
        panel_list.append({"panel_id": "dividend_pivot_table_panel", "panel": dividend_pivot_table_panel_children})
        return panel_list

    def get_panel_rows(panel_list, page_grid_columns, panel_type_id):
        data_row_list = []
        column_by_row_list = []

        for index, panel_dict in enumerate(panel_list):
            is_last_risk_criteria = ((index + 1) == len(panel_list))
            is_new_row_required = ((index + 1) % page_grid_columns == 0) or is_last_risk_criteria

            col_id = {"type": panel_type_id, "index": panel_dict["panel_id"]}
            column_by_row_list.append(dbc.Col(panel_dict["panel"], id=col_id, className="data-div"))

            if is_new_row_required:
                data_row_list.append(dbc.Row(column_by_row_list))
                column_by_row_list = []
        return data_row_list

    panel_type_id = "obtained-dividends-data-panel"
    # get body_panel
    panel_list = get_panels(obtained_dividends_df) #---> #TODO: Tengo que crear N paneles. como lo hago para que sea dinamico????
                                                        #TODO: primero voy a crearlos a manija, si veo patrón común ya lo generalizo
    # get_body_rows
    data_row_list = get_panel_rows(panel_list, page_grid_columns, panel_type_id)
    body_row = dbc.Row(dbc.Col(data_row_list))
    return body_row


def get_dividends_by_company_panel(obtained_dividends_df, weight_criteria_column, filter_dict_list=[]):
    def get_panel_body_row(pie_chart, table, pie_chart_id, table_id):
        data_row = dbc.Row([
            dbc.Col([pie_chart], id=pie_chart_id, className="col-md-6"),
            dbc.Col([table], id=table_id, className="col-md-6")
        ])
        return data_row

    # Parametría
    group_by_column = "Nombre Empresa" # por empresa

    title = f"Dividendos cobrados por empresa (en EUROS)"
    table_id = {'type': 'table-container', 'index': "dividendos_cobrado_por_empresa"}
    pie_chart_id = {'type': 'pie_chart-container', 'index': "dividendos_cobrado_por_empresa"}

    # get_data
    weight_by_criteria_df = obtained_dividends_data.get_weight_by_criteria(
        obtained_dividends_df,
        weight_criteria_column,
        group_by_column,
        filter_dict_list
    )

    # Creacion de elementos
    pie_chart_html_component = obtained_dividends_charts_and_tables.get_dividends_pie_chart(
        weight_by_criteria_df,
        weight_criteria_column,
        group_by_column
    )

    table_html_component = obtained_dividends_charts_and_tables.get_dividends_table(
        weight_by_criteria_df,
        group_by_column,
        table_id="dividends_weight_by_company_table"
    )

    # Montaje
    title_row = obtained_dividends_titles.get_page_common_panel_title_row(title)
    data_row = get_panel_body_row(pie_chart_html_component, table_html_component, pie_chart_id, table_id)

    return [title_row, data_row]


def get_dividend_evolution_panel(obtained_dividends_df, data_column, first_group_by_column, second_group_by_column, filter_dict_list=[]):
    def get_panel_body_row(bar_chart, bar_chart_id):
        data_row = dbc.Row([
            dbc.Col([bar_chart], id=bar_chart_id, className="col-md-12"),
        ])
        return data_row

    # Parametría
    title = f"Evolución de los Dividendos cobrados"
    # table_id = {'type': 'table-container', 'index': "dividendos_cobrado_por_empresa"}
    bar_chart_id = {'type': 'bar_chart-container', 'index': "evolucion_dividendos_cobrados"}

    if second_group_by_column:
        group_by_column_list = [first_group_by_column, second_group_by_column]
    else:
        group_by_column_list = [first_group_by_column]

    # get_data ----> tengo que obtener un DF que tenga sumados por año los dividendos en EUROS
    dividends_by_year_df = obtained_dividends_data.get_dividends_by_year(
        obtained_dividends_df,
        data_column,
        group_by_column_list,
        filter_dict_list
    )

    # Creacion de elementos
    bar_chart_html_component = obtained_dividends_charts_and_tables.get_dividend_evolution_bar_chart(
        dividends_by_year_df,
        data_column,
        group_by_column_list
    )

    # Montaje
    title_row = obtained_dividends_titles.get_page_common_panel_title_row(title)
    data_row = get_panel_body_row(bar_chart_html_component, bar_chart_id)

    return [title_row, data_row]


def get_dividend_pivot_table(obtained_dividends_df, filter_dict_list=[]):
    def get_panel_body_row(pivot_table, table_id):
        data_row = dbc.Row([
            dbc.Col([pivot_table], id=table_id, className="col-md-12")
        ])
        return data_row

    title = f"Tabla Pivote de Dividendos"
    # NO puedo quitar lo del tiempo, es para generar de manera dinámica un ID y que pueda actualizar la tabla
    # cuando se filtren los datos
    table_id = f"tabla_pivote_dividendos-{int(time.time() * 1000)}"

    modified_obtained_dividends_df = obtained_dividends_data.get_dividend_data_for_pivot_table(
        obtained_dividends_df, filter_dict_list
    )

    pivot_table_component = dash_pivottable.PivotTable(
        id=table_id,
        data=modified_obtained_dividends_df.to_dict('records'),

        # Initial hierarchical row and column configuration
        rows=['Año Cobro', 'Mes Cobro'],
        cols=['stock_market_country', 'Mercado'],

        # The value to be aggregated
        vals=['Dinero BRUTO (EUR)'],
        aggregatorName='Sum',

        # Initial rendering mode
        rendererName='Table'
    )

    # Montaje
    title_row = obtained_dividends_titles.get_page_common_panel_title_row(title)
    data_row = get_panel_body_row(pivot_table_component, table_id)

    return [title_row, data_row]


def get_kpi_indicators_panel(obtained_dividends_df, filter_dict_list=[]):
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

    filtered_obtained_dividends_df = obtained_dividends_data.get_obtained_dividends_filtered_by_dropdowns(
        obtained_dividends_df,
        filter_dict_list
    )

    total_brute_obtained_dividends = filtered_obtained_dividends_df["Dinero BRUTO (EUR)"].sum()
    total_net_obtained_dividends = filtered_obtained_dividends_df["Dinero NETO Cobrado (EUR)"].sum()
    total_invested = 100000
    purchases_and_sales_enriched_df = data_utils.get_purchases_and_sales_enriched()
    total_invested = purchases_and_sales_enriched_df["Dinero (EUR)"].sum() + purchases_and_sales_enriched_df["Dinero pagado en comisión (EUR)"].sum()

    total_real_invested = total_invested - total_net_obtained_dividends

    # Creacion de KPIs
    total_brute_dividends_html_component = obtained_dividends_charts_and_tables.get_kpi_indicator(
        id=total_brute_obtained_dividends_indicator_id,
        text_dict=total_brute_dividends_text_dict,
        value=total_brute_obtained_dividends,
        mode="number",
        domain_dict={'x': [0, 1], 'y': [0, 1]},
        height=150,
        margin_dict={"t": 40, "b": 10, "l": 10, "r": 10},
        paper_bgcolor="#f8f9fa"
    )

    total_net_dividends_html_component = obtained_dividends_charts_and_tables.get_kpi_indicator(
        id=total_net_obtained_dividends_indicator_id,
        text_dict=total_net_dividends_text_dict,
        value=total_net_obtained_dividends,
        mode="number",
        domain_dict={'x': [0, 1], 'y': [0, 1]},
        height=150,
        margin_dict={"t": 40, "b": 10, "l": 10, "r": 10},
        paper_bgcolor="#f8f9fa"
    )
    total_real_invested_html_component = obtained_dividends_charts_and_tables.get_kpi_indicator(
        id=total_real_invested_indicator_id,
        text_dict=total_real_invested_text_dict,
        value=total_real_invested,
        mode="number",
        domain_dict={'x': [0, 1], 'y': [0, 1]},
        height=150,
        margin_dict={"t": 40, "b": 10, "l": 10, "r": 10},
        paper_bgcolor="#f8f9fa"
    )
    total_brute_dividends_and_real_invested_ratio_html_component = obtained_dividends_charts_and_tables.get_kpi_indicator(
        id=total_brute_dividends_and_invested_ratio_indicator_id,
        text_dict=total_brute_dividends_and_real_invested_ratio_text_dict,
        value=round((total_brute_obtained_dividends / total_real_invested)*100, 2),
        mode="number",
        domain_dict={'x': [0, 1], 'y': [0, 1]},
        height=150,
        margin_dict={"t": 40, "b": 10, "l": 10, "r": 10},
        paper_bgcolor="#f8f9fa"
    )
    total_net_dividends_and_real_invested_ratio_html_component = obtained_dividends_charts_and_tables.get_kpi_indicator(
        id=total_net_dividends_and_invested_ratio_indicator_id,
        text_dict=total_net_dividends_and_real_invested_ratio_text_dict,
        value=round((total_net_obtained_dividends / total_real_invested)*100,2),
        mode="number",
        domain_dict={'x': [0, 1], 'y': [0, 1]},
        height=150,
        margin_dict={"t": 40, "b": 10, "l": 10, "r": 10},
        paper_bgcolor="#f8f9fa"
    )

    total_brute_obtained_dividends_col_indicator_id = {'type': 'kpi_indicator-container', 'index': "total_brute_obtained_dividends_kpi_indicator"}
    total_real_invested_col_indicator_id_1 = {'type': 'kpi_indicator-container', 'index': "total_real_invested_kpi_indicator_1"}
    total_brute_dividends_and_invested_ratio_col_indicator_id = {'type': 'kpi_indicator-container', 'index': "total_brute_obtained_dividends_and_total_real_invested_ratio_kpi_indicator"}
    total_net_dividends_col_indicator_id = {'type': 'kpi_indicator-container', 'index': "total_net_obtained_dividends_kpi_indicator"}
    total_real_invested_col_indicator_id_2 = {'type': 'kpi_indicator-container', 'index': "total_real_invested_kpi_indicator_2"}
    total_net_dividends_and_invested_ratio_col_indicator_id = {'type': 'kpi_indicator-container', 'index': "total_net_obtained_dividends_and_total_real_invested_ratio_kpi_indicator"}

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

    # Montaje
    data_row_1 = get_panel_body_row(row_element_dict_list_1)
    data_row_2 = get_panel_body_row(row_element_dict_list_2)

    return [data_row_1, data_row_2]


def get_panel_body_row(row_element_dict_list):
    column_list = []
    column_size = int(12 / len(row_element_dict_list))

    for row_element_dict in row_element_dict_list:
        html_element_id = row_element_dict["id"]
        html_element_component = row_element_dict["html_component"]

        column_list.append(dbc.Col([html_element_component], id=html_element_id, className=f"col-md-{column_size}"))

    data_row = dbc.Row(column_list)
    return data_row

