from dash.dash_table import DataTable
from dash.dash_table.Format import Format, Group, Scheme
import utils.table_utils as table_utils


def get_stock_portfolio_table(stock_portfolio_df, non_numeric_column_list):
    def get_configurated_table_columns(df, non_numeric_column_list):
        table_column_dict_list = []

        for column in df.columns:
            if column == "Acciones":
                format_weight = Format(decimal_delimiter=',', group_delimiter='.', group=Group.yes, groups=[3])
            else:
                format_weight = Format(decimal_delimiter=',', group_delimiter='.', group=Group.yes, groups=[3], precision=2, scheme=Scheme.fixed)

            column_type = 'text' if column == non_numeric_column_list else 'numeric'
            column_format = format_weight if column_type == 'numeric' else None

            table_column_dict_list.append({'id': column, 'name': column, 'type': column_type, 'format': column_format})

        return table_column_dict_list

    # Creacion de tabla
    ## Orden y seleccion de columnas
    # stock_portfolio_df = stock_portfolio_df[['Mercado', 'Ticker', 'Nombre Empresa', 'Acciones', 'Dinero', 'Dinero(EUR)', 'Dinero pagado en Comisión', 'Dinero pagado en comisión (EUR)', 'latest_stock_price_in_euros', 'invested_money_with_comissions', 'invested_money_with_comissions_in_euros', 'mean_price', 'mean_price_in_euros', 'mean_price_with_comissions', 'mean_price_with_comissions_in_euros', 'company_value', 'company_value_in_euros']]
    #TODO: pongo aqui el filtro de cosas a mantener como columnas de la tabla o lo pongo en el UPDATE de los datos????? ---------> Lo he puesto en el UPDATE!!!!!
    # stock_portfolio_df = stock_portfolio_df[
    #     ['Mercado', 'Nombre Empresa', 'Acciones', 'Dinero (EUR)',
    #      'Dinero pagado en comisión (EUR)', 'latest_stock_price_in_euros',
    #      'invested_money_with_comissions_in_euros', 'mean_price_in_euros',
    #      'mean_price_with_comissions_in_euros', 'company_value_in_euros']]

    # stock_portfolio_df = stock_portfolio_df[
    #     ['Mercado', 'Nombre Empresa', 'Acciones', 'Dinero',
    #      'Dinero pagado en Comisión', 'latest_stock_price',
    #      'invested_money_with_comissions', 'mean_price',
    #      'mean_price_with_comissions', 'company_value']]

    table_data = stock_portfolio_df.to_dict('records')
    # table_columns = [{"name": i, "id": i} for i in weight_by_criteria_df.columns]
    table_columns = get_configurated_table_columns(stock_portfolio_df, non_numeric_column_list)

    style_header = table_utils.get_default_style_header()
    style_data = table_utils.get_default_style_data()
    style_data['whiteSpace'] = 'normal'
    style_data['height'] = 'auto'
    style_data_conditional = table_utils.get_default_style_data_conditional()
    style_table = table_utils.get_default_style_table()
    style_table['overflowX'] = 'auto'
    style_cell = {"minWidth": 150}

    weight_by_criteria_table_html_component = DataTable(data=table_data,
                                                        columns=table_columns,
                                                        page_size=15,
                                                        # filter_action="native",
                                                        sort_action="native",
                                                        id="stock-portfolio-table",
                                                        style_header=style_header,
                                                        style_data=style_data,
                                                        style_data_conditional=style_data_conditional,
                                                        style_table=style_table,
                                                        style_cell=style_cell,
                                                        # fixed_columns={'headers': True, 'data': 1},
                                                        )
    return weight_by_criteria_table_html_component
