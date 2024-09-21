# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Read the airline data into the pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})
# Create a dash application
app = dash.Dash(__name__)
                               
app.layout = html.Div(children=[ html.H1('Airline Performance Dashboard',style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}), #title head and its style
                                html.Div(["Input Year: ", dcc.Input(id='input-year', value='2010', #input component(string and the input id, default value is 2010)
                                type='number', style={'height':'50px', 'font-size': 35}),], #type of input is number, # set height and font size of the drop down text
                                style={'font-size': 40}), #set style of the whole inputting inner division(div)
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id='line-plot')), #add a id='line-plot' div from the dash core component memory
                                ])

# add callback decorator
@app.callback( Output(component_id='line-plot', component_property='figure'), #call back: when input is made, adjust the output
               Input(component_id='input-year', component_property='value'))

# Add computation to callback function and return graph
def get_graph(entered_year): #this will use input from call back and send output to callback
    # Select 2019 data
    df =  airline_data[airline_data['Year']==int(entered_year)] #extract info based on the input
    
    # Group the data by Month and compute average over arrival delay time.
    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index() #group by month and then calculate the mean of column: ArrDelay

    fig = go.Figure(data=go.Scatter(x=line_data['Month'], y=line_data['ArrDelay'], mode='lines', marker=dict(color='green'))) #use plotly.graph_object
    fig.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()