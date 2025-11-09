import pages.stock_portfolio.page_components.titles as stock_portfolio_titles
import pages.stock_portfolio.page_components.charts_and_tables as stock_portfolio_charts_and_tables
import dash_bootstrap_components as dbc


def get_body_row(stock_portfolio_df, page_grid_columns):
    def get_panels(stock_portfolio_df):
        panel_list = []
        panel_children = get_panel(stock_portfolio_df) # Esto va a devolver un [elemento, elemento2, elemento3] donde cada elemento es un ROW
        panel_list.append({"panel_id": "portfolio", "panel": panel_children})
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

    panel_type_id = "stock-portfolio-data-panel"
    # get body_panel
    panel_list = get_panels(stock_portfolio_df)
    # get_body_rows
    data_row_list = get_panel_rows(panel_list, page_grid_columns, panel_type_id)
    body_row = dbc.Row(dbc.Col(data_row_list))
    return body_row


def get_panel(stock_portfolio_df):
    def get_panel_body_row(table, table_id):
        data_row = dbc.Row([
            dbc.Col([table], id=table_id)
        ])
        return data_row

    # Parametría
    title = f""
    table_id = {'type': 'table-container', 'index': 'portfolio_table'}
    non_numeric_column_list = ['Propietario', 'Mercado', 'Ticker', 'Nombre']

    # Creacion de elementos
    table_html_component = stock_portfolio_charts_and_tables.get_stock_portfolio_table(
        stock_portfolio_df,
        non_numeric_column_list
    )

    # Montaje
    title_row = stock_portfolio_titles.get_page_common_panel_title_row(title)
    data_row = get_panel_body_row(table_html_component, table_id)
    return [title_row, data_row]



