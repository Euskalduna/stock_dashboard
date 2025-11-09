from dash import dcc
from dash.dash_table import DataTable
from dash.dash_table.Format import Format, Scheme, Group
import utils.table_utils as table_utils
import plotly.express as px
import plotly.graph_objects as go


def get_dividends_pie_chart(obtained_dividends_df, data_column, group_by_column):
    """
    recibo los datos y filtros
    filtro el DF

    creo el pie chart y le paso los datos
    devuelvo el piechart
    """
    pie_chart_id = f"dividends_weight_pie_chart"
    pop_up_text_html = "<b>%{label} (%{percent})</b>  <br> " + data_column + ": %{value:,.2f}"

    # Creacion de pie chart
    weight_by_criteria_pie_chart = px.pie(
        obtained_dividends_df,
        values=data_column,
        names=group_by_column,
        # template="vizro_dark"
        # template="plotly_dark"
    )

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
    weight_by_criteria_pie_chart.update_layout(
        legend=legend_format_dict,
        hoverlabel=pop_up_format_dict,
        paper_bgcolor='rgba(0,0,0,0)',  # Quita el background de la grafica
        plot_bgcolor='rgba(0,0,0,0)'
    )

    weight_by_criteria_pie_chart_html_component = dcc.Graph(
        id=pie_chart_id,
        figure=weight_by_criteria_pie_chart,
        config={'displayModeBar': False}
    )
    return weight_by_criteria_pie_chart_html_component


def get_dividends_table(weight_by_criteria_df, group_by_column, table_id):
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
                                                        id=table_id,
                                                        style_header=style_header,
                                                        style_data=style_data,
                                                        style_data_conditional=style_data_conditional,
                                                        style_table=style_table
                                                        )
    return weight_by_criteria_table_html_component


def get_dividend_evolution_bar_chart(obtained_dividends_df, data_column, group_by_column_list):
    bar_chart_id = f"dividend_evolution_bar_chart"
    # pop_up_text_html = "<b>%{label} (%{percent})</b>  <br> " + data_column + ": %{value:,.2f}"

    if (len(group_by_column_list) > 1) & ("Año" in group_by_column_list[0]):
        # Case to group by Year and Currency
        group_by_column = group_by_column_list[0]
        color_column = group_by_column_list[1]
        dividend_evolution_bar_chart = px.bar(
            obtained_dividends_df,
            x=group_by_column,
            y=data_column,
            barmode="group",
            color=color_column
        )
    else:
        # Case to group by Year
        group_by_column = group_by_column_list[0]
        dividend_evolution_bar_chart = px.bar(
            obtained_dividends_df,
            x=group_by_column,
            y=data_column,
            barmode="group"
        )

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

    # dividend_evolution_bar_chart.update_traces(hovertemplate=pop_up_text_html)
    dividend_evolution_bar_chart.update_layout(
        legend=legend_format_dict,
        hoverlabel=pop_up_format_dict,
        paper_bgcolor="rgba(0,0,0,0)",  # Quita el background de la grafica
        plot_bgcolor="rgba(0,0,0,0)"
    )

    dividend_evolution_bar_chart_html_component = dcc.Graph(
        id=bar_chart_id,
        figure=dividend_evolution_bar_chart,
        config = {'displayModeBar': False}
    )

    return dividend_evolution_bar_chart_html_component


def get_kpi_indicator(
        id, text_dict, value, mode, domain_dict,
        height, margin_dict, paper_bgcolor, number={"valueformat": ",.0f"}
):
    kpi_indicator = go.Figure(go.Indicator(
        mode=mode,
        value=value,
        title=text_dict,
        # IMPORTANT: "Domain" is to determine the position and size of the "Indicator"
        # With {'x': [0, 1], 'y': [0, 1]} we are saying: "start at the point 0 in X and you can occupy the 100% of
        # your cells width". Same for the Y.
        domain=domain_dict,
        number=number
    ))

    # Ajuste de layout para un aspecto limpio de KPI
    # TODO: tengo que cambiar esto de alguna forma para que NO se gestione esto desde aquí, si no con el CSS
    # Para así poder permitir que los KPIs sean RELATIVOS al tamaño de pantalla del USER
    kpi_indicator.update_layout(
        height=height,
        margin=margin_dict, # t -> Margin top, b -> Margin bottom, l -> Margin left, r -> Maring right
        paper_bgcolor=paper_bgcolor
    )





    # total_brute_obtained_dividends_indicator = go.Figure(go.Indicator(
    #     mode="number",
    #     value=value,
    #     title=text_dict,
    #     # IMPORTANT: "Domain" is to determine the position and size of the "Indicator"
    #     # With {'x': [0, 1], 'y': [0, 1]} we are saying: "start at the point 0 in X and you can occupy the 100% of
    #     # your cells width". Same for the Y.
    #     domain={'x': [0, 1], 'y': [0, 1]}
    # ))
    #
    # # Ajuste de layout para un aspecto limpio de KPI
    # # TODO: tengo que cambiar esto de alguna forma para que NO se gestione esto desde aquí, si no con el CSS
    # # Para así poder permitir que los KPIs sean RELATIVOS al tamaño de pantalla del USER
    # total_brute_obtained_dividends_indicator.update_layout(
    #     height=150,
    #     margin=dict(t=40, b=10, l=10, r=10), # t -> Margin top, b -> Margin bottom, l -> Margin left, r -> Maring right
    #     paper_bgcolor="#f8f9fa"
    # )

    kpi_indicator_html_component = dcc.Graph(
        id=id,
        figure=kpi_indicator,
        config={'displayModeBar': False}
    )
    return kpi_indicator_html_component