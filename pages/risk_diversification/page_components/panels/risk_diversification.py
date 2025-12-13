import dash_bootstrap_components as dbc
import pages.risk_diversification.data as risk_diversification_data
import pages.risk_diversification.page_components.titles as risk_diversification_titles
import utils.general_utils as general_utils
import utils.charts as charts_utils
import utils.tables as tables_utils
import configs.chart_configs as chart_configs
import configs.table_configs as table_configs


def get_risk_diversification(purchases_and_sales_enriched_df, risk_criteria_dict, weight_criteria_column):
    group_by_column = risk_criteria_dict['data_column']
    risk_criteria_name = risk_criteria_dict['criteria_name']

    # Panel parameters
    title = f"Diversificación por {risk_criteria_name}"
    table_id = {'type': 'table-container', 'index': risk_criteria_name}
    pie_chart_id = {'type': 'pie_chart-container', 'index': risk_criteria_name}

    # Get the data
    weight_by_criteria_df = risk_diversification_data.get_weight_by_criteria_for_risk(
        purchases_and_sales_enriched_df,
        weight_criteria_column,
        group_by_column
    )

    # Get the elements configuration and other attributes (Pie Chart)
    pie_chart_obj_id = f"diversification_by_{risk_criteria_name}_pie_chart"
    pie_chart_config = chart_configs.get_pie_chart_config()

    # Create the elements (Pie Chart)
    pie_chart_html_component = charts_utils.get_pie_chart(
        pie_chart_id=pie_chart_obj_id,
        data_df=weight_by_criteria_df,
        data_column=weight_criteria_column,
        labels_column=group_by_column,
        legend_format_dict=pie_chart_config['legend_format_dict'],
        pop_up_format_dict=pie_chart_config['pop_up_format_dict'],
        pop_up_text_html=pie_chart_config['pop_up_text_html'],
    )

    # Get the elements configuration and other attributes (Table)
    table_columns_dict_list = table_configs.get_column_config(weight_by_criteria_df.columns, group_by_column)

    table_config = table_configs.get_table_config()
    style_header = table_config["style_header"]
    style_data = table_config["style_data"]
    style_data_conditional = table_config["style_data_conditional"]
    style_table = table_config["style_table"]

    # Create the elements (Table)
    table_html_component = tables_utils.get_table(
        table_id="risk-diversification-table",
        data_df=weight_by_criteria_df,
        column_configuration_dict_list=table_columns_dict_list,
        page_size=15,
        # filter_action="native",
        sort_action="native",
        style_table=style_table,
        # style_cell=None,
        style_header=style_header,
        style_data=style_data,
        style_data_conditional=style_data_conditional
    )

    # table_html_component = risk_diversification_charts_and_tables.get_risk_diversification_table(
    #     weight_by_criteria_df,
    #     group_by_column
    # )

    # Assembly of the panel elements
    row_element_dict_list = [
        {"id": pie_chart_id, "html_component": pie_chart_html_component},
        {"id": table_id, "html_component": table_html_component},
    ]

    title_row = risk_diversification_titles.get_page_common_panel_title_row(title)
    # selector_row = risk_diversification_selectors.get_data_panel_data_checklist(visualization_checklist_id)
    # data_row = get_panel_row(pie_chart_html_component, table_html_component, pie_chart_id, table_id)
    data_row_style = {"minHeight": "300px"}
    # data_row_style = {"height": "40vh"} # La unidad VH sería la correcta a usar, PERO plotly no parece llevar bien los cambios
                                          # de tamaño y cada vez que se redimiensiona el gráfico ,los elementos se ponene de peor manera
    data_row = general_utils.get_panel_row(row_element_dict_list, data_row_style=data_row_style, column_size_proportions=[7, 5])

    # return [title_row, selector_row, data_row]
    return [title_row, data_row]
