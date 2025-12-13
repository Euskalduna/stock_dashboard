from dash.dash_table import DataTable
from dash_pivottable import PivotTable


def get_table(
        table_id, data_df, column_configuration_dict_list=None, page_size=10, filter_action='none', sort_action=None,
        style_table=None, style_cell=None, style_header=None, style_data=None, style_data_conditional=None
):
    """
    It creates a Dash DataTable from a Pandas DataFrame.

    :param table_id: the id of the table HTML component
    :param data_df: the dataframe containing the data for the table
    :param column_configuration_dict_list: a list of dicts configuring the columns of the table
    :param page_size: the number of rows to display per page
    :param filter_action: the filtering action for the table. The 'none' value disables filtering. It must not be None.
    :param sort_action: the sorting action for the table
    :param style_table: the style for the table
    :param style_cell: the style for the cells of the table
    :param style_header: the style for the header of the table
    :param style_data: the style for the data of the table
    :param style_data_conditional: the conditional style for the data of the table
    :return: a Dash HTML component containing the table
    """

    table_html_component = DataTable(
        page_size=page_size,  # Number of rows per page
        id=table_id,
        columns=column_configuration_dict_list,
        data=data_df.to_dict('records'),
        style_table=style_table,
        style_cell=style_cell,
        style_header=style_header,
        style_data=style_data,
        style_data_conditional=style_data_conditional,
        filter_action=filter_action,
        sort_action=sort_action,
    )

    return table_html_component


def get_pivot_table(
        table_id, data_df, default_columns=(), default_rows=(), default_values=(), default_aggregatorName='Sum',
        default_rendererName='Table',
):
    """
    It creates a Dash PivotTable from a Pandas DataFrame.

    :param table_id: the id of the table HTML component
    :param data_df: the dataframe containing the data for the table
    :param default_columns: the columns that appear by default when loading the table
    :param default_rows: the rows that appear by default when loading the table
    :param default_values: the column that are considered as values by default when loading the table
    :param default_aggregatorName: the aggregation function used by default when loading the table
    :param default_rendererName: the default mode of rendering the table (it can be loaded as different charts too)
    :return: a Dash HTML component containing the pivot table
    """

    pivot_table_component = PivotTable(
        id=table_id,
        data=data_df.to_dict('records'),
        cols=default_columns,
        rows=default_rows,
        vals=default_values,
        aggregatorName=default_aggregatorName,
        rendererName=default_rendererName
    )

    return pivot_table_component
