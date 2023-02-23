import requests
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


url_loc = "https://proxy.royaleapi.dev/v1/locations"
headers = {"Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjBkYzgzNzY1LWYxNWMtNGRmZC1iOWNlLTQ0N2E3Y2E3YmMzMyIsImlhdCI6MTY3Njg1NDI3Miwic3ViIjoiZGV2ZWxvcGVyLzQxMzk1MjcwLTJiMjUtM2RkMC1mYzhlLWYwODQ1YTI3OWZiMCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI0NS43OS4yMTguNzkiXSwidHlwZSI6ImNsaWVudCJ9XX0.aV7JV24ZUQf0atHnLlE0jb3hf7otXKmcHuH8W0fs8MynipdseURVCEknzcIU2PjhHztJ0_yta0m87m5In0601Q"}

response = requests.get(url_loc, headers=headers)

locations_clash = pd.json_normalize(response.json()["items"])
locations_clash_countr = locations_clash[locations_clash["isCountry"] == True].reset_index(drop=True)

all_clans = pd.DataFrame()

for i in locations_clash_countr["id"]:
    url_clan_info = "https://proxy.royaleapi.dev/v1/locations/"+str(i)+"/rankings/clans?limit=100"
    response = requests.get(url_clan_info, headers=headers)
    clan_info = pd.json_normalize(response.json()["items"])
    all_clans = pd.concat([all_clans,clan_info])

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1("Top 10 clans by country",
                                style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                html.Div(["Input Country's Name", dcc.Input(id="input-country",value=" ",type="text",
                                style={'height':'50px','font-size':35}),],
                                style={'font-size':40}),
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id="top10-table")),
                                ])

# add callback decorator

@app.callback(Output(component_id='top10-table',component_property='figure'),\
    Input(component_id='input-country',component_property='value'))

def top10clans(country):
    all_clans["location.name"] = all_clans["location.name"].str.lower()
    country = country.lower()
    all_clans_filtered = all_clans[all_clans["location.name"]==country].head(10)
    fig = go.Figure(data=[go.Table(header=dict(values=["tag","name","clanScore"]),
                 cells=dict(values=[all_clans_filtered["tag"],
                 all_clans_filtered["name"],
                 all_clans_filtered["clanScore"]]))])
    
    fig.update_layout(title="Top 10 clans in "+str(country))
    return fig

#Run the app
if __name__ == '__main__':
    app.run_server()


