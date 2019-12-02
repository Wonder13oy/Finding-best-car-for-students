import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

df = pd.read_csv('../dataset/car_prices.csv')

app = dash.Dash()
features = df.columns

year_options = []
for year in df.sort_values('year').year.unique():
    year_options.append({'label': str(year), 'value':year})

# HTML PAGE
app.title = 'Used Cars Dashboard'
app.layout = html.Div([
    html.Div([
        html.H1('Price of cars over the years'),
        html.P('Select a year'),
        dcc.Dropdown(
            id='year-picker',
            options=year_options,
            value=df.year.max()
        ),
        dcc.Graph(id='graph')
    ]),
    html.Div([
        html.H1('Manual comparer'),
        html.Div([
            html.P('X axis'),
            dcc.Dropdown(
                id='xaxis',
                options=[{'label': i, 'value': i} for i in features],
                value='year'
            )
        ],style={'width':'48%', 'display':'inline-block'}),
        html.Div([
            html.P('Y axis'),
            dcc.Dropdown(
                id='yaxis',
                options=[{'label': i, 'value': i} for i in features],
                value='price'
            )
        ],style={'width':'48%', 'display':'inline-block'}),
        dcc.Graph(id='feature-graphic')
    ],style={'padding': 10}),
    html.Div([
        html.H1('Top Ten cars'),
        html.Div([
            html.P('Sort by'),
            dcc.Dropdown(
                id='top-yaxis',
                options=[{'label': i, 'value': i} for i in ['mileage', 'price', 'fee per month']],
                value='mileage'
            )
        ],style={'width':'48%', 'display':'inline-block'}),
        html.Div([
            html.P('What to measure'),
            dcc.Dropdown(
                id='return-top',
                options=[{'label': i, 'value': i} for i in ['price', 'mileage']],
                value='mileage'
            )
        ],style={'width':'48%', 'display':'inline-block'}),
        html.Div([
            html.P('Range:'),
            dcc.Slider(
                id='top-number',
                min=5,
                max=15,
                step=5,
                marks={
                    5: '5',
                    10: '10',
                    15: '15',
                },
                value=10,
            )
        ],style={'width':'48%', 'display':'inline-block', 'padding': 5}),
        html.Div([
            dcc.RadioItems(
                id='min_or_max',
                options=[{'label': i, 'value': i} for i in ['smallest', 'largest']],
                value='largest'
            )
        ],style={'width':'48%', 'display':'inline-block'}),
        dcc.Graph(id='top-graph')
    ]),
    html.Div([
        html.H1('Average price of each car over the years'),
        html.Div([
            html.P('Select a brand'),
            dcc.Dropdown(
                id='avg-brands',
                options=[{'label': i, 'value': i} for i in df.sort_values('brand').brand.unique()],
                value='AUDI'
            )
        ]),
        dcc.Graph(id='avg-graph')
    ])
],style={'width':'100%', 'height': '100vh','display':'grid', 'grid-template-columns': '1fr 1fr'})

# SINGLE INPUTS
@app.callback(
    Output('graph', 'figure'),
    [Input('year-picker', 'value')]
)
def update_fig(selected_year):

    # DATA ONLY FOR SELECTED YEAR FROM DROPDOWN
    filtered_df = df[df.year == selected_year]

    trace=[]
    for car_brand in filtered_df.brand.unique():
        df_by_cars = filtered_df[filtered_df.brand == car_brand]
        trace.append(go.Scatter(
            x = df_by_cars.mileage,
            y = df_by_cars.price,
            mode='markers',
            opacity=0.7,
            marker = {'size': 15},
            name=car_brand
        ))

    return {
        'data': trace,
        'layout': go.Layout(
            title='Mileage vs Price',
            xaxis={
                'title': 'Mileage in KM',
                'type': 'log'
            },
            yaxis={
                'title': 'Price in Rands'
            }
        )
    }

# MULTIPLE OUTPUTS

@app.callback(
    Output('feature-graphic', 'figure'),
    [
        Input('xaxis', 'value'),
        Input('yaxis', 'value')
    ]
)
def update_graph(x_name, y_name):

    scat_graph = [
        go.Scatter(
            x=df[x_name],
            y=df[y_name],
            text=df.brand,
            mode='markers',
            marker={
                'size':15,
                'opacity': 0.5,
                'line':{
                    'width':0.5,
                    'color': 'white'
                }
            }
        )
    ]

    return {
        'data': scat_graph,
        'layout': go.Layout(
            title=f'{x_name} vs {y_name}',
            xaxis={'title': x_name},
            yaxis={'title': y_name},
            hovermode='closest'
        )
    }

@app.callback(
    Output('top-graph', 'figure'),
    [
        Input('return-top', 'value'),
        Input('top-yaxis', 'value'),
        Input('top-number', 'value'),
        Input('min_or_max', 'value')
    ]
)
def update_top_ten(comparer, measure, range, max_min):

    if max_min == 'largest':
        new_df = df.nlargest(range, measure)
    else:
        new_df = df.nsmallest(range, measure)

    bar_graph = [
        go.Bar(
            x=new_df.brand.unique(),
            y=new_df[comparer]
        )
    ]

    return {
        'data': bar_graph,
        'layout': go.Layout(
            title=f'Top {range} cars with the {max_min} {comparer}',
            xaxis={'title': 'car brands'},
            yaxis={'title': comparer},
        )
    }

@app.callback(
    Output('avg-graph', 'figure'),
    [Input('avg-brands', 'value')]
)
def update_avg_graph(car_name):
    cars = df[df.brand == car_name].sort_values('year')

    sums = []
    avgs = []

    for year in cars.year:
        y = np.average(cars[cars.year == year].price)
        avgs.append(y)

    line_graph = [
        go.Scatter(
            x=cars.year,
            y=avgs,
            marker={
                'size':15,
                'symbol': 'circle',
                'line':{
                    'width':0.5,
                    'color': 'white'
                }
            }
        )
    ]
    return {
        'data': line_graph,
        'layout': go.Layout(
            title=f'Average price of {car_name} over the years',
            xaxis={'title': 'Years'},
            yaxis={'title': 'Average Price'},
        )
    }

if __name__ == '__main__':
    app.run_server();
