import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_pivottable
import pandas as pd
import random
from datetime import datetime, timedelta

# Initialize the Dash app
app = dash.Dash(__name__)


# --- Step 2: Prepare Your Data ---
# Create some sample data that matches your described structure
# (Year, Month, Complete Date) for rows and (Country, Stock Market, Company) for columns.
def generate_sample_data(num_records=1000):
    """Generates a sample DataFrame for the pivot table."""
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    countries = ['USA', 'UK', 'Germany', 'Japan']
    stock_markets = {
        'USA': ['NASDAQ', 'NYSE'],
        'UK': ['LSE'],
        'Germany': ['FWB'],
        'Japan': ['TSE']
    }
    companies = ['Apple', 'Microsoft', 'Tesla', 'Unilever', 'Siemens', 'Toyota']

    for _ in range(num_records):
        date = start_date + timedelta(days=random.randint(0, 365))
        country = random.choice(countries)
        stock_market = random.choice(stock_markets[country])
        company = random.choice(companies)

        data.append({
            'Year': date.year,
            'Month': date.strftime('%B'),
            'Complete Date': date.strftime('%Y-%m-%d'),
            'Country': country,
            'Stock Market': stock_market,
            'Company': company,
            'Revenue': random.randint(100, 1000)
        })
    return pd.DataFrame(data)


# Generate the DataFrame
df = generate_sample_data()

# --- Step 3: Configure the PivotTable Component ---
app.layout = html.Div(style={'fontFamily': 'sans-serif', 'padding': '20px'}, children=[
    html.H1("Dynamic Pivot Table Tutorial", style={'textAlign': 'center', 'color': '#333'}),
    html.P("This table is powered by dash-pivottable. Drag and drop the fields to explore the data.",
           style={'marginBottom': '20px'}),

    dash_pivottable.PivotTable(
        id='my-pivot-table',
        data=df.to_dict('records'),  # Data must be a list of dictionaries

        # Initial hierarchical row and column configuration
        rows=['Year', 'Month'],
        cols=['Country', 'Stock Market'],

        # The value to be aggregated
        vals=['Revenue'],
        aggregatorName='Sum',

        # Initial rendering mode
        rendererName='Table'
    ),

    # This div will display the JSON output of the table's state
    html.Div([
        html.H3("Pivot Table State (JSON):", style={'marginTop': '40px', 'color': '#555'}),
        dcc.Loading(
            id="loading-output",
            type="default",
            children=html.Pre(id='pivot-output',
                              style={'border': '1px solid #ccc', 'padding': '10px', 'backgroundColor': '#f9f9f9',
                                     'whiteSpace': 'pre-wrap', 'wordWrap': 'break-word'})
        )
    ])
])


# --- Step 4: Create a Callback to Capture the State ---
@app.callback(
    Output('pivot-output', 'children'),
    [
        Input('my-pivot-table', 'data'),
        Input('my-pivot-table', 'rows'),
        Input('my-pivot-table', 'cols'),
        Input('my-pivot-table', 'vals'),
        Input('my-pivot-table', 'aggregatorName')
    ]
)
def update_pivot_output(data, rows, cols, vals, aggregator_name):
    # This callback is triggered whenever the user changes the table configuration.
    # It returns a JSON string of the current state for demonstration.
    state = {
        'number_of_data_rows': len(data),
        'current_rows': rows,
        'current_cols': cols,
        'current_vals': vals,
        'current_aggregator': aggregator_name
    }
    return str(state)


if __name__ == '__main__':
    app.run(debug=True)
