import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

#importing the engineered_data

data = pd.read_csv("/Users/antwnhsvellopoulos/Desktop/GitHub/supply_chain_dashboard/data/engineered_data")

def month_sorter(column):
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    correspondence = {month: order for order, month in enumerate(months)}
    return column.map(correspondence)

def total_profit_kpi(category,year,data = data):
    data = data[data['Category Name'].isin(category)]
    data = data[data['Year'] == year]
    fig = go.Figure()
    fig.add_trace( go.Indicator(
    mode = "number",
    value = sum(data['Order Profit Per Order']),
    number = {'prefix': "$"},
    title = {"text": "<span style='font-size:2em;color:white'>profit earned</span>"},
    domain = {'x': [1, 1], 'y': [0, 1]}))
    
    fig.update_layout( 
                        uniformtext_minsize=12,
                        paper_bgcolor='rgb(105,105,105)',
                        uniformtext_mode='hide',
                        font = dict(color = 'pink', family = "Arial"),
                        )
               
    return fig



line_fig = go.Figure()
year = data['Year'].unique().tolist()
for year, color in zip(sorted(year), px.colors.sequential.PuBu):
    fig_data = data[(data['Year'] == year)].groupby(by = ['Month']).sum().sort_values(by = 'Month', key = month_sorter).reset_index()
    line_fig.add_trace(go.Scatter(
        x = fig_data['Month'],
        y = fig_data['Order Profit Per Order'],
        name = year,
        marker_color = color,
        
        ))
line_fig.update_layout( title=" Total Profit per month per year",
                xaxis_title="Months",
                yaxis_title="Profit ($)",
                uniformtext_minsize=12,
                paper_bgcolor='rgb(105,105,105)',
                plot_bgcolor='rgb(105,105,105)',
                uniformtext_mode='hide',
                font = dict(color = 'white', family = "Arial")
                )



def bar_total_profits(category, year ,data = data):
    fig = go.Figure()
    data = data[data['Category Name'].isin(category)]
    continents = ['Oceania', 'Africa', 'Europe','Asia','USA']
    for cont, color in zip(continents, px.colors.sequential.PuBu):
        fig_data  = data[(data['Year'] == year) & (data['continent'] == cont)].groupby(by = ['Month']).sum().sort_values(by = 'Month', key = month_sorter).reset_index()
        fig.add_trace(go.Bar(
            x = fig_data['Month'],
            y = fig_data['Order Profit Per Order'],
            name = cont,
            marker_color = color,
            width = 0.2))
        
    fig.update_traces( marker_line_color='rgb(8,48,107)',
                       marker_line_width=1.5, opacity=0.6)    
        
    fig.update_layout(barmode='group', xaxis_tickangle=-45)

    fig.update_layout( title="Total profits per month per continent",
                    xaxis_title="Months",
                    yaxis_title="Profit ($)",
                    uniformtext_minsize=12,
                    paper_bgcolor='rgb(105,105,105)',
                    plot_bgcolor='rgb(105,105,105)',
                    uniformtext_mode='hide',
                    font = dict(color = 'white', family = "Arial"),
                    bargap= 0.3
                    
                    )
    return fig

def category_pie(year, data=data): 
    fig_data  = data[data['Year']== year].groupby(by = 'Category Name').count().sort_values(by = 'Type').reset_index().head(5)
    fig_data['units sold per category'] = fig_data['Type']
    fig = px.pie(fig_data, values='units sold per category', names='Category Name', color_discrete_sequence=px.colors.sequential.PuBu,
                    hole = 0.7)  
    fig.update_traces(textposition='outside')
    fig.update_layout(title= " Top five categories in sales",
                           uniformtext_minsize=12,
                           paper_bgcolor='rgb(105,105,105)',
                           uniformtext_mode='hide',
                           font = dict(color = 'white', family = "Arial"),
                           showlegend = False)
    return fig








app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background": "rgb(208,209,230)"
    }



CONTENT_STYLE = {
    "margin-left": "16rem",
    "margin-right": "10rem",
    "padding": "3rem 3rem",
    "background": "rgb(56,56,56)"
}

sidebar = html.Div(
    [
        html.H2("Menu", className="display-4"),
        html.Hr(),
        html.P(
            "please select the year and the category that you want to preview", className="lead"
        ),
        html.H3("Year selection", className="display-6"),
        dcc.Dropdown(
            id = "year-dropdown",
            options =[{'label':i, 'value':i} for i in data['Year'].unique().tolist()],
            value = 2016
            ),
        html.H3("Category selection", className="display-6"),
        dcc.Dropdown(
            id = "category-dropdown",
            options =[{'label':i, 'value':i} for i in data['Category Name'].unique().tolist()],
            value = ['Garden'],
            multi = True 
            ),
    ],
    style=SIDEBAR_STYLE,
)

app.layout = html.Div([dcc.Location(id="url"), sidebar, dbc.Container(
    [
        dbc.Row(dbc.Col(html.H2('SALES OVERVIEW', className='text-center text-primary, mb-3'))),  # header row
        
        dbc.Row([  # start of second row

            dbc.Col([  # first column on second row
            
            dcc.Graph(id='line-fig',
                      figure = line_fig,
                      style={'height':380}),
            
            html.Hr(),

            ], width={'size': 6, 'offset': 0, 'order': 1}),  # width first column on second row

            dbc.Col([  # second column on second row
            
            dcc.Graph(id='total-profit-kpi',
                              style={'height':380}),
            html.Hr()

            ], width={'size': 3, 'offset': 0, 'order': 2}),  # width second column on second row

            dbc.Col([  # third column on second row
            

            html.Hr()

            ], width={'size': 3, 'offset': 0, 'order': 3}),  # width third column on second row
        ]),  # end of second row
        
        dbc.Row([  # start of third row
            dbc.Col([  # first column on third row
                
                dcc.Graph(id ="bar-total-profits",
                            style = {'height':380})
    
            ], width={'size': 6, 'offset': 0, 'order': 1}),  # width first column on second row

            dbc.Col([  # second column on third row
                
                dcc.Graph(id = "pie-chart",
                            style={'height':380} )
                
            ], width={'size': 4, 'offset': 0, 'order': 2}),  # width second column on second row
        ])  # end of third row
        
    ], fluid=True, style=CONTENT_STYLE) 

])

@app.callback(Output("total-profit-kpi", 'figure'),
             [Input('category-dropdown', 'value')],
             [Input('year-dropdown', 'value')])
def update_output(category,year):
    return total_profit_kpi(category,year)

@app.callback(Output("bar-total-profits", 'figure'),
             [Input('category-dropdown', 'value')],
             [Input('year-dropdown', 'value')])
def update_bar(category,year):
     return bar_total_profits(category, year)

@app.callback(Output("pie-chart", 'figure'),
             [Input('year-dropdown', 'value')])
def update_bar(year):
    return category_pie(year)

if __name__ == "__main__":
    app.run_server(port=8888)