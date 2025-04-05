import pandas as pd


def get_purchases_and_sales_log():
    compra_ventas_df = pd.read_csv("data/log_compra_venta.csv", decimal=",")
    # compra_ventas_df = pd.read_csv("data/log_compra_venta_AITA.csv", decimal=",")
    return compra_ventas_df


def get_company_info():
    company_info_df = pd.read_csv("data/info_empresas.csv", decimal=",")
    # company_info_df = pd.read_csv("data/info_empresas_AITA.csv", decimal=",")
    return company_info_df


def get_purchases_and_sales():
    purchases_and_sales_df = get_purchases_and_sales_log()
    company_info_df = get_company_info()

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

    # df['Dinero (EUR)'] = df.loc[df['Acción'] == 'Venta', 'Dinero (EUR)'].apply(lambda value: value * -1) # Tengo que compensar de alguna forma las ventas que he hecho, pero este no funciona INVESTIGAR MÁS!!!
    # filter_dict_list = ['column_to_filter': 'Propietario', 'values_to_keep':[]]
    df = purchases_and_sales_enriched_df.copy()
    for filter_dict in filter_dict_list:
        column_to_filter = filter_dict['column_to_filter']
        values_to_keep_list = filter_dict['values_to_keep']
        if 'Todo' not in values_to_keep_list:
            df = df[df[column_to_filter].isin(values_to_keep_list)]

    weight_by_criteria_df = calculate_weight_by_group(
        df,
        group=[group_by_column],
        weight_criteria=data_column
    )

    weight_by_criteria_df[data_column] = weight_by_criteria_df[data_column].round(2)
    weight_by_criteria_df = weight_by_criteria_df.sort_values(by=['weight'], ascending=False)
    return weight_by_criteria_df
