#!/usr/bin/env python
# coding: utf-8

import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': '...........', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': '.........'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div(children=[
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 24}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {"label": "Yearly Statistics", "value": "Yearly Statistics"},
                {"label": "Recession Period Statistics", "value": "Recession Period Statistics"},
            ],
            value='Select Statistics',
            placeholder='Select a report type',
            style={
                'width': '80%',
                'padding': '3px',
                'font-size': '20px',
                'text-align-last': 'center'
            }
        )
    ]),
    html.Div(
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='Select year',
            placeholder='Select year',
        )),
    html.Div([
        html.Div(
            id='output-container', 
            className='chart-grid', 
            style={'display': 'flex'}),
            ])
])

# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True

# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), 
    Input(component_id='select-year', component_property='value')])


def update_output_container(report_type, input_year):
    if report_type == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
#Create and display graphs for Recession Report Statistics

#Plot 1 Automobile sales fluctuate over Recession Period (year wise)

        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"))

#Plot 2 Calculate the average number of vehicles sold by vehicle type       

        average_sales = recession_data.groupby("Vehicle_Type")['Automobile_Sales'].mean().reset_index()        
        R_chart2  = dcc.Graph(
            figure=px.bar(average_sales,
            x='Vehicle_Type',
            y='Automobile_Sales',
            title="Average Number of Vehicles sold by Vehicle Type"))
        
#Plot 3 Pie chart for total expenditure share by vehicle type during recessions

        exp_rec= recession_data.groupby("Vehicle_Type")['Advertising_Expenditure'].mean().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
            values='Advertising_Expenditure',
            names='Vehicle_Type',
            title="Total Advertising Expenditure by Vehicle Type during Recession"))

# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales

        unemp_data = recession_data.groupby(["unemployment_rate","Vehicle_Type"])['Automobile_Sales'].mean().reset_index() 
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data,
            x='unemployment_rate',
            y='Automobile_Sales',
            labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
            color="Vehicle_Type",
            title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [
            html.Div( 
                className='chart-container',
                children=[
                    html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)]),
                    html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)])
                ],
                style={'display': 'flex', 'flex-wrap': 'wrap'} 
            )
        ]

# Create and display graphs for Yearly Report Statistics

    elif (input_year and report_type =='Yearly Statistics'):
        yearly_data = data[data['Year'] == input_year]
                              
#Plot 1 Yearly Automobile sales using line chart for the whole period.

        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, 
                x='Year',
                y='Automobile_Sales',
                title=f"Yearly Automobile Sales"))
            
#Plot 2 Total Monthly Automobile sales using line chart.

        mas=yearly_data.groupby("Month")['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas,
            x='Month',
            y='Automobile_Sales',
            title='Total Monthly Automobile Sales in the year {}'.format(input_year)))

  # Plot bar chart for average number of vehicles sold during the given year

        avr_vdata=yearly_data.groupby(["Vehicle_Type"])['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata,
                x="Vehicle_Type",
                y="Automobile_Sales",
                labels={'Vehicle_Type': 'Vehicle Type', 'Automobile_Sales': 'Average Automobile Sales'},
                title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year))
            ),

    # Total Advertisement Expenditure for each vehicle using pie chart

        exp_data=yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data,
            values="Advertising_Expenditure",
            names='Vehicle_Type',
            title="Total Advertising Expenditure by Vehicle Type in the year {}".format(input_year)
            ))

#Returning the graphs for displaying Yearly data
        return [
            html.Div( 
                className='chart-container',  # Add a class for easier styling
                children=[
                    html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)]),
                    html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)])
                ],
                style={'display': 'flex', 'flex-wrap': 'wrap'}  # Apply flexbox to the container
            )
        ]

    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

