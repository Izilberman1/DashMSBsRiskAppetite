#-------------------------------------------------------
mapbox_access_token = 'NotForYou'

import pandas as pd
import numpy as np
import dash                     #(version 1.0.0)
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.offline as py     #(version 4.4.1)
import plotly.graph_objs as go

df = pd.read_excel(r"C:\Users\16476\Desktop\Itamar's Folder\BCIA Class Notes\RSC885 Capstone Project\20230309_OntarioMSBsAnalysis_IZ.xlsx")

app = dash.Dash(__name__)

blackbold={'color':'black', 'font-weight': 'bold'}

app.layout = html.Div([
#---------------------------------------------------------------
# Map_legend + Jurisdiction_checklist + Status_type_checklist + Activities_checklist + Name + Map
    html.Div([
        html.Div([
            # Map-legend
            html.Ul([
                html.Li("Ceased", className='circle', style={'background': '#ffcc66','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li("Expired", className='circle', style={'background': '#33ccff','color':'black',
                    'list-style':'none','text-indent': '17px','white-space':'nowrap'}),
                html.Li("Registered", className='circle', style={'background': '#99ff99','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li("Revoked", className='circle', style={'background': '#ff9999','color':'black',
                    'list-style':'none','text-indent': '17px'}),
            ], style={'border-bottom': 'solid 3px', 'border-color':'#003366','padding-top': '6px'}
            ),

            # Status_type
            html.Label(children=['MSB Status: '], style=blackbold),
            dcc.Checklist(id='status_type',
                    options=[{'label':str(s),'value':s} for s in sorted(df['Status'].unique())],
                    value=[s for s in sorted(df['Status'].unique())],
            ),

            # Activities
            html.Br(),
            html.Label(['Activity: '],style=blackbold),
            html.Pre(id='activity_type', children=[],
            style={'white-space': 'pre-wrap','word-break': 'break-all',
                 'border': '1px solid black','text-align': 'center',
                 'padding': '12px 12px 12px 12px', 'color':'blue',
                 'margin-top': '3px'}
            ),

            # Jurisdiction_checklist
            html.Br(),
            html.Label(children=['Jurisdiction: '], style=blackbold),
            dcc.Checklist(id='jurisdiction_name',
                    options=[{'label':str(j),'value':j} for j in sorted(df['Jurisdiction'].unique())],
                    value=[j for j in sorted(df['Jurisdiction'].unique())],
            ),



        ], className='three columns left-side-bar'
        ),

        # Map
        html.Div([
            dcc.Graph(id='graph', config={'displayModeBar': False, 'scrollZoom': True},
                style={'background':'#efeff5','padding-bottom':'2px','padding-left':'2px','height':'100vh'}
            )
        ], className='nine columns'
        ),

    ], className='row'
    ),

], className='ten columns offset-by-one'
)

#---------------------------------------------------------------
# Output of Graph
@app.callback(Output('graph', 'figure'),
              [Input('jurisdiction_name', 'value'),
               Input('status_type', 'value')])

def update_figure(chosen_jurisdiction,chosen_status):
    df_sub = df[(df['Jurisdiction'].isin(chosen_jurisdiction)) &
                (df['Status'].isin(chosen_status))]

    # Create figure
    locations=[go.Scattermapbox(
                    lon = df_sub['Longitude'],
                    lat = df_sub['Latitude'],
                    mode='markers',
                    marker={'color' : df_sub['Colour']},
                    unselected={'marker' : {'opacity':1}},
                    selected={'marker' : {'opacity':0.5, 'size':25}},
                    hoverinfo='text',
                    hovertext=df_sub['Name'],
                    customdata=df_sub['Activities']
    )]

    # Return figure
    return {
        'data': locations,
        'layout': go.Layout(
            uirevision= 'foo', #preserves state of figure/map after callback activated
            clickmode= 'event+select',
            hovermode='closest',
            hoverdistance=2,
            title=dict(text="Ontario Money Services Businesses Risk Appetite",font=dict(size=26, color='#6699ff')),
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=25,
                style='dark',
                center=dict(
                    lat=43.7278015,
                    lon=-79.3393776
                ),
                pitch=40,
                zoom=5
            ),
        )
    }
#---------------------------------------------------------------
# callback for activity type
@app.callback(
    Output('activity_type', 'children'),
    [Input('graph', 'clickData')])
def display_click_data(clickData):
    if clickData is None:
        return 'Click on any bubble'
    else:
        # print (clickData)
        the_activities=clickData['points'][0]['customdata']
        if the_activities is None:
            return 'No Activities Available'
        else:
            return html.Span(the_activities)
# #--------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)
