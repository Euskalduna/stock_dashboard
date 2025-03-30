from utils.data_utils import *
from dash import html, dcc
from dash.dash_table import DataTable
from dash.dash_table.Format import Format, Group
import dash_bootstrap_components as dbc
import plotly.express as px
import copy

def get_risk_diversification_div(weight_criteria, risk_criteria_dict, weight_by_criteria_df):
    def get_diversification_panel_children(diversification_criteria, pie_chart_html_component, table_html_component):
        title = f"Diversificación por {diversification_criteria}"
        table_button_id = {'type': 'update-table-visibility-button', 'index': diversification_criteria}
        pie_chart_button_id = {'type': 'update-pie_chart-visibility-button', 'index': diversification_criteria}
        # pie_chart_id = f"weight_by_{diversification_criteria}_pie_chart"
        # table_id = f"weight_by_{diversification_criteria}_table"
        table_id = {'type': 'table-container', 'index': diversification_criteria}
        pie_chart_id = {'type': 'pie_chart-container', 'index': diversification_criteria}

        pie_title_row = dbc.Row([
            # dbc.Col([html.H2(title)], width=6),
            dbc.Col([html.H2(title)]),
            dbc.Col([
                dbc.Button('Grafico',
                           className="btn btn-secondary float-right",
                           color="danger",
                           id=pie_chart_button_id),
                dbc.Button('Tabla',
                           className="btn btn-secondary float-right",
                           color="danger",
                           id=table_button_id),
            ]),
        ])

        data_row = dbc.Row([
            dbc.Col([pie_chart_html_component], id=pie_chart_id, className="d-block col-md-6"),
            dbc.Col([table_html_component], id=table_id, className="d-block col-md-6")
        ])

        # diversification_div = dbc.Row(dbc.Col(([pie_title_row, data_row])))
        diversification_div_children = [pie_title_row, data_row]
        return diversification_div_children

    def get_table_columns(df):
        table_column_dict_list = []

        for column in df.columns:
            column_type = 'text' if column == risk_criteria_dict['data_column'] else 'numeric'
            format_weight = Format(decimal_delimiter=',', group_delimiter='.', group=Group.yes, groups=[3])
            column_format = format_weight if column_type == 'numeric' else None

            table_column_dict_list.append({'id': column, 'name': column, 'type': column_type, 'format': column_format})

        return table_column_dict_list

    pie_chart_id = f"diversification_by_{risk_criteria_dict['criteria_name']}_pie_chart"

    # Creacion de pie chart
    weight_by_criteria_pie_chart = px.pie(
        weight_by_criteria_df,
        values=weight_criteria,
        names=risk_criteria_dict['data_column'],
        template="vizro_dark"
        # template="plotly_dark"
    )
    weight_by_criteria_pie_chart.update_layout(legend={'x': 1, 'y': 0.5})

    weight_by_criteria_pie_chart_html_component = dcc.Graph(id=pie_chart_id,
                                                            figure=weight_by_criteria_pie_chart)

    # Creacion de tabla

    # weight_by_criteria_df = weight_by_criteria_df.drop(['weight'], axis=1)
    # weight_by_criteria_df = weight_by_criteria_df.rename(columns={'weight_to_display': 'Peso'})
    weight_by_criteria_df = weight_by_criteria_df.rename(columns={'weight': 'Peso (%)'})
    table_data = weight_by_criteria_df.to_dict('records')
    # table_columns = [{"name": i, "id": i} for i in weight_by_criteria_df.columns]
    table_columns = get_table_columns(weight_by_criteria_df)

    weight_by_criteria_table_html_component = DataTable(data=table_data,
                                                        columns=table_columns,
                                                        page_size=15,
                                                        # filter_action="native",
                                                        sort_action="native",
                                                        id="risk-diversification-table"
                                                        )

    # Creacion del div final
    weight_by_criteria_div_children = get_diversification_panel_children(
        diversification_criteria=risk_criteria_dict['criteria_name'],
        pie_chart_html_component=weight_by_criteria_pie_chart_html_component,
        table_html_component=weight_by_criteria_table_html_component
    )
    return weight_by_criteria_div_children


# -------------------------- MAIN -------------------------------

def get_risk_diversification_page_layout():
    def get_checklist_options(risk_diversification_criteria_dict_list):
        option_value_list = [risk_criteria_dict['criteria_name'] for risk_criteria_dict in risk_diversification_criteria_dict_list]
        option_dict_list = [{'label': option.capitalize(), "value": option} for option in option_value_list]
        return option_dict_list

    def get_selector_row(risk_diversification_criteria_dict_list):
        option_dict_list = get_checklist_options(risk_diversification_criteria_dict_list)
        selector_row = dbc.Row([
            dbc.Col([dcc.Dropdown(
                options=[
                    {'label': 'Dinero Invertido (Euros)', 'value': 'Dinero (EUR)'},
                    {'label': 'Peso de Cotizacion (Euros)', 'value': 'Dinero'}
                ],
                value='Dinero (EUR)',
                clearable=False,
                id="weight_dropdown_selector",
            )
            ], width=2),

            dbc.Col([dcc.Checklist(
                options=option_dict_list,
                inline=True,
                value=[option_dict['value'] for option_dict in option_dict_list],
                id="diversification_section_checklist",
                labelStyle={'display': 'inline-block', 'margin-right': '2%', 'padding-right': '1%'})
            ], width=3)
        ], className="selector-div")
        return selector_row

    def get_data_div(weight_criteria_column, risk_criteria_dict):
        # Get data by selected weight and criteria
        weight_by_criteria_df = get_risk_diversification_data(weight_criteria_column, risk_criteria_dict)
        # Get de div of each sector of the page (that is supposed to contain data)
        weight_by_criteria_div_children = get_risk_diversification_div(weight_criteria_column, risk_criteria_dict, weight_by_criteria_df)
        return weight_by_criteria_div_children

    def update_diversification_div_for_each_risk(weight_criteria_column, risk_diversification_criteria_dict_list):
        new_risk_diversification_criteria_dict_list = copy.deepcopy(risk_diversification_criteria_dict_list)
        for risk_criteria_dict in new_risk_diversification_criteria_dict_list:
            risk_criteria_dict['diversification_div'] = get_data_div(weight_criteria_column, risk_criteria_dict)
        return new_risk_diversification_criteria_dict_list

    def get_data_rows(risk_diversification_criteria_dict_list):
        data_row_list = []
        column_by_row_list = []
        for index, risk_criteria_dict in enumerate(risk_diversification_criteria_dict_list):
            is_last_risk_criteria = ((index + 1) == len(risk_diversification_criteria_dict_list))
            is_new_row_required = ((index + 1) % page_grid_columns == 0) or is_last_risk_criteria

            col_id = f"diversification_by_{risk_criteria_dict['criteria_name']}_col"
            col_id = {'type': 'data-panel', 'index': risk_criteria_dict['criteria_name']}

            column_by_row_list.append(dbc.Col(risk_criteria_dict['diversification_div'], id=col_id, className="data-div"))

            if is_new_row_required:
                data_row_list.append(dbc.Row(column_by_row_list))
                column_by_row_list = []
        return data_row_list

    # Fijo el numero de columnas que quiero en cada fila (lo que definira el numero de filas)
    page_grid_columns = 2  # Esto lo pongo a mano
    default_weight_criteria_column = 'Dinero (EUR)'
    risk_diversification_criteria_dict_list = [
        {'criteria_name': 'empresa', 'data_column': 'Ticker', 'diversification_div': ''},
        {'criteria_name': 'sector', 'data_column': 'Sector', 'diversification_div': ''},
        {'criteria_name': 'pais', 'data_column': 'Pais', 'diversification_div': ''},
        {'criteria_name': 'moneda', 'data_column': 'Moneda del mercado', 'diversification_div': ''},
    ]

    page_title_row = dbc.Row(dbc.Col(html.H1('Diversifiación de Riesgos')))
    selector_row = get_selector_row(risk_diversification_criteria_dict_list)
    risk_diversification_criteria_dict_list = update_diversification_div_for_each_risk(default_weight_criteria_column,
                                                                                       risk_diversification_criteria_dict_list)
    data_row_list = get_data_rows(risk_diversification_criteria_dict_list)
    content_row = dbc.Row(dbc.Col(data_row_list))

    return [page_title_row, selector_row, content_row]



# app = Dash(__name__, use_pages=True)




@app.callback(
    [
        Output({'type': 'data-panel', 'index': MATCH}, 'children'),
        #Output({'type': 'table-container', 'index': MATCH}, 'children'),
    ],
    [
        Input("weight_dropdown_selector", "value")
    ]
)
def update_page_data(selected_options):
    weight_criteria_column = selected_options  # es el nombre de una columna del DF
    case_to_update = callback_context.outputs_grouping[0]['id']['index']

    # Esta variable tendria que conseguirla del context de la página de RISK DIVERSIFICATION pero no se como hacerlo, de momento, lo hardcodeo
    risk_diversification_criteria_dict_list = [
        {'criteria_name': 'empresa', 'data_column': 'Ticker'},
        {'criteria_name': 'sector', 'data_column': 'Sector'},
        {'criteria_name': 'pais', 'data_column': 'Pais'},
        {'criteria_name': 'moneda', 'data_column': 'Moneda del mercado'},
    ]

    new_risk_diversification_div_list = []
    for risk_criteria_dict in risk_diversification_criteria_dict_list:
        if case_to_update == risk_criteria_dict['criteria_name']:
            # Get data by selected weight and criteria
            weight_by_criteria_df = data_utils.get_risk_diversification_data(weight_criteria_column, risk_criteria_dict)
            # Get de div of each sector of the page (that is supposed to contain data)
            weight_by_criteria_div_children = data_utils.get_risk_diversification_div(weight_criteria_column, risk_criteria_dict, weight_by_criteria_df)
            new_risk_diversification_div_list.append(weight_by_criteria_div_children)

    return new_risk_diversification_div_list  # Esto tendria que ser una lista?? una lista de listas????


@app.callback(
    [
        Output("diversification_by_company_col", "className"),
        Output("diversification_by_sector_col", "className"),
        Output("diversification_by_country_col", "className"),
        Output("diversification_by_currency_col", "className"),
    ],
    [Input("diversification_section_checklist", "value")]
)
def update_data_section_display(selected_options):
    print("DENTRO")
    # Según si su opcion está marcada o no, muestro u oculto un panel
    diversification_by_company_div_class = 'col-md-6' if 'Empresa' in selected_options else 'd-none'
    diversification_by_sector_div_class = 'col-md-6' if 'Sector' in selected_options else 'd-none'
    diversification_by_country_div_class = 'col-md-6' if 'País' in selected_options else 'd-none'
    diversification_by_currency_div_class = 'col-md-6' if 'Moneda' in selected_options else 'd-none'

    if 'Compañía' in selected_options and 'Sector' not in selected_options:
        diversification_by_company_div_class = 'col-md-12'
    if 'Sector' in selected_options and 'Empresa' not in selected_options:
        diversification_by_sector_div_class = 'col-md-12'
    if 'País' in selected_options and 'Moneda' not in selected_options:
        diversification_by_country_div_class = 'col-md-12'
    if 'Moneda' in selected_options and 'País' not in selected_options:
        diversification_by_currency_div_class = 'col-md-12'

    return (diversification_by_company_div_class, diversification_by_sector_div_class,
            diversification_by_country_div_class, diversification_by_currency_div_class)
