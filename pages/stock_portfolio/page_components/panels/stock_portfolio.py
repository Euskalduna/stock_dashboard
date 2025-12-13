import dash_bootstrap_components as dbc
import dash_pivottable
import pages.stock_portfolio.page_components.titles as stock_portfolio_titles
import time # Import the time module
import utils.general_utils as general_utils
import utils.tables as tables_utils
import configs.table_configs as table_configs


def get_portfolio_table(stock_portfolio_df):
    # Panel parameters
    title = f""
    table_id = {'type': 'table-container', 'index': 'portfolio_table'}
    non_numeric_column_list = ['owner', 'market', 'ticker', 'company_name']

    # Get the elements configuration and other attributes (Table)
    table_columns_dict_list = table_configs.get_column_config(stock_portfolio_df.columns, non_numeric_column_list)

    table_config = table_configs.get_table_config()
    style_header = table_config["style_header"]
    style_data = table_config["style_data"]
    style_data['whiteSpace'] = 'normal'
    style_data['height'] = 'auto'
    style_data_conditional = table_config["style_data_conditional"]
    style_table = table_config["style_table"]
    style_table['overflowX'] = 'auto'
    style_cell = {"minWidth": 150}

    # Create the elements (Table)
    table_html_component = tables_utils.get_table(
        table_id="risk-diversification-table",
        data_df=stock_portfolio_df,
        column_configuration_dict_list=table_columns_dict_list,
        page_size=15,
        # filter_action="native",
        sort_action="native",
        style_table=style_table,
        style_cell=style_cell,
        style_header=style_header,
        style_data=style_data,
        style_data_conditional=style_data_conditional
    )

    # # Creacion de elementos
    # table_html_component = stock_portfolio_charts_and_tables.get_stock_portfolio_table(
    #     stock_portfolio_df,
    #     non_numeric_column_list
    # )

    # Assembly of the panel elements
    row_element_dict_list = [
        {"id": table_id, "html_component": table_html_component}
    ]

    title_row = stock_portfolio_titles.get_page_common_panel_title_row(title)
    data_row = general_utils.get_panel_row(row_element_dict_list)

    return [title_row, data_row]


def get_portfolio_table_new(stock_portfolio_df):
    title = f"Cartera de acciones"
    table_id = f"pivot_table_stock_portfolio-{int(time.time() * 1000)}"

    # TODO: puedo añadir el peso que representa cada accion en la cartera, por empresa, por sector, por pais, etc.
    pivot_table_component = dash_pivottable.PivotTable(
        id=table_id,
        data=stock_portfolio_df.to_dict('records'),
        rows=[
            # "company_name", "ticker", "market", "stock_quantity", "payed_money_in_euros", "mean_price_in_euros", "isin",
            # "country", "sector", "reit", "dividend_payment_months"
            "company_name"
        ],
        cols=[],
        vals=["stock_quantity", "payed_money_in_euros", "mean_price_in_euros"],
        # vals=[],
        aggregatorName="Sum",
        rendererName="Table"
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
        {"id": table_id, "html_component": styled_pivot_table}
    ]

    # Montaje
    title_row = stock_portfolio_titles.get_page_common_panel_title_row(title)
    data_row = general_utils.get_panel_row(row_element_dict_list)
    return [title_row, data_row]