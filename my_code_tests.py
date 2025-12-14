import plotly.graph_objects as go
from dash import Dash, dcc, html

# 1. Crear la Figura de Plotly con el go.Indicator
mi_valor = 1234567.89
fig = go.Figure(
    go.Indicator(
        mode="number",
        value=mi_valor,
        title={'text': "Ingresos Anuales"},
        number={
            # Usar la especificación de formato decimal con '.' para aplicar el locale
            'valueformat': '0f',
        }
    )
)

app = Dash(__name__)

# 2. Definir el Layout de Dash y aplicar el 'locale' en dcc.Graph
app.layout = html.Div([
    dcc.Graph(
        id='indicador-localizado',
        figure=fig,
        # ⬅️ ESTE ES EL PUNTO CLAVE
        config={
            'locale': 'es'
        }
    )
])


if __name__ == '__main__':
    app.run(debug=True)
