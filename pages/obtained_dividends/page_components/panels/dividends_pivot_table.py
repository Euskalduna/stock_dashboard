import time # Import the time module
import dash_pivottable
import dash_bootstrap_components as dbc
import pages.obtained_dividends.data as obtained_dividends_data
import pages.obtained_dividends.page_components.titles as obtained_dividends_titles
import utils.general_utils as general_utils


def get_dividend_pivot_table(obtained_dividends_df):
    # Panel parameters
    title = f"Tabla Pivote de Dividendos"
    # NO puedo quitar lo del tiempo, es para generar de manera dinámica un ID y que pueda actualizar la tabla
    # cuando se filtren los datos
    table_id = f"pivot_table_dividends-{int(time.time() * 1000)}"

    modified_obtained_dividends_df = obtained_dividends_data.get_dividend_data_for_pivot_table(
        obtained_dividends_df
    )

    pivot_table_component = dash_pivottable.PivotTable(
        id=table_id,
        data=modified_obtained_dividends_df.to_dict('records'),

        # Initial hierarchical row and column configuration
        rows=['payment_year', 'payment_month'],
        cols=['stock_market_country', 'market'],

        # The value to be aggregated
        vals=['brute_obtained_money_in_euros'],
        aggregatorName='Sum',

        # Initial rendering mode
        rendererName='Table'
    )

    styled_pivot_table = dbc.Container(
        pivot_table_component,
        style={
            "overflowX": "auto",  # Enable horizontal scrolling
            "overflowY": "auto",  # Enable vertical scrolling
            "maxHeight": "1000px",  # Optional: Limit the height
            "maxWidth": "100%",   # Optional: Limit the width
        }
    )

    row_element_dict_list = [
        {"id": table_id, "html_component": styled_pivot_table},
    ]

    # Montaje
    title_row = obtained_dividends_titles.get_page_common_panel_title_row(title)
    # data_row = get_panel_row(pivot_table_component, table_id)
    data_row = general_utils.get_panel_row(row_element_dict_list)

    return [title_row, data_row]
