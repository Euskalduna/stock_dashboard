import pages.risk_diversification.page_components.titles as risk_diversification_titles
import pages.risk_diversification.data as risk_diversification_data
import pages.risk_diversification.page_components.selectors as risk_diversification_selectors
import pages.risk_diversification.page_components.charts_and_tables as risk_diversification_charts_and_tables
import dash_bootstrap_components as dbc


def get_body_row(purchases_and_sales_enriched_df, risk_diversification_criteria_dict_list, weight_criteria_column, page_grid_columns):
    def get_panels(purchases_and_sales_enriched_df, risk_diversification_criteria_dict_list):
        panel_list = []
        for risk_criteria_dict in risk_diversification_criteria_dict_list:
            panel_children = get_panel(
                purchases_and_sales_enriched_df,
                risk_criteria_dict,
                weight_criteria_column) # Esto va a devolver un [elemento, elemento2, elemento3]
                                        # donde cada elemento es un ROW
            panel_list.append({"panel_id": risk_criteria_dict["criteria_name"], "panel": panel_children})
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

    panel_type_id = "risk-diversification-data-panel"
    # get body_panel
    panel_list = get_panels(purchases_and_sales_enriched_df, risk_diversification_criteria_dict_list)
    # get_body_rows
    data_row_list = get_panel_rows(panel_list, page_grid_columns, panel_type_id)
    body_row = dbc.Row(dbc.Col(data_row_list))
    return body_row


def get_panel(purchases_and_sales_enriched_df, risk_criteria_dict, weight_criteria_column, filter_dict_list=[]):
    def get_panel_body_row(pie_chart, table, pie_chart_id, table_id):
        data_row = dbc.Row([
            dbc.Col([pie_chart], id=pie_chart_id, className="col-md-6"),
            dbc.Col([table], id=table_id, className="col-md-6")
        ])
        return data_row

    # Parametría
    group_by_column = risk_criteria_dict['data_column']
    risk_criteria_name = risk_criteria_dict['criteria_name']

    title = f"Diversificación por {risk_criteria_name}"
    visualization_checklist_id = {'type': 'visualization-checklist', 'index': risk_criteria_name}
    table_id = {'type': 'table-container', 'index': risk_criteria_name}
    pie_chart_id = {'type': 'pie_chart-container', 'index': risk_criteria_name}

    # get_data
    weight_by_criteria_df = risk_diversification_data.get_weight_by_criteria_for_risk(
        purchases_and_sales_enriched_df,
        weight_criteria_column,
        group_by_column,
        filter_dict_list
    )

    # Creacion de elementos
    pie_chart_html_component = risk_diversification_charts_and_tables.get_risk_diversification_pie_chart(
        risk_criteria_name,
        weight_by_criteria_df,
        weight_criteria_column,
        group_by_column
    )
    table_html_component = risk_diversification_charts_and_tables.get_risk_diversification_table(
        weight_by_criteria_df,
        group_by_column
    )

    # Montaje
    title_row = risk_diversification_titles.get_page_common_panel_title_row(title)
    selector_row = risk_diversification_selectors.get_data_panel_data_checklist(visualization_checklist_id)
    data_row = get_panel_body_row(pie_chart_html_component, table_html_component, pie_chart_id, table_id)
    return [title_row, selector_row, data_row]
