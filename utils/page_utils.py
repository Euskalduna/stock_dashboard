import data_utils

# def get_risk_diversification_data(weight_criteria_column, risk_criteria_dict):
#     def calculate_weight_by_group(df, group, weight_criteria):
#         df_grouped = df.groupby(group).sum()[weight_criteria].reset_index().copy()
#         df_grouped['weight'] = (df_grouped[weight_criteria] / df_grouped[weight_criteria].sum() * 100).round(2)
#         # df_grouped['weight_to_display'] = df_grouped['weight'].apply(lambda value: f'{value} %')
#         return df_grouped
#
#     compra_ventas_df = data_utils.get_purchases_and_sales_log()
#     company_info_df = data_utils.get_company_info()
#
#
#     # TRANSFORMACIONES DE DATOS
#     ## UNIONES DE DATOS
#     compra_ventas_df['pk'] = compra_ventas_df['Mercado'].astype(str) + compra_ventas_df['Ticker'].astype(str)
#     company_info_df = company_info_df.rename(columns={'PK': 'pk'})
#     compra_ventas_enriched_df = compra_ventas_df.merge(company_info_df[['pk', 'Sector', 'Moneda del mercado', 'Pais']],
#                                                        how="left", on='pk')
#
#     # CALCULOS
#     # df['Dinero (EUR)'] = df.loc[df['Acción'] == 'Venta', 'Dinero (EUR)'].apply(lambda value: value * -1) # Tengo que compensar de alguna forma las ventas que he hecho, pero este no funciona INVESTIGAR MÁS!!!
#     weight_by_criteria_df = calculate_weight_by_group(
#         compra_ventas_enriched_df,
#         group=[risk_criteria_dict['data_column']],
#         weight_criteria=weight_criteria_column
#     )
#     weight_by_criteria_df[weight_criteria_column] = weight_by_criteria_df[weight_criteria_column].round(2)
#     weight_by_criteria_df = weight_by_criteria_df.sort_values(by=['weight'], ascending=False)
#     return weight_by_criteria_df






