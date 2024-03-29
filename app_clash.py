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
    url_clan_info = "https://proxy.royaleapi.dev/v1/locations/"+str(i)+"/rankings/clans?limit=120"
    response = requests.get(url_clan_info, headers=headers)
    clan_info = pd.json_normalize(response.json()["items"])
    all_clans = pd.concat([all_clans,clan_info])

#all_clans["location.name"] = all_clans["location.name"].str.lower()

def availability(df):
    available_clans = df[(df["members"]<50)]
    return available_clans

# def top_clans(all_clans):
#     all_clans_filtered = all_clans[(all_clans["location.name"]==country)].head(10)
#     return all_clans_filtered



app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([html.Img(src=app.get_asset_url('clashroyale.png'),
                                         style={'max-width':'40%','height':'auto','margin-left':'auto','margin-right':'auto',
                                                'display': 'block'}),
                            html.Div([
                                 html.Div([html.Br(),
                                           html.Br(),
                                           html.Br(),
                                           html.Br(),
                                           html.H2("Input Country's Name",
                                                    style={'textAlign': 'left', 'color': '#FFFFFF',
                                                        'font-family': 'Arial','font-size': '1vw',
                                                        'padding':'10px'}),

                                            dcc.Dropdown(id="input-country",
                                                    options=[{'label':html.Span(i,
                                                                               style={'color':'black','font-size': '1vw'}),
                                                             'value':i}
                                                             for i in locations_clash_countr["name"].tolist()],
                                                    value=" ",
                                                    placeholder = "Select a Country"),

                                            html.H2("Check for Available Clans",
                                                    style={'textAlign': 'left', 'color': '#FFFFFF',
                                                        'font-family': 'Arial','font-size': '1vw',
                                                        'padding':'10px'}),

                                            dcc.Dropdown(id="input-members",
                                                    options=[{'label': html.Span('<50 members',style={'color':'black','font-size': '1vw'}),'value':'YES'},
                                                            {'label':html.Span('ALL',style={'color':'black','font-size': '1vw'}),'value':'NO'}],
                                                    placeholder = "Select an Option"),
                                            
                                            html.H2("Pick List's Length",
                                            style={'textAlign': 'left', 'color': '#FFFFFF',
                                                'font-family': 'Arial','font-size': '1vw',
                                                'padding':'10px'}),

                                            dcc.Dropdown(id="input-number",
                                                    options=[{'label': html.Span('10',style={'color':'black','font-size': '1vw'}),'value':10},
                                                            {'label':html.Span('20',style={'color':'black','font-size': '1vw'}),'value':20},
                                                            {'label':html.Span('50',style={'color':'black','font-size': '1vw'}),'value':50},
                                                            {'label':html.Span('100',style={'color':'black','font-size': '1vw'}),'value':100}],
                                                    placeholder = "Select an Option")],
                                                    style={'width':'30%',
                                                           'height':'1px',
                                                           'padding':'12px'}),

                                html.Div([html.Div(id="country-selected",
                                                    style={'textAlign': 'left', 'color': '#FFFFFF',
                                                        'font-family': 'Arial','font-size': '2vw',
                                                        'padding':'10px'}),
                                          dcc.Graph(id="top10-table",responsive=True,
                                                    style={'height':'85vh'}),
                                          html.Br()],
                                         style={'width':'70%',
                                                'display':'block'})],
                                
                            style={'display':'flex'})],
                        style={'background-image':'url('+app.get_asset_url('fondo_app_cr.jpg')+')',
                            'background-size':'cover',
                            'background-position': 'center center',
                            'background-attachment': 'fixed',
                            'width':'95%'})

# add callback decorator

@app.callback([Output(component_id='country-selected',component_property='children'),
               Output(component_id='top10-table',component_property='figure')],
    [
    Input(component_id='input-country',component_property='value'),
     Input(component_id='input-members',component_property='value'),
     Input(component_id='input-number',component_property='value')]
    )

def top10clans(country,members,number):
    #country = country.lower()

    df = all_clans[(all_clans["location.name"]==country)]

    country_pick = "Top clans in "+str(country)

    if members == 'YES':
        available_clans_filtered = availability(df).head(number)
        fig_available = go.Figure(data=[go.Table(header=dict(values=["tag","name","clanScore","members"]),
                    cells=dict(values=[available_clans_filtered["tag"],
                    available_clans_filtered["name"],
                    available_clans_filtered["clanScore"],
                    available_clans_filtered["members"]]))],
                    layout = go.Layout(height=200,
                                       margin=dict(
                                                    l=50,
                                                    r=50,
                                                    b=100,
                                                    t=20,
                                                    pad=4
                                                )
                                       ))
        #fig_available.update_layout(title="Top clans in "+str(country),title_font_family="Arial")
        fig_available.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)'})
        fig_available.update_layout(template="none")

        

        return [country_pick,fig_available]
    else:
        df = df.head(number)
        fig_all = go.Figure(data=[go.Table(header=dict(values=["tag","name","clanScore","members"]),
                    cells=dict(values=[df["tag"],
                    df["name"],
                    df["clanScore"],
                    df["members"]]))],
                    layout = go.Layout(height=500,
                                       margin=dict(
                                                    l=50,
                                                    r=50,
                                                    b=100,
                                                    t=20,
                                                    pad=4
                                                )
                                       ))
       # fig_all.update_layout(title="Top clans in "+str(country),title_font_family="Arial")
        fig_all.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)'})
        fig_all.update_layout(template="none")


        return [country_pick,fig_all]



#Run the app
if __name__ == '__main__':
    app.run_server()


