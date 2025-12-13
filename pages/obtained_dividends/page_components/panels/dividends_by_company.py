import dash_bootstrap_components as dbc
import pages.obtained_dividends.data as obtained_dividends_data
import pages.obtained_dividends.page_components.titles as obtained_dividends_titles
import utils.general_utils as general_utils
import utils.charts as charts_utils
import utils.tables as tables_utils
import configs.chart_configs as chart_configs
import configs.table_configs as table_configs


def get_dividends_by_company_panel(obtained_dividends_df, weight_criteria_column):
    # Panel parameters
    title = f"Dividendos cobrados por empresa (en EUROS)"
    table_id = {'type': 'table-container', 'index': "dividendos_cobrado_por_empresa"}
    pie_chart_id = {'type': 'pie_chart-container', 'index': "dividendos_cobrado_por_empresa"}

    # Get the data
    group_by_column = "company_name" # por empresa
    weight_by_criteria_df = obtained_dividends_data.get_weight_by_criteria(
        obtained_dividends_df,
        weight_criteria_column,
        group_by_column
    )

    # Get the elements configuration and other attributes (Pie Chart)
    pie_chart_obj_id = f"dividends_weight_pie_chart"
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

    # Create the elements (Table)
    # table_html_component = obtained_dividends_charts_and_tables.get_dividends_table(
    #     weight_by_criteria_df,
    #     group_by_column,
    #     table_id="dividends_weight_by_company_table"
    # )

    # Assembly of the panel elements
    row_element_dict_list = [
        {"id": pie_chart_id, "html_component": pie_chart_html_component},
        {"id": table_id, "html_component": table_html_component}
    ]

    title_row = obtained_dividends_titles.get_page_common_panel_title_row(title)
    data_row_style = {"minHeight": "400px"}
    data_row = general_utils.get_panel_row(row_element_dict_list, data_row_style=data_row_style, column_size_proportions=[7, 5])

    return [title_row, data_row]
