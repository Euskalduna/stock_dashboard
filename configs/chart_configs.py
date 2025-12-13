def get_pie_chart_config(legend_orientation="v", yanchor="top", y=1, xanchor="left", x_offset=1.02, font_size=22):
    """
    Returns a reusable configuration for pie charts.
    """
    return {
        "legend_format_dict": {
            "orientation": legend_orientation,
            "yanchor": yanchor,
            "y": y,
            "xanchor": xanchor,
            "x": x_offset,
        },
        "pop_up_format_dict": {"font_size": font_size},
        "pop_up_text_html": "<b>%{label} (%{percent})</b>  <br> Value: %{value:,.2f}",
    }


def get_bar_chart_config(legend_orientation="v", yanchor="top", y=1, xanchor="left", x_offset=1.02, font_size=22):
    """
    Returns a reusable configuration for bar charts.
    """
    return {
        "legend_format_dict": {
            "orientation": legend_orientation,
            "yanchor": yanchor,
            "y": y,
            "xanchor": xanchor,
            "x": x_offset,
        },
        "pop_up_format_dict": {"font_size": font_size},
    }


def get_kpi_indicator_config(
        mode="number", height=150, domain_x=(0, 1), domain_y=(0, 1),
        margin_top=40, margin_bottom=10, margin_left=10, margin_right=10,
        paper_bg_color="#f8f9fa"
):
    """
    margin_dict={"t": 40, "b": 10, "l": 10, "r": 10},
    Returns a reusable configuration for KPI indicators.
    """

    return {
        "mode": mode,
        "height": height,
        "domain_dict": {
            "x": domain_x,
            "y": domain_y
        },
        "margin_dict": {
            "t": margin_top,
            "b": margin_bottom,
            "l": margin_left,
            "r": margin_right
        },
        "paper_bg_color": paper_bg_color,
    }
