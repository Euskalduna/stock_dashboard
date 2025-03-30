from dash import Dash, Output, Input, State, MATCH, callback_context
import pages.risk_diversification.risk_diversification_titles as risk_diversification_titles
import pages.risk_diversification.risk_diversification_selectors as risk_diversification_selectors
import pages.risk_diversification.risk_diversification_body as risk_diversification_body
import pages.risk_diversification.risk_diversification_data as risk_diversification_data

def get_risk_diversification_page_layout():
    # Fijo el numero de columnas que quiero en cada fila (lo que definira el numero de filas)
    page_grid_columns = 1  # Esto lo pongo a mano
    dummy = "dummy_change"
    default_weight_criteria_column = 'Dinero (EUR)'
    risk_diversification_criteria_dict_list = [
        # {'criteria_name': 'empresa', 'data_column': 'Ticker', 'diversification_div': ''},
        {'criteria_name': 'empresa', 'data_column': 'Nombre Empresa', 'diversification_div': ''},
        {'criteria_name': 'sector', 'data_column': 'Sector', 'diversification_div': ''},
        {'criteria_name': 'pais', 'data_column': 'Pais', 'diversification_div': ''},
        {'criteria_name': 'moneda', 'data_column': 'Moneda del mercado', 'diversification_div': ''},
    ]
    page_title = "Diversifiación de Riesgos"

    page_title_row = risk_diversification_titles.get_page_title_row(page_title)
    selector_row = risk_diversification_selectors.get_page_general_selector_row(risk_diversification_criteria_dict_list)
    # selector_row = risk_diversification_selectors.get_test_checklist() # ESTO ES UN TEST!!!
    body_row = risk_diversification_body.get_body_row(risk_diversification_criteria_dict_list, default_weight_criteria_column, page_grid_columns)
    return [page_title_row, selector_row, body_row]


def get_risk_diversification_page_callbacks(app):
    @app.callback(
        [Output({'type': 'data-panel', 'index': MATCH}, 'children')],
        [Input("owner_dropdown_selector", "value"),
         Input("weight_dropdown_selector", "value")]
    )
    def update_page_data(selected_options_owner, selected_options_weight):
        """
        Borra y vuelve a poner Generar los datos en función de los valores seleccionados en los INPUTs
        """
        def get_filter_dict_list(owner_criteria_column):
            filter_dict_list = [{'column_to_filter': 'Propietario', 'values_to_keep': [owner_criteria_column]}]
            return filter_dict_list

        def get_new_data_divs_to_draw(new_risk_diversification_div_list, risk_diversification_criteria_dict_list,
                                      owner_criteria_column, weight_criteria_column, case_to_update):
            for risk_criteria_dict in risk_diversification_criteria_dict_list:
                if case_to_update == risk_criteria_dict['criteria_name']:
                    # Get data by selected weight and criteria
                    purchases_and_sales_enriched_df = risk_diversification_data.get_purchases_and_sales()
                    # Get criteria to filter by the DF
                    filter_dict_list = get_filter_dict_list(owner_criteria_column)
                    # Get de div of each sector of the page (that is supposed to contain data)
                    panel_children = risk_diversification_body.get_panel(purchases_and_sales_enriched_df,
                                                                         risk_criteria_dict,
                                                                         weight_criteria_column,
                                                                         filter_dict_list)  # Esto va a devolver un [elemento, elemento2, elemento3]
                    new_risk_diversification_div_list.append(panel_children)
            return new_risk_diversification_div_list

        owner_criteria_column = selected_options_owner  # es el valor de una columna del DF ????
        weight_criteria_column = selected_options_weight  # es el valor de una columna del DF ????
        case_to_update = callback_context.outputs_grouping[0]['id']['index']
        # TODO: Esta variable tendria que conseguirla del context de la página de RISK DIVERSIFICATION pero no se como hacerlo, de momento, lo hardcodeo
        risk_diversification_criteria_dict_list = [
            # {'criteria_name': 'empresa', 'data_column': 'Ticker'},
            {'criteria_name': 'empresa', 'data_column': 'Nombre Empresa'},
            {'criteria_name': 'sector', 'data_column': 'Sector'},
            {'criteria_name': 'pais', 'data_column': 'Pais'},
            {'criteria_name': 'moneda', 'data_column': 'Moneda del mercado'},
        ]

        # Get the new data to draw in the browser
        new_risk_diversification_div_list = []
        new_risk_diversification_div_list = get_new_data_divs_to_draw(new_risk_diversification_div_list,
                                                                      risk_diversification_criteria_dict_list,
                                                                      owner_criteria_column,
                                                                      weight_criteria_column,
                                                                      case_to_update)
        return new_risk_diversification_div_list  # Esto tendria que ser una lista?? una lista de listas????

    # @app.callback(
    #     [Output({'type': 'data-panel', 'index': MATCH}, 'children')],
    #     [Input("weight_dropdown_selector", "value")]
    # )
    # def update_page_data_by_weight(selected_options):
    #     weight_criteria_column = selected_options  # es el nombre de una columna del DF
    #     case_to_update = callback_context.outputs_grouping[0]['id']['index']
    #
    #     #TODO: Esta variable tendria que conseguirla del context de la página de RISK DIVERSIFICATION pero no se como hacerlo, de momento, lo hardcodeo
    #     risk_diversification_criteria_dict_list = [
    #         # {'criteria_name': 'empresa', 'data_column': 'Ticker'},
    #         {'criteria_name': 'empresa', 'data_column': 'Nombre Empresa'},
    #         {'criteria_name': 'sector', 'data_column': 'Sector'},
    #         {'criteria_name': 'pais', 'data_column': 'Pais'},
    #         {'criteria_name': 'moneda', 'data_column': 'Moneda del mercado'},
    #     ]
    #
    #     new_risk_diversification_div_list = []
    #     for risk_criteria_dict in risk_diversification_criteria_dict_list:
    #         if case_to_update == risk_criteria_dict['criteria_name']:
    #             # Get data by selected weight and criteria
    #             purchases_and_sales_enriched_df = risk_diversification_data.get_purchases_and_sales()
    #             # Get de div of each sector of the page (that is supposed to contain data)
    #             panel_children = risk_diversification_body.get_panel(purchases_and_sales_enriched_df, risk_criteria_dict, weight_criteria_column)  # Esto va a devolver un [elemento, elemento2, elemento3]
    #             new_risk_diversification_div_list.append(panel_children)
    #
    #     return new_risk_diversification_div_list  # Esto tendria que ser una lista?? una lista de listas????

    @app.callback(
        [Output({'type': 'data-panel', 'index': MATCH}, 'className')],
        [Input("diversification_section_checklist", "value")],
        [State({'type': 'data-panel', 'index': MATCH}, 'className')]
    )
    def hide_or_show_data_panel(selected_options, className):
        # TODO: Aqui tengo que hacer que se pongan col-6 y col-12 porque si lo dejo como está, con una combinación concreta de cosas, provoca que se salten de linea los gráficos
        def is_invisible(className):
            if "d-none" in className:
                return True
            return False

        def should_be_invisible(triggered_option_value, selected_options):
            if triggered_option_value in selected_options:
                return False
            return True

        triggered_option_value = callback_context.outputs_grouping[0]['id']['index']
        new_className = className

        if is_invisible(className) and not should_be_invisible(triggered_option_value, selected_options):
            new_className = className.replace("d-none", "")
        if not is_invisible(className) and should_be_invisible(triggered_option_value, selected_options):
            new_className = f"{className} d-none"

        return [new_className]



    @app.callback(
        [Output({"type": "pie_chart-container", "index": MATCH}, "className"),
         Output({"type": "table-container", "index": MATCH}, "className")],
        [Input({'type': 'visualization-checklist', 'index': MATCH}, "value")],
        [State({"type": "pie_chart-container", "index": MATCH}, "className"),
         State({"type": "table-container", "index": MATCH}, "className")],
    )
    def hide_or_show_data(selected_options, pie_chart_classname, table_classname):
        def is_invisible(className):
            if "d-none" in className:
                return True
            return False

        def should_be_invisible(value, selected_options):
            if value in selected_options:
                return False
            return True

        def set_width_for_item(classname, width_class):
            if "col-md-6" in classname:
                return classname.replace("col-md-6", width_class)

            if "col-md-12" in classname:
                return classname.replace("col-md-12", width_class)

            return f"{classname} {width_class}"

        def set_chart_and_table_visibility(pie_chart_classname, table_classname):
            # Visibilizo u oculto las cosas en cada panel
            new_pie_chart_classname = pie_chart_classname
            new_table_classname = table_classname

            if is_invisible(pie_chart_classname) and not should_be_invisible('chart', selected_options):
                new_pie_chart_classname = pie_chart_classname.replace("d-none", "")

            if not is_invisible(pie_chart_classname) and should_be_invisible('chart', selected_options):
                new_pie_chart_classname = f"{pie_chart_classname} d-none"


            if is_invisible(table_classname) and not should_be_invisible('table', selected_options):
                new_table_classname = table_classname.replace("d-none", "")

            if not is_invisible(table_classname) and should_be_invisible('table', selected_options):
                new_table_classname = f"{table_classname} d-none"

            return [new_pie_chart_classname, new_table_classname]

        def set_chart_and_table_width(pie_chart_classname, table_classname):
            # Establezco el ancho de los componentes visibles
            new_pie_chart_classname = pie_chart_classname
            new_table_classname = table_classname

            if is_invisible(table_classname) and not is_invisible(pie_chart_classname):
                new_pie_chart_classname = set_width_for_item(pie_chart_classname, "col-md-12")

            if is_invisible(pie_chart_classname) and not is_invisible(table_classname):
                new_table_classname = set_width_for_item(new_table_classname, "col-md-12")

            if not is_invisible(pie_chart_classname) and not is_invisible(table_classname):
                new_pie_chart_classname = set_width_for_item(new_pie_chart_classname, "col-md-6")
                new_table_classname = set_width_for_item(new_table_classname, "col-md-6")

            return [new_pie_chart_classname, new_table_classname]

        new_pie_chart_classname, new_table_classname = set_chart_and_table_visibility(pie_chart_classname, table_classname)
        new_pie_chart_classname, new_table_classname = set_chart_and_table_width(new_pie_chart_classname, new_table_classname)

        return [new_pie_chart_classname, new_table_classname]


#TODO: debo estandarizar la nomenclatura de los IDs
