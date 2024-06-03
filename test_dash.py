#%%

from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import lawplotlib
import os
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go

pio.templates.default = 'seaborn'

app = Dash()

waves = os.listdir('waveforms')

csvName = 'Using CSV: No CSV selected'

app.layout = [
    html.H1(children='Lawrences CSV AutoPlotter'),
    dcc.Dropdown(waves, id='csvToParse'),
    html.H3(
        id = 'csvNameHeader',
        children=csvName
        ),
    html.Hr(),
    html.H3(
        'By-family Plotter'
    ),
    dcc.Dropdown(id='waveToPlot',multi=True),
    dcc.Graph(id='graph-content',
              style={
                  'marginLeft':'auto',
                  'marginRight':'auto',
                  'align':'center'
              },
              config={
                  'editable':True,  
                  'toImageButtonOptions': {'format': 'svg'},
              },
    ),
    html.Div([
        html.H3('RegEXP Plotter'),
        'Input Traces separated with ; by row. Add traces via , . e.g. "BL,BLB;SA_OUT,SA_OUTB"',
        dcc.Input(
        id = 'wavesConfigString',
        type = 'text',
        style={
            'width':'100%'
        }
        ),
    ]),
    
    dcc.Graph(id='configStringGraph',
              style={
                  'marginLeft':'auto',
                  'marginRight':'auto',
                  'align':'center'
              },
              config={
                  'editable':True,  
                  'toImageButtonOptions': {'format': 'svg'},
              },
    ),
    # html.Div(['Number of Subplot Rows:',
    # dcc.Input(
    #     id='numRowSubplots',
    #     type='number'),
    # 'Number of Subplot Cols:',
    # dcc.Input(
    #     id='numColSubplots',
    #     type='number')
    #     ]),
    # dash_table.DataTable(
    #     id = 'dfViewer',
    #     style={
    #         'hidden':'True',
    #     }
    # )
]

@callback(
    [Output('csvNameHeader', 'children'),
    Output('waveToPlot','options')
    ],
    Input('csvToParse', 'value')
)
def updateSelectedCSV(value):
    df = pd.read_csv('waveforms/' + value)
    df = lawplotlib.processAndMelt(df)
    df = lawplotlib.addFamilyTypeToMeltedDF(df)
    return value, df['family'].unique()

@callback(
    Output('graph-content', 'figure'),
    [Input('waveToPlot', 'value'),
    Input('csvToParse', 'value'),]
)
def update_graph(familylist,csvName):
    df = pd.read_csv('waveforms/' + csvName)
    df = lawplotlib.processAndMelt(df)
    df = lawplotlib.addFamilyTypeToMeltedDF(df)

    df = df[df['family'].isin(familylist)]

    fig = px.line(df,y='value',x='time',facet_row='family',color='variable')
    fig.update_layout(
        font_family="Trebuchet MS",
        title_font_family="Trebuchet MS",
    )
    fig.update_yaxes(automargin=True)
    return fig

@callback(
    Output('configStringGraph','figure'),
    [Input('wavesConfigString', 'value'),
    Input('csvToParse', 'value'),]
)
def updateCfgGraph(configString,csvName):
    df = pd.read_csv('waveforms/' + csvName)
    df = lawplotlib.processAndMelt(df)
    df = lawplotlib.configFilterFamily(configString,df)

    fig = px.line(df,y='value',x='time',facet_row='family',color='variable')
    fig.update_layout(
        font_family="Trebuchet MS",
        title_font_family="Trebuchet MS",
    )
    fig.update_yaxes(automargin=True)

    return fig

if __name__ == '__main__':
    app.run(debug=True)