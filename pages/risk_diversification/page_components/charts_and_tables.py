from dash import dcc
from dash.dash_table import DataTable
from dash.dash_table.Format import Format, Scheme, Group
import utils.table_utils as table_utils
import plotly.express as px


def get_risk_diversification_pie_chart(risk_criteria_name, weight_by_criteria_df, data_column, group_by_column):
    pie_chart_id = f"diversification_by_{risk_criteria_name}_pie_chart"

    # Creacion de pie chart
    weight_by_criteria_pie_chart = px.pie(
        weight_by_criteria_df,
        values=data_column,
        names=group_by_column,
        # template="vizro_dark"
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
                                               hoverlabel=pop_up_format_dict,
                                               paper_bgcolor='rgba(0,0,0,0)',  # Quita el background de la grafica
                                               plot_bgcolor='rgba(0,0,0,0)')
    weight_by_criteria_pie_chart_html_component = dcc.Graph(id=pie_chart_id,
                                                            figure=weight_by_criteria_pie_chart)
    return weight_by_criteria_pie_chart_html_component


def get_risk_diversification_table(weight_by_criteria_df, group_by_column):
    def get_configurated_table_columns(df, group_by_column):
        table_column_dict_list = []

        for column in df.columns:
            column_type = 'text' if column == group_by_column else 'numeric'
            format_weight = Format(decimal_delimiter=',', group_delimiter='.', group=Group.yes, groups=[3],
                                   precision=2, scheme=Scheme.fixed)
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

    style_header = table_utils.get_default_style_header()
    style_data = table_utils.get_default_style_data()
    style_data_conditional = table_utils.get_default_style_data_conditional()
    style_table = table_utils.get_default_style_table()

    weight_by_criteria_table_html_component = DataTable(data=table_data,
                                                        columns=table_columns,
                                                        page_size=15,
                                                        # filter_action="native",
                                                        sort_action="native",
                                                        id="risk-diversification-table",
                                                        style_header=style_header,
                                                        style_data=style_data,
                                                        style_data_conditional=style_data_conditional,
                                                        style_table=style_table
                                                        )
    return weight_by_criteria_table_html_component
