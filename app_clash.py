# Here we are going to do a simple request using the Clash Royale API to retrieve info about the top 10 clans in all the 
# countries in which there are teams registered.

# The call will give us info for one country at a time. Though I could retreieve info for all countries at once, 
# that would be to much info to display at once in a single table. Instead, we are going to input the country in 
# which we are interested first and, then, the app will output the info about that location.

# Also, by the end, we are going to configure a simple dash app, which will display the info we have scripted. 
# A user friendly solution to retrieve the info about the clans for the non-tech user.

#### First. Import Modules.
#These are the packages we are going to need to make our script work. 

import requests
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

#########

#Second. First API Call
#Get all possible locations in CLash Royale.


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

all_clans["location.name"] = all_clans["location.name"].str.lower()

def availability(df):
    available_clans = df[(df["members"]<50)]
    return available_clans

# def top_clans(all_clans):
#     all_clans_filtered = all_clans[(all_clans["location.name"]==country)].head(10)
#     return all_clans_filtered



app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1("Top 10 clans by country",
                                style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                html.Div(["Input Country's Name",
                                dcc.Dropdown(id="input-country",
                                          options=locations_clash_countr["name"].tolist(),
                                          value=" ",
                                          placeholder = "Select a Country",
                                style={'height':'50px','font-size':35}),],
                                style={'font-size':40}),
                                html.Div(["Check for clans with less than 50 members",
                                dcc.Dropdown(id="input-members",
                                            options=[{'label':'YES','value':'YES'},
                                                        {'label':'NO','value':'NO'}],
                                            value=['YES']),
    
                                ]
                                ),
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id="top10-table")),
                                html.Div(id="test"),
                                ])

# add callback decorator

@app.callback([Output(component_id='top10-table',component_property='figure'),
               Output(component_id='test',component_property='children')],
    [
    Input(component_id='input-country',component_property='value'),
     Input(component_id='input-members',component_property='value')]
    )

def top10clans(country,members):
    country = country.lower()

    df = all_clans[(all_clans["location.name"]==country)]

    if members == 'YES':
        available_clans_filtered = availability(df).head(15)
        fig_available = go.Figure(data=[go.Table(header=dict(values=["tag","name","clanScore","members"]),
                    cells=dict(values=[available_clans_filtered["tag"],
                    available_clans_filtered["name"],
                    available_clans_filtered["clanScore"],
                    available_clans_filtered["members"]]))])
        fig_available.update_layout(title="Top 10 clans in "+str(country))

        return [fig_available,members]
    else:
        df = df.head(15)
        fig_all = go.Figure(data=[go.Table(header=dict(values=["tag","name","clanScore","members"]),
                    cells=dict(values=[df["tag"],
                    df["name"],
                    df["clanScore"],
                    df["members"]]))])
        fig_all.update_layout(title="Top 10 clans in "+str(country))
        return [fig_all,members]



#Run the app
if __name__ == '__main__':
    app.run_server()


