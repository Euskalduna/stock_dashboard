import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd

app = dash.Dash(__name__)

# Sample data for the DataTable
data = {
    'Column 1 with a very long header title': ['Short content', 'Another short one'],
    'Column 2': ['Content that is long and needs to wrap around.', 'More content that is also quite long to test the wrapping feature.'],
    'Column 3': ['Short', 'VeryLongWordThatMightNotWrapProperlyWithoutSpaces']
}
df = pd.DataFrame(data)

app.layout = html.Div([
    html.H1("Datatable with Dynamic Column Width and Text Wrapping"),
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
        style_cell={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 150, # Adjust this value as the threshold for wrapping
            'whiteSpace': 'normal' # This allows text to wrap
        },
        style_header={
            'whiteSpace': 'normal',
            'height': 'auto',
            'fontWeight': 'bold'
        },
        # Auto-width based on content (header or body)
        style_data_conditional=[
            {
                'if': {'column_id': col},
                'minWidth': '100px',  # Minimum width
                'width': 'auto',
                'maxWidth': '300px', # Maximum width before wrapping
            } for col in df.columns
        ]
    ),
    html.Div(id='datatable-interactivity-container')
])

@app.callback(
    Output('datatable-interactivity-container', 'children'),
    Input('datatable-interactivity', 'data'),
    Input('datatable-interactivity', 'columns'))
def display_output(rows, columns):
    if rows:
        return html.Div([
            html.H3('Selected Data'),
            dash_table.DataTable(
                data=rows,
                columns=[{"name": i, "id": i} for i in columns]
            )
        ])

if __name__ == '__main__':
    app.run_server(debug=True)