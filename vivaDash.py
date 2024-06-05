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
csvName = 'Using CSV: No CSV selected'
waves = os.listdir('waveforms')

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
    html.Div([
        'Graph Height: \t',
        dcc.Slider(
            1,200,
            marks=None,
            value=60,
            id = 'familyGraphHeight'
        ),
    ]),
    html.Div(  
        id = 'familyGraphContainer',
        style={
            'height':'60vh'
        },
        children=[
            dcc.Graph(id='graph-content',
                    style={
                        'marginLeft':'auto',
                        'marginRight':'auto',
                        'align':'center',
                        'width':'100%',
                        'height':'100%',
                    },
                    config={
                        'editable':True,  
                        'toImageButtonOptions': {'format': 'svg'},
                    },
            )
        ]
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
    html.Div([
        'Graph Height: \t',
        dcc.Slider(
            1,200,
            marks=None,
            value=60,
            id = 'cfgStringGraphHeight'
        ),
    ]),
    html.Div(  
        id = 'configGraphContainer',
        style={
            'height':'60vh'
        },
        children=[
            dcc.Graph(id='configStringGraph',
                    style={
                        'marginLeft':'auto',
                        'marginRight':'auto',
                        'align':'center',
                        'width':'100%',
                        'height':'100%',
                    },
                    config={
                        'editable':True,  
                        'toImageButtonOptions': {'format': 'svg'},
                    },
                    responsive=True,
            ),
        ],
    )
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
    Output('familyGraphContainer','style'),
    Input('familyGraphHeight', 'value')
)
@callback(
    Output('configGraphContainer','style'),
    Input('cfgStringGraphHeight', 'value')
)
def updateCfgGraphContainer(heightString):
    styleDict = {'height':str(heightString) + 'vh'}
    return styleDict

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
    fig.for_each_annotation(lambda a: a.update(text=''))
    fig.update_yaxes(automargin=True)

    return fig

@callback(
    Output('csvToParse','options'),
    Input('csvToParse','value')
)
def reloadWaveforms(surrogateValue):
    return os.listdir('waveforms')


if __name__ == '__main__':
    app.run(debug=True)