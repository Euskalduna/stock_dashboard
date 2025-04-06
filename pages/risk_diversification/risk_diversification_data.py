import pandas as pd
import numpy as np
import utils.data_utils as data_utils




def get_purchases_and_sales():
    purchases_and_sales_df = data_utils.get_purchases_and_sales_log()
    company_info_df = data_utils.get_company_info()

    purchases_and_sales_df['pk'] = purchases_and_sales_df['Mercado'].astype(str) + purchases_and_sales_df['Ticker'].astype(str)
    company_info_df = company_info_df.rename(columns={'PK': 'pk'})
    purchases_and_sales_enriched_df = purchases_and_sales_df.merge(
        company_info_df[['pk', 'Sector', 'Moneda del mercado', 'Pais']],
        how="left", on='pk')
    return purchases_and_sales_enriched_df


def get_weight_by_criteria_for_risk(purchases_and_sales_enriched_df, data_column, group_by_column, filter_dict_list=[]):
    def calculate_weight_by_group(df, group, weight_criteria):
        df_grouped = df.groupby(group).sum()[weight_criteria].reset_index().copy()
        df_grouped['weight'] = (df_grouped[weight_criteria] / df_grouped[weight_criteria].sum() * 100).round(2)
        # df_grouped['weight_to_display'] = df_grouped['weight'].apply(lambda value: f'{value} %')
        return df_grouped

    def calculate_stock_value(stock_number, latest_stock_price):
        latest_stock_value = np.nan
        try:
            latest_stock_value = stock_number * latest_stock_price
        except Exception as e:
            print(e)
        return latest_stock_value

    # df['Dinero (EUR)'] = df.loc[df['Acción'] == 'Venta', 'Dinero (EUR)'].apply(lambda value: value * -1) # Tengo que compensar de alguna forma las ventas que he hecho, pero este no funciona INVESTIGAR MÁS!!!
    # filter_dict_list = ['column_to_filter': 'Propietario', 'values_to_keep':[]]

    # Get the stocks latest values in each of the log's rows
    company_info_df = purchases_and_sales_enriched_df[['Ticker', 'Mercado', 'Moneda del mercado']].drop_duplicates()
    company_info_df = data_utils.get_companies_latest_stock_price(company_info_df)
    purchases_and_sales_enriched_df = purchases_and_sales_enriched_df.merge(company_info_df, on=["Ticker", "Mercado"], how='left')
    purchases_and_sales_enriched_df['latest_stock_value_in_euros'] = purchases_and_sales_enriched_df.apply(lambda row: calculate_stock_value(row['Acciones'], row['latest_stock_price_in_euros']), axis=1)

    for filter_dict in filter_dict_list:
        column_to_filter = filter_dict['column_to_filter']
        values_to_keep_list = filter_dict['values_to_keep']
        if 'Todo' not in values_to_keep_list:
            purchases_and_sales_enriched_df = purchases_and_sales_enriched_df[purchases_and_sales_enriched_df[column_to_filter].isin(values_to_keep_list)]

    weight_by_criteria_df = calculate_weight_by_group(
        purchases_and_sales_enriched_df,
        group=[group_by_column],
        weight_criteria=data_column
    )

    weight_by_criteria_df[data_column] = weight_by_criteria_df[data_column].round(2)
    weight_by_criteria_df = weight_by_criteria_df.sort_values(by=['weight'], ascending=False)
    return weight_by_criteria_df
