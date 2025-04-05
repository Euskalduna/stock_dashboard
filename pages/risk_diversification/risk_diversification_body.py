from dash import dcc
from dash.dash_table import DataTable
from dash.dash_table.Format import Format, Group
import locale

import pages.risk_diversification.risk_diversification_data as risk_diversification_data
import pages.risk_diversification.risk_diversification_titles as risk_diversification_titles
import pages.risk_diversification.risk_diversification_selectors as risk_diversification_selectors
import plotly.express as px
import dash_bootstrap_components as dbc


def get_body_row(risk_diversification_criteria_dict_list, weight_criteria_column, page_grid_columns):
    # get the data to play with
    purchases_and_sales_enriched_df = risk_diversification_data.get_purchases_and_sales()

    # get body_panel
    #necesito luego el nombre del criterio + el layout de su panel

    for risk_diversification_criteria_dict in risk_diversification_criteria_dict_list:
        panel_children = get_panel(purchases_and_sales_enriched_df, risk_diversification_criteria_dict, weight_criteria_column)  # Esto va a devolver un [elemento, elemento2, elemento3]
                                                                                                         # donde cada elemento es un ROW
        risk_diversification_criteria_dict['diversification_panel_children'] = panel_children

    # get the body's layout / get the distribution of the panels in the body
    def get_data_rows(risk_diversification_criteria_dict_list, page_grid_columns):
        data_row_list = []
        column_by_row_list = []
        for index, risk_criteria_dict in enumerate(risk_diversification_criteria_dict_list):
            is_last_risk_criteria = ((index + 1) == len(risk_diversification_criteria_dict_list))
            is_new_row_required = ((index + 1) % page_grid_columns == 0) or is_last_risk_criteria

            col_id = f"diversification_by_{risk_criteria_dict['criteria_name']}_col"
            col_id = {'type': 'data-panel', 'index': risk_criteria_dict['criteria_name']}

            column_by_row_list.append(dbc.Col(risk_criteria_dict['diversification_panel_children'], id=col_id, className="data-div"))

            if is_new_row_required:
                data_row_list.append(dbc.Row(column_by_row_list))
                column_by_row_list = []
        return data_row_list

    data_row_list = get_data_rows(risk_diversification_criteria_dict_list, page_grid_columns)
    body_row = dbc.Row(dbc.Col(data_row_list))
    return body_row


def get_panel(purchases_and_sales_enriched_df, risk_criteria_dict, weight_criteria_column, filter_dict_list=[]):
    # Parametría
    group_by_column = risk_criteria_dict['data_column']
    risk_criteria_name = risk_criteria_dict['criteria_name']

    title = f"Diversificación por {risk_criteria_name}"
    visualization_checklist_id = {'type': 'visualization-checklist', 'index': risk_criteria_name}
    table_id = {'type': 'table-container', 'index': risk_criteria_name}
    pie_chart_id = {'type': 'pie_chart-container', 'index': risk_criteria_name}

    # get_data
    weight_by_criteria_df = risk_diversification_data.get_weight_by_criteria_for_risk(purchases_and_sales_enriched_df, weight_criteria_column, group_by_column, filter_dict_list)

    # Creacion de elementos
    pie_chart_html_component = get_risk_diversification_pie_chart(risk_criteria_name, weight_by_criteria_df, weight_criteria_column, group_by_column)
    table_html_component = get_risk_diversification_table(weight_by_criteria_df, group_by_column)

    # Montaje
    title_row = risk_diversification_titles.get_page_common_panel_title_row(title)
    selector_row = risk_diversification_selectors.get_data_panel_data_checklist(visualization_checklist_id)
    data_row = get_panel_body_row(pie_chart_html_component, table_html_component, pie_chart_id, table_id)
    return [title_row, selector_row, data_row]


def get_panel_body_row(pie_chart, table, pie_chart_id, table_id):
    data_row = dbc.Row([
        dbc.Col([pie_chart], id=pie_chart_id, className="col-md-6"),
        dbc.Col([table], id=table_id, className="col-md-6")
        # dbc.Col([pie_chart], id=pie_chart_id, className=""),
        # dbc.Col([table], id=table_id, className="")
    ])
    return data_row


## TODO: MUEVO ESTO A UN ARCHIVO DE PANEL COMPONENTS / CHARTS / TABLES??????? y ahi creo todas las graficas tablas y demás que me apetezca????
def get_risk_diversification_pie_chart(risk_criteria_name, weight_by_criteria_df, data_column, group_by_column):
    pie_chart_id = f"diversification_by_{risk_criteria_name}_pie_chart"

    # Creacion de pie chart
    weight_by_criteria_pie_chart = px.pie(
        weight_by_criteria_df,
        values=data_column,
        names=group_by_column,
        template="vizro_dark"
        # template="plotly_dark"
    )

    pop_up_text_html = "<b>%{label} (%{percent})</b>  <br> " + data_column + ": %{value:,.2f}"

    legend_format_dict = dict(
        orientation="v",  # Set orientation to vertical ('v')
        yanchor="top",    # Anchor the legend to the top
        y=1,              # Position the legend at the top (y=1)
        xanchor="left",   # Anchor the legend to the left
        x=1.02,           # Position the legend slightly to the right of the chart (x=1.02)
    )
    pop_up_format_dict = dict(
        font_size=22
    )
    weight_by_criteria_pie_chart.update_traces(hovertemplate=pop_up_text_html)
    weight_by_criteria_pie_chart.update_layout(legend=legend_format_dict,
                                               hoverlabel=pop_up_format_dict)
    weight_by_criteria_pie_chart_html_component = dcc.Graph(id=pie_chart_id,
                                                            figure=weight_by_criteria_pie_chart)
    return weight_by_criteria_pie_chart_html_component


def get_risk_diversification_table(weight_by_criteria_df, group_by_column):
    def get_configurated_table_columns(df, group_by_column):
        table_column_dict_list = []

        for column in df.columns:
            column_type = 'text' if column == group_by_column else 'numeric'
            format_weight = Format(decimal_delimiter=',', group_delimiter='.', group=Group.yes, groups=[3])
            column_format = format_weight if column_type == 'numeric' else None

            table_column_dict_list.append({'id': column, 'name': column, 'type': column_type, 'format': column_format})

        return table_column_dict_list

    # Creacion de tabla

    # weight_by_criteria_df = weight_by_criteria_df.drop(['weight'], axis=1)
    # weight_by_criteria_df = weight_by_criteria_df.rename(columns={'weight_to_display': 'Peso'})
    weight_by_criteria_df = weight_by_criteria_df.rename(columns={'weight': 'Peso (%)'})
    table_data = weight_by_criteria_df.to_dict('records')
    # table_columns = [{"name": i, "id": i} for i in weight_by_criteria_df.columns]
    table_columns = get_configurated_table_columns(weight_by_criteria_df, group_by_column)

    weight_by_criteria_table_html_component = DataTable(data=table_data,
                                                        columns=table_columns,
                                                        page_size=15,
                                                        # filter_action="native",
                                                        sort_action="native",
                                                        id="risk-diversification-table",
                                                        style_data={'whiteSpace': 'normal', 'height': 'auto'}
                                                        )
    return weight_by_criteria_table_html_component
