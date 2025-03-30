import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H3("Checklist with Text Visibility"),
    dcc.Checklist(
        id='text-checklist',
        options=[
            {'label': 'Text 1', 'value': 'text1'},
            {'label': 'Text 2', 'value': 'text2'},
            {'label': 'Text 3', 'value': 'text3'}
        ],
        value=[]  # Initial values (all unchecked)
    ),
    html.Div(id='text-container')
])

@app.callback(
    Output('text-container', 'children'),
    [Input('text-checklist', 'value')]
)
def update_text(selected_values):
    texts = {
        'text1': html.P("This is Text 1."),
        'text2': html.P("This is Text 2."),
        'text3': html.P("This is Text 3.")
    }
    displayed_texts = [texts[value] for value in selected_values]
    return displayed_texts

if __name__ == '__main__':
    app.run_server(debug=True)