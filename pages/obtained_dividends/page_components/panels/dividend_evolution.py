import dash_bootstrap_components as dbc
import pages.obtained_dividends.data as obtained_dividends_data
import pages.obtained_dividends.page_components.titles as obtained_dividends_titles
import utils.general_utils as general_utils
import utils.charts as charts_utils
import configs.chart_configs as chart_configs


def get_dividend_evolution_panel(obtained_dividends_df, data_column, first_group_by_column, second_group_by_column):
    # Panel parameters
    title = f"Evolución de los Dividendos cobrados"
    bar_chart_id = {'type': 'bar_chart-container', 'index': "evolucion_dividendos_cobrados"}

    if second_group_by_column:
        group_by_column_list = [first_group_by_column, second_group_by_column]
    else:
        group_by_column_list = [first_group_by_column]

    # Get data ----> tengo que obtener un DF que tenga sumados por año los dividendos en EUROS
    dividends_by_year_df = obtained_dividends_data.get_dividends_by_year(
        obtained_dividends_df,
        data_column,
        group_by_column_list
    )

    # Get the elements configuration and other attributes
    bar_chart_obj_id = f"dividend_evolution_bar_chart"
    bar_chart_config = chart_configs.get_pie_chart_config()
    if (len(group_by_column_list) > 1) & ("Año" in group_by_column_list[0]):
        # Case to group by Year and Currency
        group_by_column = group_by_column_list[0]
        color_column = group_by_column_list[1]
    else:
        # Case to group by Year
        group_by_column = group_by_column_list[0]
        color_column = None

    # Create the elements (Bar Chart)
    bar_chart_html_component = charts_utils.get_bar_chart(
        bar_chart_id=bar_chart_obj_id,
        data_df=dividends_by_year_df,
        x_column=group_by_column,
        y_column=data_column,
        color_column=color_column,
        legend_format_dict=bar_chart_config['legend_format_dict'],
        pop_up_format_dict=bar_chart_config['pop_up_format_dict'],
    )

    # Assembly of the panel elements
    row_element_dict_list = [
        {"id": bar_chart_id, "html_component": bar_chart_html_component},
    ]
    title_row = obtained_dividends_titles.get_page_common_panel_title_row(title)
    data_row = general_utils.get_panel_row(row_element_dict_list)

    return [title_row, data_row]
