

import requests
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

#########

numbers = pd.DataFrame({"numbers":["YES","YES","YES","NO","NO"]})


app = dash.Dash(__name__)

app.layout = html.Div(children=[
                                html.Div(["Check for clans with less than 50 members",
                                          dcc.Checklist(id="input-members",
                                                        options=[{'label':"YES",'value':"YES"},
                                                                 {'label':"NO",'value':"NO"}],
                                                        value=["YES"]),
    
                                ]
                                ),
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id="test")),
                                ])

# add callback decorator

@app.callback(Output(component_id='test',component_property='figure'),\
    [
     Input(component_id='input-members',component_property='value')]
    )

def func(members):
        numbers_filt = numbers[numbers["numbers"].isin(members)]
        fig = go.Figure(data=[go.Table(header=dict(values=["numbers"]),
                 cells=dict(values=[numbers_filt["numbers"]]))])
        return fig

#Run the app
if __name__ == '__main__':
    app.run_server()

