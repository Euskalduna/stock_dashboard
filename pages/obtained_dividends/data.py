import utils.data_utils as data_utils


def get_page_data():
    obtained_dividends_df = data_utils.get_obtained_dividends()

    return obtained_dividends_df


def get_obtained_dividends_filtered_by_dropdowns(obtained_dividends_df, filter_dict_list):
    filtered_obtained_dividends_df = obtained_dividends_df

    for filter_dict in filter_dict_list:
        column_to_filter = filter_dict['column_to_filter']
        values_to_keep_list = filter_dict['values_to_keep']

        if values_to_keep_list:
            filtered_obtained_dividends_df = obtained_dividends_df[obtained_dividends_df[column_to_filter].isin(values_to_keep_list)]

    return filtered_obtained_dividends_df


def get_weight_by_criteria(obtained_dividends_df, data_column, group_by_column, filter_dict_list=[]):
    def calculate_weight_by_group(df, group, weight_criteria):
        df_grouped = df.groupby(group).sum()[weight_criteria].reset_index().copy()
        df_grouped['weight'] = (df_grouped[weight_criteria] / df_grouped[weight_criteria].sum() * 100).round(2)
        return df_grouped

    # Get the registers to keep
    filtered_obtained_dividends_df = get_obtained_dividends_filtered_by_dropdowns(obtained_dividends_df, filter_dict_list)

    weight_by_criteria_df = calculate_weight_by_group(
        filtered_obtained_dividends_df,
        group=[group_by_column],
        weight_criteria=data_column
    )

    weight_by_criteria_df = weight_by_criteria_df[weight_by_criteria_df[data_column] != 0]
    weight_by_criteria_df[data_column] = weight_by_criteria_df[data_column].round(3)
    weight_by_criteria_df = weight_by_criteria_df.sort_values(by=['weight'], ascending=False)
    return weight_by_criteria_df


def get_dividends_by_year(obtained_dividends_df, data_column, group_by_column_list, filter_dict_list=[]):
    # Get the registers to keep
    filtered_obtained_dividends_df = get_obtained_dividends_filtered_by_dropdowns(obtained_dividends_df, filter_dict_list)

    df_grouped = filtered_obtained_dividends_df.groupby(group_by_column_list).sum()[data_column].reset_index().copy()

    df_grouped = df_grouped[df_grouped[data_column] != 0]
    df_grouped[data_column] = df_grouped[data_column].round(3)
    df_grouped = df_grouped.sort_values(by=['Año Cobro'], ascending=False)
    df_grouped["Año Cobro"] = df_grouped["Año Cobro"].astype(str)
    return df_grouped


def get_dividend_data_for_pivot_table(obtained_dividends_df, filter_dict_list=[]):
    # Get the registers to keep
    filtered_obtained_dividends_df = get_obtained_dividends_filtered_by_dropdowns(obtained_dividends_df, filter_dict_list)

    # Keep the columns that I thought that would be more important to experiment with
    columns_to_keep = ["Año Cobro", "Mes Cobro", "Fecha Cobro", "stock_market_country", "Mercado",
                       "Nombre Empresa", "Ticker", "Propietario", "Broker", "Dinero BRUTO (EUR)",
                       "Dinero NETO Cobrado (EUR)", "Dinero BRUTO Cobrado", "Dinero NETO Cobrado", "Moneda de lo cobrado"]
    return filtered_obtained_dividends_df[columns_to_keep]


# def get_total_brute_obtained_dividends(obtained_dividends_df, filter_dict_list=[]):
#     filtered_obtained_dividends_df = get_obtained_dividends_filtered_by_dropdowns(
#         obtained_dividends_df,
#         filter_dict_list
#     )
#
#     total_brute_obtained_dividends = filtered_obtained_dividends_df["Dinero BRUTO (EUR)"].sum()
#
#     return total_brute_obtained_dividends
