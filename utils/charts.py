from dash import dcc
import plotly.graph_objects as go
import plotly.express as px


def get_pie_chart(
        pie_chart_id, data_df, data_column, labels_column, legend_format_dict=None, pop_up_format_dict=None,
        pop_up_text_html=None, paper_bg_color="rgba(0,0,0,0)", plot_bg_color="rgba(0,0,0,0)"
):
    """
    It creates a pie chart using Plotly Express and returns it as a Dash HTML component.

    :param pie_chart_id: the id of the pie chart HTML component
    :param data_df: the dataframe containing the data for the pie chart
    :param data_column: the column from the dataframe to use for the pie chart values
    :param labels_column: the column from the dataframe to use for the pie chart labels
    :param legend_format_dict: a dict to format the legend of the pie chart
    :param pop_up_format_dict: a dict to format the pop-up of the pie chart when hovering it
    :param pop_up_text_html: the HTML text to show in the pop-up when hovering the pie chart
    :param paper_bg_color: a string representing the background color of the paper
    :param plot_bg_color: a string representing the background color of the plot
    :return: a Dash HTML component containing the pie chart
    """

    # Creacion de pie chart
    pie_chart = px.pie(
        data_df,
        values=data_column,
        names=labels_column,
        # template="vizro_dark"
        # template="plotly_dark"
    )

    if pop_up_text_html is not None:
        pie_chart.update_traces(hovertemplate=pop_up_text_html)

    pie_chart.update_layout(
        legend=legend_format_dict,
        hoverlabel=pop_up_format_dict,
        paper_bgcolor=paper_bg_color,  # Quita el background de la grafica
        plot_bgcolor=plot_bg_color
    )

    pie_chart_html_component = dcc.Graph(
        id=pie_chart_id,
        figure=pie_chart,
        config={'displayModeBar': False}
    )

    return pie_chart_html_component


def get_bar_chart(
        bar_chart_id, data_df, x_column, y_column, color_column=None, legend_format_dict=None, pop_up_format_dict=None,
        pop_up_text_html=None, paper_bg_color="rgba(0,0,0,0)", plot_bg_color="rgba(0,0,0,0)"
):
    """
    It creates a bar chart using Plotly Express and returns it as a Dash HTML component.

    :param bar_chart_id: the id of the bar chart HTML component
    :param data_df: the dataframe containing the data for the bar chart
    :param x_column: the column from the dataframe to use for the x-axis
    :param y_column: the column from the dataframe to use for the y-axis
    :param color_column: the column from the dataframe to use for the color of the bars
    :param legend_format_dict: a dict to format the legend of the bar chart
    :param pop_up_format_dict: a dict to format the pop-up of the bar chart when hovering it
    :param pop_up_text_html: the HTML text to show in the pop-up when hovering the bar chart
    :param paper_bg_color: a string representing the background color of the paper
    :param plot_bg_color: a string representing the background color of the plot
    :return: a Dash HTML component containing the bar chart
    """

    bar_chart = px.bar(
        data_df,
        x=x_column,
        y=y_column,
        barmode="group",
        color=color_column
    )

    if pop_up_text_html is not None:
        bar_chart.update_traces(hovertemplate=pop_up_text_html)

    bar_chart.update_layout(
        legend=legend_format_dict,
        hoverlabel=pop_up_format_dict,
        paper_bgcolor=paper_bg_color,
        plot_bgcolor=plot_bg_color
    )

    bar_chart_html_component = dcc.Graph(
        id=bar_chart_id,
        figure=bar_chart,
        config={'displayModeBar': False}
    )

    return bar_chart_html_component


def get_kpi_indicator(
        kpi_id, text_dict, value, mode, domain_dict, height, margin_dict,
        paper_bg_color="rgba(0,0,0,0)", number={"valueformat": ",.0f"}
):
    """
    It creates a KPI indicator using Plotly Graph Objects and returns it as a Dash HTML component.

    :param kpi_id: the id of the KPI indicator HTML component
    :param text_dict: a dict containing the title and subtitle of the KPI
    :param value: a numeric value to show in the KPI
    :param mode: a string representing the mode of the KPI (e.g., "number", "gauge+number", etc.)
    :param domain_dict: a dict to determine the position and size of the "Indicator"
                        With {'x': [0, 1], 'y': [0, 1]} we are saying:
                        "start at the point 0 in X and you can occupy the 100% of your cells width".
                        Same for the Y.
    :param height: the height of the KPI indicator in pixels
    :param margin_dict: a dict containing the margins of the KPI indicator
    :param paper_bg_color: a string representing the background color of the paper
    :param number: a dict to format the number shown in the KPI
    :return: a Dash HTML component containing the KPI indicator
    """

    kpi_indicator = go.Figure(go.Indicator(
        mode=mode,
        value=value,
        title=text_dict,
        domain=domain_dict,
        number=number
    ))

    # Ajuste de layout para un aspecto limpio de KPI
    # TODO: tengo que cambiar esto de alguna forma para que NO se gestione esto desde aquí, si no con el CSS
    # Para así poder permitir que los KPIs sean RELATIVOS al tamaño de pantalla del USER
    kpi_indicator.update_layout(
        height=height,
        margin=margin_dict,  # t -> Margin top, b -> Margin bottom, l -> Margin left, r -> Maring right
        paper_bgcolor=paper_bg_color
    )

    kpi_indicator_html_component = dcc.Graph(
        id=kpi_id,
        figure=kpi_indicator,
        config={'displayModeBar': False}
    )

    return kpi_indicator_html_component
