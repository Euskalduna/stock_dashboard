import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

app = dash.Dash(__name__)

# Sample data for the pie chart
data = {'labels': ['Category A', 'Category B', 'Category C'],
        'values': [30, 45, 25]}

# Create the pie chart figure
fig = px.pie(data, values='values', names='labels')

# Update the hovertemplate for larger pop-ups
fig.update_traces(hovertemplate='<b>%{label}</b> (%{percent}) <br> Dinero(EUR): %{value}')

# Update the layout to position the legend and increase hoverinfo font size
fig.update_layout(
    legend=dict(x=1, y=0.5),  # Adjust x and y values as needed
    hoverlabel=dict(font_size=16)  # Adjust font size as desired
)

app.layout = html.Div(children=[
    html.H1(children="Pie Chart with Larger Hover Pop-ups"),
    dcc.Graph(id='pie-chart', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)

