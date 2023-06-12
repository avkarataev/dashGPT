import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, dash_table

# Load the data from the provided CSV file
df = pd.read_csv('https://raw.githubusercontent.com/tatyskya/dataset_for_ChatGPT/main/2018.csv')

# Create the list of country options for the dropdown filter
country_options = [{'label': country, 'value': country} for country in df['Country or region'].unique()]

# Create the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(
    children=[
        html.H1('Happiness Score by Country or Region'),

        html.H2('Filter by Country'),

        dcc.Dropdown(
            id='country-dropdown',
            options=country_options,
            value=[],
            multi=True
        ),

        dcc.Graph(
            id='choropleth-map',
            figure=px.choropleth(
                df,
                locations='Country or region',
                locationmode='country names',
                color='Score',
                color_continuous_scale='Viridis',
                range_color=(df['Score'].min(), df['Score'].max()),
                labels={'Score': 'Happiness Score'}
            )
        ),

        html.H2('Top 10 Countries or Regions Bar Chart'),

        dcc.Graph(id='bar-chart'),

        html.H2('Top 10 Countries or Regions Table'),

        dash_table.DataTable(
            id='table',
            columns=[{'name': col, 'id': col} for col in df.columns],
            data=df.to_dict('records')
        )
    ]
)


# Define callback function to update the bar chart and table based on the dropdown selection
@app.callback(
    [dash.dependencies.Output('bar-chart', 'figure'),
     dash.dependencies.Output('table', 'data'),
     dash.dependencies.Output('choropleth-map', 'figure')],
    [dash.dependencies.Input('country-dropdown', 'value')]
)
def update_data(selected_countries):
    if selected_countries:
        filtered_df = df[df['Country or region'].isin(selected_countries)]
        top_10_countries = filtered_df.nlargest(10, 'Score')

        bar_chart_figure = px.bar(top_10_countries, x='Score', y='Country or region', orientation='h')
        updated_data = top_10_countries.to_dict('records')

        choropleth_map_figure = px.choropleth(
            filtered_df,
            locations='Country or region',
            locationmode='country names',
            color='Score',
            color_continuous_scale='Viridis',
            range_color=(filtered_df['Score'].min(), filtered_df['Score'].max()),
            labels={'Score': 'Happiness Score'}
        )
    else:
        top_10_countries = df.nlargest(10, 'Score')

        bar_chart_figure = px.bar(top_10_countries, x='Score', y='Country or region', orientation='h')
        updated_data = top_10_countries.to_dict('records')

        choropleth_map_figure = px.choropleth(
            df,
            locations='Country or region',
            locationmode='country names',
            color='Score',
            color_continuous_scale='Viridis',
            range_color=(df['Score'].min(), df['Score'].max()),
            labels={'Score': 'Happiness Score'}
        )

    return bar_chart_figure, updated_data, choropleth_map_figure


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
