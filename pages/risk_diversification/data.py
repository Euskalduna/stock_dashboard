from utils.global_variables import context
import numpy as np
import utils.data_utils as data_utils


def get_page_data():
    purchases_and_sales_enriched_df = data_utils.get_purchases_and_sales_enriched()
    purchases_and_sales_enriched_df = purchases_and_sales_enriched_df[purchases_and_sales_enriched_df["Ticker"].notna()]
    purchases_and_sales_enriched_df = purchases_and_sales_enriched_df[
        purchases_and_sales_enriched_df["Tipo de Valor"] == "Acción"]
    return purchases_and_sales_enriched_df


def get_weight_by_criteria_for_risk(purchases_and_sales_enriched_df, data_column, group_by_column, filter_dict_list=[]):
    def calculate_weight_by_group(df, group, weight_criteria):
        # Si la empresa tiene tipo de valor accion y accion es VENTA, entonces, debo multiplicar el valor por -1
        # ventas_df = df[(df["Tipo de Valor"] == "Acción") & (df["Acción"] == "Venta")]
        # ventas_df.loc[:, ["Acciones", "Dinero", "Dinero (EUR)"]] = ventas_df.loc[:, ["Acciones", "Dinero", "Dinero (EUR)"]] * -1

        # # Corrijo los registros de venta, para que computen como negativas algunas columnas
        # sales_condition = (df["Tipo de Valor"] == "Acción") & (df["Acción"] == "Venta")
        # sales_columns_to_alter = ["Acciones", "Dinero", "Dinero (EUR)"]
        # df.loc[sales_condition, sales_columns_to_alter] = df.loc[sales_condition, sales_columns_to_alter] * -1

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
    company_stock_prices_df = context['company_stock_prices_df'].copy()
    purchases_and_sales_enriched_df = purchases_and_sales_enriched_df.merge(company_stock_prices_df, on=["Ticker", "Mercado"], how='left')
    purchases_and_sales_enriched_df['latest_stock_value_in_euros'] = purchases_and_sales_enriched_df.apply(lambda row: calculate_stock_value(row['Acciones'], row['latest_stock_price_in_euros']), axis=1)
    purchases_and_sales_enriched_df = purchases_and_sales_enriched_df.rename({'latest_stock_value_in_euros': 'Ultimo Valor (EUR)'}, axis=1)

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

    weight_by_criteria_df = weight_by_criteria_df[weight_by_criteria_df[data_column] != 0]
    weight_by_criteria_df[data_column] = weight_by_criteria_df[data_column].round(3)
    weight_by_criteria_df = weight_by_criteria_df.sort_values(by=['weight'], ascending=False)
    return weight_by_criteria_df
