from dash.dash_table.Format import Format, Scheme, Group


def get_table_config():
    font_family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"'
    style_header = {
        'backgroundColor': '#000000',  # A bootstrap primary blue
        'fontWeight': 'bold',
        'color': 'white',  # White text on black background
        'fontFamily': font_family,
        'fontSize': '18px',
    }

    style_data = {
        'border': '1px solid #dee2e6',  # Add subtle borders
        'fontFamily': font_family
    }

    style_data_conditional = [
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(240, 240, 240)',  # Zebra striping
        }
    ]

    style_table = {'borderRadius': '10px', 'overflow': 'auto'}

    table_config_dict = {
        'style_header': style_header,
        'style_data': style_data,
        'style_data_conditional': style_data_conditional,
        'style_table': style_table
    }

    return table_config_dict


def get_column_config(total_column_list, non_value_column_list):
    """
    Generate a list of column configuration dictionaries for the NUMERIC COLUMNS

    :param total_column_list: the total list of columns
    :param non_value_column_list: the subset of columns (from the total list of columns) that are NON numeric
    (I use this column because it is easier to define the non-numeric columns than the numeric ones)
    :return:
    """

    table_column_dict_list = []
    for column in total_column_list:
        column_type = 'text' if column in non_value_column_list else 'numeric'
        format_weight = Format(
            decimal_delimiter=',',
            group_delimiter='.',
            group=Group.yes,
            groups=[3],
            precision=2,
            scheme=Scheme.fixed
        )
        column_format = format_weight if column_type == 'numeric' else None
        table_column_dict_list.append({
            'id': column,
            'name': column,
            'type': column_type,
            'format': column_format
        })

    return table_column_dict_list
