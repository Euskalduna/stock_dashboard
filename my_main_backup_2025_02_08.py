import pandas as pd
from dash import Dash, html, dcc, dash_table, Output, Input, State, MATCH, ALL, callback_context
import dash_bootstrap_components as dbc
import plotly.express as px

"""
# CONSEJOS
## Organizacion de codigo (modularizacion)
- crear archivos "utils"
En esta carpeta, en los archivos va a haber un fichero "XXX_utils.py" que va a tener las funciones de ese ambito
Esto sería algo así como
    + Crear una carpeta utils
    + Meter en ella fichero charts_utils.py (contiene funciones de gráficos)
    + Meter en ella fichero data_utils.py (contiene funciones de ETL)
Una función a poner en un fichero "utils" seria cualquier funcion que hace algún cálculo complejo y NO crea una página 

- crear archivos "page"
En esta carpeta , los archivos son el código que genera cada una de las páginas de la app
EJEMPLO:
    + pages (carpeta)
        + home_page.py
        + other_page.py
Estos archivos, su "main" sería generar un metodo llamado "layout" (distribución) que debería de devolver la distribución
de la página que representa este archivo
PARA CAMBIAR DE LAYOUT se utiliza el componente de la librería DCC llamado link (dcc.Link entiendo que sería), esto cambia la URL sin recargar la página 
LUEGO se utliza el componente de DCC llamado location (dcc.Location entiendo que sería) que lee como input el link en un Callback
LA FORMA MÁS SIMPLE AHORA es utilizar la feature Dash Pages


## Code formatters (Readability)
- Utilizar un Python formatter. Ellos usan uno llamado "black"





# Consejos / tutorial de Bootstrap + Dash Plotly        https://www.youtube.com/watch?v=0mfIK8zxUds 
- UTILIZAR  
    app.layout = dbc.Container()
EN LUGAR DE
    app.layout = html.Div()

- Dentro de lo anterior, lo primero a declarar son los ROWs  y luego dentro de los ROWs, los COLs
Dentro de los COLS, directamente ponemos el componente
Los ROWs a parte del atributo CHILDREN tienen un atributo llamado NO_GUTTERS, que si lo pones a TRUE hace que las COLUMNAS HIJAS NO TENGAN NINGUN TIPO DE SEPARACION ENTRE ELLAS

Los COLS a parte del atributo CHILDREN tienen un atributo llamado WIDTH  que puede ser de hasta 12. (indica el nº de columnas a ocupar)
EJ:
    width = 4
    width = {'size': 4}
    width = {'size': 4, 'offset':1} 
    width = {'size': 4, 'offset':1, 'order':2} # La clave ORDER hace que Col esté en 2 posición respecto a los otros, se utiliza para no tener que escribir en orden los componentes 

- Si quiero darle estilos asignando una clase, usao las clases de bootstrap natural. Si quiero poner más de una, ponerlas separadas por espacio NO POR COMA
- 
"""

"""
# PRINCIPIOS DE DASH

Habría que dividir el proyecto en 3 secciones principales
    - Una para preparar los datos
    - Otra para preparar los componentes y aspecto de la página 
    - Otra para dar el comportamiento a las cosas (esto es con los callbacks)

# Princpios de los callbacks
Los callbacks son metodos normales con un decoratos
Recibe 2 listas
    - Outputs --> Puede tener N componentes PERO al finalizar el metodo y poner RETURN el número de elementos
    a devolver han de ser los mismos Y EN EL MISMO ORDEN QUE LOS QUE PUSE
    - Inputs --> Puede tener N componentes PERO han de ser los mismos que los argumentos que recibe el metodo 
    al que se le ha puesto el decorator

Estas listas tienen como elementos OBJETOS Output o Input, en funcion de lo que tenga que tener la lista
Ambos tienen los mismos argumentos
    - component_id -> ID del componenten en el que tiene que escribir (si es OUTPUT) o del que recibe cosas (si es INPUT)
    - component_property -> nombre de la propiedad del elemento al que apunta. 
    SOBREESCRIBE (OVERWRITE, no APPEND) el valor en esa propiedad (si es OUTPUT) o coge los datos de esa (Si es IPNUT)
    Puede coger / volcar datos EN CUALQUIER PROPIEDAD DEL COMPONENTE


# Buenas practicas a la hora de manejar los datos
- Hacer una copia del DF inicial y luego ya hacer los filtros, agrupaciones, sumas... 

"""

"""
# OBJETIVO INICIAL: 
crear una página que tenga la diversificacion de mi cartera
Esta diversificación ha de ser por 2 criterios, dinero invertido y valor del stock

Se tiene que crear una página solo con 4 criterios de diversificación:
    - Por empresa
    - Por sector
    - Por pais
    - Por moneda
Y esto es calcular los pesos por los criterios dichos.
Se ha de poder cambiar los pesos cambiando en un DROPDOWN el criterio que indica el peso

Los datos han de leerse de mi cuenta de Google
Tengo que crear un .exe que me abra el Cuadro de Mando

UNA VEZ HECHO ESTO, ya nos podemos poner creativos intentando crear páginas

# DISEÑO INICIAL
Quiero una página que tiene un DIV principal
Este DIV principal se va a dividir en 5
    - Uno que será la primera fila y que cogerá toda la página en la parte superior (Aquí pondre el Título, el dropdown y las notas)
    - En la siguiente fila, tendré que dividirla en 2 y el lado izquierdo será para uno de los criterios y el derecho para el otro 
    - En la siguiente fila, tendré que dividirla en 2 y el lado izquierdo será para uno de los criterios y el derecho para el otro 

 Cada uno de los DIVs con para mostrar la diversificación consistirá en 2 elementos
    - Una tabla
    - Un gráfico de tarta

Los DIVs y la distancia y tamaño de los elementos entre ellos HAN DE SER DINÁMICOS
"""

"""
posibles colores
#3f4057 ---"claro"
#292a3e ---"oscuro"

"""


# def get_data_log_compra_venta():
#     compra_ventas_df = pd.read_csv("data/log_compra_venta.csv", decimal=",")
#     return compra_ventas_df

# def get_invested_euros_by_company(df):
#     #df['Dinero (EUR)'] = df.loc[df['Acción'] == 'Venta', 'Dinero (EUR)'].apply(lambda value: value * -1) # Tengo que compensar de alguna forma las ventas que he hecho, pero este no funciona INVESTIGAR MÁS!!!
#     invested_euros_by_company_df = df.groupby('Ticker').sum()['Dinero (EUR)'].reset_index()
#     return invested_euros_by_company_df

def create_pie_chart(df):
    title = None
    fig = px.pie(df, values='Dinero (EUR)', names='Ticker', title=title)
    return fig


def create_table(df):
    return None


# Inicio de la aplicacion
# app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# Other themes https://www.bootstrapcdn.com/bootswatch/
# Cheatsheet https://hackerthemes.com/bootstrap-cheatsheet/

compra_ventas_df = pd.read_csv("data/log_compra_venta.csv", decimal=",")
company_info_df = pd.read_csv("data/info_empresas.csv", decimal=",")

# TRANSFORMACIONES DE DATOS
## UNIONES DE DATOS
compra_ventas_df['pk'] = compra_ventas_df['Mercado'].astype(str) + compra_ventas_df['Ticker'].astype(str)
company_info_df = company_info_df.rename(columns={'PK': 'pk'})
compra_ventas_enriched_df = compra_ventas_df.merge(company_info_df[['pk', 'Sector', 'Moneda del mercado', 'Pais']],
                                                   how="left", on='pk')


def calculate_weight_by_group(df, group, weight_criteria):
    df_grouped = df.groupby(group).sum()[weight_criteria].reset_index().copy()
    df_grouped['weight'] = (df_grouped[weight_criteria] / df_grouped[weight_criteria].sum() * 100).round(2)
    df_grouped['weight_to_display'] = df_grouped['weight'].apply(lambda value: f'{value} %')
    return df_grouped


def get_diversification_panel_children(diversification_criteria, pie_chart_html_component, table_html_component):
    title = f"Diversificación por {diversification_criteria}"
    table_button_id = {'type': 'update-table-visibility-button', 'index': diversification_criteria}
    pie_chart_button_id = {'type': 'update-pie_chart-visibility-button', 'index': diversification_criteria}
    # pie_chart_id = f"weight_by_{diversification_criteria}_pie_chart"
    # table_id = f"weight_by_{diversification_criteria}_table"
    table_id = {'type': 'table-container', 'index': diversification_criteria}
    pie_chart_id = {'type': 'pie_chart-container', 'index': diversification_criteria}

    pie_title_row = dbc.Row([
        # dbc.Col([html.H2(title)], width=6),
        dbc.Col([html.H2(title)]),
        dbc.Col([
            dbc.Button('Grafico',
                       className="btn btn-secondary float-right",
                       color="danger",
                       id=pie_chart_button_id),
            dbc.Button('Tabla',
                       className="btn btn-secondary float-right",
                       color="danger",
                       id=table_button_id),
        ]),
    ])

    data_row = dbc.Row([
        dbc.Col([pie_chart_html_component], id=pie_chart_id, className="d-block col-md-6"),
        dbc.Col([table_html_component], id=table_id, className="d-block col-md-6")
    ])

    # diversification_div = dbc.Row(dbc.Col(([pie_title_row, data_row])))
    diversification_div_children = [pie_title_row, data_row]
    return diversification_div_children


default_weight_criteria_column = 'Dinero (EUR)'
risk_diversification_criteria_list = [
    {'criteria_name': 'empresa', 'data_column': 'Ticker'},
    {'criteria_name': 'sector', 'data_column': 'Sector'},
    {'criteria_name': 'pais', 'data_column': 'Pais'},
    {'criteria_name': 'moneda', 'data_column': 'Moneda del mercado'},
]

for risk_criteria in risk_diversification_criteria_list:
    pie_chart_id = f"diversification_by_{risk_criteria['criteria_name']}_pie_chart"

    # CALCULOS
    # df['Dinero (EUR)'] = df.loc[df['Acción'] == 'Venta', 'Dinero (EUR)'].apply(lambda value: value * -1) # Tengo que compensar de alguna forma las ventas que he hecho, pero este no funciona INVESTIGAR MÁS!!!
    weight_by_criteria_df = calculate_weight_by_group(
        compra_ventas_enriched_df,
        group=[risk_criteria['data_column']],
        weight_criteria=default_weight_criteria_column
    )
    weight_by_criteria_df = weight_by_criteria_df.sort_values(by=['weight'], ascending=False)

    # Creacion de pie chart
    weight_by_criteria_pie_chart = px.pie(
        weight_by_criteria_df,
        values=default_weight_criteria_column,
        names=risk_criteria['data_column']
    )
    weight_by_criteria_pie_chart_html_component = dcc.Graph(id=pie_chart_id, figure=weight_by_criteria_pie_chart)

    # Creacion de tabla
    weight_by_criteria_table_html_component = dash_table.DataTable(weight_by_criteria_df.to_dict('records'),
                                                                   [{"name": i, "id": i} for i in
                                                                    weight_by_criteria_df.columns])

    # Creacion del div final
    weight_by_criteria_div_children = get_diversification_panel_children(
        diversification_criteria=risk_criteria['criteria_name'],
        pie_chart_html_component=weight_by_criteria_pie_chart_html_component,
        table_html_component=weight_by_criteria_table_html_component
    )
    weight_by_criteria_div_children
    risk_criteria['diversification_div'] = weight_by_criteria_div_children

content_first_row = dbc.Row([
    dbc.Col(risk_diversification_criteria_list[0]['diversification_div'], id="diversification_by_company_col"),
    dbc.Col(risk_diversification_criteria_list[1]['diversification_div'], id="diversification_by_sector_col"),
])

content_second_row = dbc.Row([
    dbc.Col(risk_diversification_criteria_list[2]['diversification_div'], id="diversification_by_country_col"),
    dbc.Col(risk_diversification_criteria_list[3]['diversification_div'], id="diversification_by_currency_col"),
])

option_list = ['Compañía', 'Sector', 'País', 'Moneda']
options = [{'label': option.capitalize(), "value": option} for option in option_list]

page_title_row = dbc.Row(dbc.Col(html.H1('Diversifiación de Riesgos')))
selector_row = dbc.Row([
    dbc.Col([dcc.Dropdown(['Dinero Invertido (Euros)', 'Peso de Cotizacion (Euros)'])], width=2),
    dbc.Col([dcc.Checklist(options=options, inline=True, value=option_list, id="diversification_section_checklist")],
            width=3)
])
content_row = dbc.Row(dbc.Col([content_first_row, content_second_row]))

app.layout = dbc.Container(children=[page_title_row, selector_row, content_row], fluid=True)


@app.callback(
    [
        Output("diversification_by_company_col", "className"),
        Output("diversification_by_sector_col", "className"),
        Output("diversification_by_country_col", "className"),
        Output("diversification_by_currency_col", "className"),
    ],
    [
        Input("diversification_section_checklist", "value")
    ]
)
def update_data_section_display(selected_options):
    # Según si su opcion está marcada o no, muestro u oculto un panel
    diversification_by_company_div_class = 'col-md-6' if 'Compañía' in selected_options else 'd-none'
    diversification_by_sector_div_class = 'col-md-6' if 'Sector' in selected_options else 'd-none'
    diversification_by_country_div_class = 'col-md-6' if 'País' in selected_options else 'd-none'
    diversification_by_currency_div_class = 'col-md-6' if 'Moneda' in selected_options else 'd-none'

    if 'Compañía' in selected_options and 'Sector' not in selected_options:
        diversification_by_company_div_class = 'col-md-12'
    if 'Sector' in selected_options and 'Compañía' not in selected_options:
        diversification_by_sector_div_class = 'col-md-12'
    if 'País' in selected_options and 'Moneda' not in selected_options:
        diversification_by_country_div_class = 'col-md-12'
    if 'Moneda' in selected_options and 'País' not in selected_options:
        diversification_by_currency_div_class = 'col-md-12'

    return (diversification_by_company_div_class, diversification_by_sector_div_class,
            diversification_by_country_div_class, diversification_by_currency_div_class)


# @app.callback(
#     [
#         Output("diversification_by_company_col", "className"),
#         Output("diversification_by_sector_col", "className"),
#         Output("diversification_by_country_col", "className"),
#         Output("diversification_by_currency_col", "className"),
#     ],
#     [
#         Input("diversification_section_checklist", "value")
#     ]
# )
# def update_data_section_display(selected_options):
#     # Según si su opcion está marcada o no, muestro u oculto un panel
#     diversification_by_company_div_class = 'col-md-6' if 'Compañía' in selected_options else 'd-none'
#     diversification_by_sector_div_class = 'col-md-6' if 'Sector' in selected_options else 'd-none'
#     diversification_by_country_div_class = 'col-md-6' if 'País' in selected_options else 'd-none'
#     diversification_by_currency_div_class = 'col-md-6' if 'Moneda' in selected_options else 'd-none'
#
#     if 'Compañía' in selected_options and 'Sector' not in selected_options:
#         diversification_by_company_div_class = 'col-md-12'
#     if 'Sector' in selected_options and 'Compañía' not in selected_options:
#         diversification_by_sector_div_class = 'col-md-12'
#     if 'País' in selected_options and 'Moneda' not in selected_options:
#         diversification_by_country_div_class = 'col-md-12'
#     if 'Moneda' in selected_options and 'País' not in selected_options:
#         diversification_by_currency_div_class = 'col-md-12'
#
#     return (diversification_by_company_div_class, diversification_by_sector_div_class,
#             diversification_by_country_div_class, diversification_by_currency_div_class)


#
# 2 INPUTS
#     boton de la tabla
#     clases del grafico
#
# 2 outputs
#     clases de la tabla
#     clases del grafico


@app.callback(
    [Output({'type': 'table-container', 'index': MATCH}, 'className'),
     Output({'type': 'pie_chart-container', 'index': MATCH}, 'className')],
    [Input({'type': 'update-table-visibility-button', 'index': MATCH}, 'n_clicks'),
     Input({'type': 'update-pie_chart-visibility-button', 'index': MATCH}, 'n_clicks')],
    [State({'type': 'table-container', 'index': MATCH}, 'className'),
     State({'type': 'pie_chart-container', 'index': MATCH}, 'className')]
)
def toggle_table(n_clicks_table_button, n_clicks_pie_chart_button, table_class,
                 pie_chart_class):  # ALGO PASA QUE CUANDO ACTIVO ESTE CALLBACK LAS SEGUNDAS TABLAS SE SALTAN DE LINEA, DESCONOZCO POR QUÉ.
    # PUEDE SER UN TEMA DE TAMAÑOS DE PANTALLA Y TAMAÑO DE LA TABLA.
    # DE MOMENTO VOY A PASAR DE ELLO PORQUE NO HE CONSEGUIDO ENCONTRAR LA CASUA, SOLO QUE SI LO PASO A UNA PANTALLA GRANDE NO SALTE DE LINEA

    # Cuando empieza el programa, NO hay ningún triger, por lo que le caso del ELSE tendria que ser simplemente
    # devolver las clases de table y pie_chart_class

    context = callback_context.triggered
    trigger_id_txt = context[0]['prop_id'].split('.')[0]
    # trigger_id3 = eval(context['prop_id'].split('.')[0])['type']

    # if trigger_id is vacio
    #     return lo  que  habia
    #
    # else
    #     el tocho
    #
    if trigger_id_txt == '':
        print("holaaaaa")
        return [pie_chart_class, table_class]
    else:
        if eval(trigger_id_txt)['type'] == "update-table-visibility-button":
            # Miro si la tarta está oculta o no
            print()
            print("-------------")
            print(f"table_class: {table_class}")
            print(f"pie_chart_class: {pie_chart_class}")

            is_pie_chart_hidden = "d-none" in pie_chart_class
            table_final_class = "col-12-md" if is_pie_chart_hidden else "col-6-md"
            pie_chart_class = pie_chart_class.replace(
                "col-md-12", "col-md-6")

            if n_clicks_table_button is None:
                table_final_class = 'd-block'
                print(f"table_final_class: {table_class}")
                print(f"pie_chart_class: {pie_chart_class}")
                return [table_final_class, pie_chart_class]

            if "d-block" in table_class:
                table_final_class = "d-none"
                pie_chart_class = pie_chart_class.replace(
                    "col-md-6", "col-md-12")
                return [table_final_class, pie_chart_class]

            table_final_class = " ".join(
                [table_final_class] + ['d-block'])
            return [table_final_class, pie_chart_class]

        elif eval(trigger_id_txt)['type'] == "update-pie_chart-visibility-button":
            # Miro si la tarta está oculta o no
            print()
            print("-------------")
            print(f"pie_chart_class: {pie_chart_class}")
            print(f"table_class: {table_class}")

            is_table_hidden = "d-none" in table_class
            pie_chart_final_class = "col-12-md" if is_table_hidden else "col-6-md"
            table_class = table_class.replace("col-md-12", "col-md-6")

            if n_clicks_pie_chart_button is None:
                pie_chart_final_class = 'd-block'
                print(f"pie_chart_class: {pie_chart_final_class}")
                print(f"table_final_class: {table_class}")
                return [pie_chart_final_class, table_class]

            if "d-block" in table_class:
                pie_chart_final_class = "d-none"
                table_class = table_class.replace("col-md-6", "col-md-12")
                return [pie_chart_final_class, table_class]

            pie_chart_final_class = " ".join([pie_chart_final_class] + ['d-block'])
            return [pie_chart_final_class, table_class]
        else:
            print("ESTE CASO NO SE COMO HAS LLEGADO")
            raise KeyError


"""
----------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------
"""

#
# @app.callback(
#     [Output({'type': 'table-container', 'index': MATCH}, 'className'),
#      Output({'type': 'pie_chart-container', 'index': MATCH}, 'className')],
#     [Input({'type': 'update-table-visibility-button', 'index': MATCH}, 'n_clicks')],
#     [State({'type': 'table-container', 'index': MATCH}, 'className'),
#      State({'type': 'pie_chart-container', 'index': MATCH}, 'className')]
# )
# def toggle_table(n_clicks_table_button, table_class, pie_chart_class):  # ALGO PASA QUE CUANDO ACTIVO ESTE CALLBACK LAS SEGUNDAS TABLAS SE SALTAN DE LINEA, DESCONOZCO POR QUÉ.
#                                                                         # PUEDE SER UN TEMA DE TAMAÑOS DE PANTALLA Y TAMAÑO DE LA TABLA.
#                                                                         # DE MOMENTO VOY A PASAR DE ELLO PORQUE NO HE CONSEGUIDO ENCONTRAR LA CASUA, SOLO QUE SI LO PASO A UNA PANTALLA GRANDE NO SALTE DE LINEA
#
#
#     # Miro si la tarta está oculta o no
#     print()
#     print("-------------")
#     print(f"table_class: {table_class}")
#     print(f"pie_chart_class: {pie_chart_class}")
#
#     is_pie_chart_hidden = "d-none" in pie_chart_class
#     table_final_class = "col-12-md" if is_pie_chart_hidden else "col-6-md"
#     pie_chart_class = pie_chart_class.replace("col-md-12", "col-md-6")
#
#     if n_clicks_table_button is None:
#         table_final_class = 'd-block'
#         print(f"table_final_class: {table_class}")
#         print(f"pie_chart_class: {pie_chart_class}")
#         return [table_final_class, pie_chart_class]
#
#     if "d-block" in table_class:
#         table_final_class = "d-none"
#         pie_chart_class = pie_chart_class.replace("col-md-6", "col-md-12")
#         return [table_final_class, pie_chart_class]
#
#     table_final_class = " ".join([table_final_class] + ['d-block'])
#     return [table_final_class, pie_chart_class]
#
#
# @app.callback(
#     # [Output({'type': 'table-container', 'index': MATCH}, 'className'),
#     #  Output({'type': 'pie_chart-container', 'index': MATCH}, 'className')],
#     # [Input({'type': 'update-table-visibility-button', 'index': MATCH}, 'n_clicks')],
#     # [State({'type': 'table-container', 'index': MATCH}, 'className'),
#     #  State({'type': 'pie_chart-container', 'index': MATCH}, 'className')]
#
#     [Output({'type': 'pie_chart-container', 'index': MATCH}, 'className'),
#     Output({'type': 'table-container', 'index': MATCH}, 'className')],
#     [Input({'type': 'update-pie_chart-visibility-button', 'index': MATCH}, 'n_clicks')],
#     [State({'type': 'pie_chart-container', 'index': MATCH}, 'className'),
#      State({'type': 'table-container', 'index': MATCH}, 'className')]
# )
# def pie_chart_table(n_clicks_pie_chart_button, pie_chart_class, table_class):   # ALGO PASA QUE CUANDO ACTIVO ESTE CALLBACK LAS SEGUNDAS TABLAS SE SALTAN DE LINEA, DESCONOZCO POR QUÉ.
#                                                                             # PUEDE SER UN TEMA DE TAMAÑOS DE PANTALLA Y TAMAÑO DE LA TABLA.
#                                                                             # DE MOMENTO VOY A PASAR DE ELLO PORQUE NO HE CONSEGUIDO ENCONTRAR LA CASUA, SOLO QUE SI LO PASO A UNA PANTALLA GRANDE NO SALTE DE LINEA
#     # Miro si la tarta está oculta o no
#     print()
#     print("-------------")
#     print(f"pie_chart_class: {pie_chart_class}")
#     print(f"table_class: {table_class}")
#
#     is_table_hidden = "d-none" in table_class
#     pie_chart_final_class = "col-12-md" if is_table_hidden else "col-6-md"
#     table_class = table_class.replace("col-md-12", "col-md-6")
#
#     if n_clicks_pie_chart_button is None:
#         pie_chart_final_class = 'd-block'
#         print(f"pie_chart_class: {pie_chart_final_class}")
#         print(f"table_final_class: {table_class}")
#         return [pie_chart_final_class, table_class]
#
#     if "d-block" in table_class:
#         pie_chart_final_class = "d-none"
#         table_class = table_class.replace("col-md-6", "col-md-12")
#         return [pie_chart_final_class, table_class]
#
#     pie_chart_final_class = " ".join([pie_chart_final_class] + ['d-block'])
#     return [pie_chart_final_class, table_class]


if __name__ == '__main__':
    print("antes")
    app.run_server(debug=True, port=8050)
    print("Despues")

"""

def create_diversification_page(app):
    page = dbc.Container(children=[], fluid=True) # A esto le tengo que hacer append de los hijos


    #page.children = [title_row, body_row]
    return page

    # TENDRIA QUE PENSAR DESDE ABAJO HACIA ARRIBA
    # Es decir, montar 1 cuadricula, luego montar 2 en una fila en 2 columnas, luego 4 en 2 filas, luego ya titulos...




app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
create_diversification_page(app)
app.layout = dbc.Container(children=[title_row, body_row],fluid=True)


"""

"""
1 DIV base (color fondo grisaceo)
    Dentro  crear 1 divs 
        1 div (titulo pagina) (sin color de fondo): Altura, lo que ocupe un H1
        1 Div con filtros: Altura, lo que ocupen los filtros 
        1 div donde estaran las cosas
            aqui dentro tengo que crear 4 divs que deberan de ocupar cada uno 1/4 del espacio del padre (color fondo grisaceo más oscuro)
                cada uno de estos 4 divs se ha de dividir en 2 o 3 divs
                    1 para el titulo
                    otro para el contenido (tabla)
                    otro para el otro contenido (grafico tarta) 
                Los divs tienen que estar en 2 filas


"""

# Using Python's dash-plotly create an app using bootstrap that has 3 rows.
# The first row must contain a title
# The second row must contain a checklist
# The third row must contain a grid of  2 rows and each row must contain two divs that occupy the same width. Each div of the grid has to contain a pie chart.
# Depending on the options selected on the checklist, a div of the grid has to hide or show and the remaining one has to occupy the freed space on the screen

# Using Python's dash-plotly create an app using bootstrap that has 3 rows.
# The first row must contain a title
# The second row contains two buttons
# The third row must contain a grid of 2 columns that occupy the same width. One of the columns must contain a pie chart and the other a table.
# One of the buttons must hide or show the pie chart when clicked and the other button hide or show the table


# Using Python's dash-plotly create an app using bootstrap that has 1 row.
# That row must have 2 cols of 6.
# Each column needs to have a table, a pie chart and two buttons.
# If you click one of the buttons of the column, the table must hide and the pie chart of the column must be shown.
# if you click the other button of the columnm, the pie chart must hide and the table of the column must be shown
# The buttons of column MUST NOT affect the other column

## ESTA CONSULTA A GEMINI NO ESTA FINA
# Using Python's dash-plotly create an app using bootstrap that has 2 rows.
# Each row must have 2 cols of width = 6.
# Each column needs to have another two rows
# in the first row there must be two buttons
# in the second row there must be a table and a pie chart both occupying 6 columns
# If you click one of the buttons of the column, the table must hide or show, deppending on if it is already visible or not
# if you click the other button of the columnm, the pie chart must hide or show, deppending on if it is already visible or not
# The buttons of column MUST NOT affect the other column
# Also whenever a component is shown or hidden, the remaining one must take the rest of the space. This behaviour must be achieved using bootstrap column classes
# NEXT: make the code to use patterns in the Input and Output of the callbacks