def get_default_style_header():
    font_family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"'
    style_header = {
        'backgroundColor': '#000000',  # A bootstrap primary blue
        'fontWeight': 'bold',
        'color': 'white',  # White text on black background
        'fontFamily': font_family,
        'fontSize': '18px',
    }
    return style_header


def get_default_style_data():
    font_family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"'

    # Style the data cells (overrides style_cell for data rows)
    style_data = {
        'border': '1px solid #dee2e6',  # Add subtle borders
        'fontFamily': font_family
    }
    return style_data


def get_default_style_data_conditional():
    # Style conditional formatting (example)
    style_data_conditional = [
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(240, 240, 240)',  # Zebra striping
        }
    ]
    return style_data_conditional


def get_default_style_table():
    # Add a border to the whole table
    style_table = {'borderRadius': '10px', 'overflow': 'hidden'}
    return style_table