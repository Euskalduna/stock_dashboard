from app import app
from dash import Output, Input, State, MATCH, callback_context
import pages.obtained_dividends.page_components.body as obtained_dividends_body
import pages.obtained_dividends.data as obtained_dividends_data
import utils.data_utils as data_utils

@app.callback(
    [Output({'type': 'obtained-dividends-data-panel', 'index': MATCH}, 'children')],
    [Input("owner_dropdown_selector", "value"),
     Input("broker_dropdown_selector", "value"),
     Input("year_dropdown_selector", "value"),
     Input("month_dropdown_selector", "value"),
     Input("country_dropdown_selector", "value"),
     Input("stock_market_dropdown_selector", "value"),
     Input("currency_dropdown_selector", "value"),
     Input("revenue_type_dropdown_selector", "value")]
)
def update_page_data(
        selected_options_owner, selected_options_broker, selected_options_year, selected_options_month,
        selected_options_country, selected_options_stock_market, selected_options_currency, selected_options_revenue_type
):

    def get_new_data_divs_to_draw(
            case_to_update, obtained_dividends_df, currency_to_show_criteria,
            revenue_to_show_criteria
    ):
        def get_data_column(revenue_to_show_criteria, currency_to_show_criteria=None):
            # if revenue_to_show_criteria and currency_to_show_criteria != None:
            if revenue_to_show_criteria and currency_to_show_criteria:
                if currency_to_show_criteria == "Euro" and revenue_to_show_criteria == "Bruto":
                    data_column = "brute_obtained_money_in_euros"
                elif currency_to_show_criteria == "Euro" and revenue_to_show_criteria == "Neto":
                    data_column = "net_obtained_money_in_euros"
                elif currency_to_show_criteria == "Moneda local" and revenue_to_show_criteria == "Bruto":
                    data_column = "brute_obtained_money"
                else:
                    data_column = "net_obtained_money"

            else:
                if revenue_to_show_criteria == "Bruto":
                    data_column = "brute_obtained_money_in_euros"
                else:
                    data_column = "net_obtained_money_in_euros"
            return data_column

        def get_group_columns(currency_to_show_criteria):
            if currency_to_show_criteria == "Euro":
                first_group_by_column = "payment_year"
                second_group_by_column = None
            else:
                first_group_by_column = "payment_year"
                second_group_by_column = "obtained_money_currency"
            return first_group_by_column, second_group_by_column

        new_data_div_list = []

        if case_to_update == "dividend_weight_by_company_panel":
            # Panel del PIE CHART
            weight_criteria_column = get_data_column(revenue_to_show_criteria)

            panel_children = obtained_dividends_body.get_dividends_by_company_panel(
                obtained_dividends_df,
                weight_criteria_column=weight_criteria_column
            )

            new_data_div_list.append(panel_children)

        elif case_to_update == "dividend_evolution_panel":
            # Panel del BAR CHART
            data_column = get_data_column(revenue_to_show_criteria, currency_to_show_criteria)
            first_group_by_column, second_group_by_column = get_group_columns(currency_to_show_criteria)

            panel_children = obtained_dividends_body.get_dividend_evolution_panel(
                obtained_dividends_df,
                data_column,
                first_group_by_column,
                second_group_by_column
            )
            new_data_div_list.append(panel_children)

        elif case_to_update == "dividend_pivot_table_panel":
            # Panel de la TABLA PIVOTE
            ## Me da igual el tipo de REVENUE
            ## ME importan los otros filtros

            panel_children = obtained_dividends_body.get_dividend_pivot_table(obtained_dividends_df)
            new_data_div_list.append(panel_children)

        elif case_to_update == "total_brute_obtained_dividends_panel":
            panel_children = obtained_dividends_body.get_kpi_indicators_panel(obtained_dividends_df)
            new_data_div_list.append(panel_children)

        else:
            print(f"{case_to_update}--> AQUI NO HABRÍA QUE HABER LLEGADO!!!!")

        return new_data_div_list

    # Get filters
    column_filter_list = []

    owner_column_filter_dict = {'column_to_filter': 'owner', 'values_to_keep': selected_options_owner}
    broker_column_filter_dict = {'column_to_filter': 'broker', 'values_to_keep': selected_options_broker}
    year_column_filter_dict = {'column_to_filter': 'payment_year', 'values_to_keep': selected_options_year}
    month_column_filter_dict = {'column_to_filter': 'payment_month', 'values_to_keep': selected_options_month}
    stock_market_column_filter_dict = {'column_to_filter': 'market', 'values_to_keep': selected_options_stock_market}
    country_column_filter_dict = {'column_to_filter': 'stock_market_country', 'values_to_keep': selected_options_country}

    column_filter_list.append(owner_column_filter_dict)
    column_filter_list.append(broker_column_filter_dict)
    column_filter_list.append(year_column_filter_dict)
    column_filter_list.append(month_column_filter_dict)
    column_filter_list.append(stock_market_column_filter_dict)
    column_filter_list.append(country_column_filter_dict)

    # Get selections
    currency_to_show_criteria = selected_options_currency
    revenue_to_show_criteria = selected_options_revenue_type

    # Get the ID of the Panel to update / overwrite its children attribute
    case_to_update = callback_context.outputs_grouping[0]['id']['index']

    # Get the data filtered by the dropdowns
    obtained_dividends_df = data_utils.get_obtained_dividends(column_filter_list)


    # Get the new content for the panel
    new_data_div_list = get_new_data_divs_to_draw(
        case_to_update,
        obtained_dividends_df,
        currency_to_show_criteria,
        revenue_to_show_criteria
    )

    return new_data_div_list
