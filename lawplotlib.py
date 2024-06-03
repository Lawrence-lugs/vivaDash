import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def configFilterFamily(configString,df : pd.DataFrame):
    tracesPerPlot = parseConfigString(configString,df)

    df['family'] = 'notIncluded'

    for i,tracesInPlot in enumerate(tracesPerPlot):
        familyString = f'traceSet{i}'
        for traceName in tracesInPlot:
            df.loc[df['variable'].str.match(traceName),'family'] = familyString

    return df[df['family'] != 'notIncluded']

def parseConfigString(configString,df):
    perFamily = configString.split(';')
    perTracePerFamily = [i.split(',') for i in perFamily]
    return perTracePerFamily

def processAndMelt(df):
    xcol = [i for i in df.columns if ' X' in i][0]
    df['time'] = df[xcol]
    df = df[[i for i in df.columns if ' X' not in i]]
    df = df.rename({i: i[1:-2] for i in df.columns if 'time' not in i}, axis='columns')
    df = df.melt('time')
    return df

def getFamilyName(waveName):
    return waveName.split('<')[0].split('(')[0]

def addFamilyTypeToMeltedDF(df):
    df['family'] = df['variable'].apply(getFamilyName)
    return df

def split_traces_by_family_dict(df):
    plotlines =[]
    familydict = {}

    for colName in df.columns:
        stringToMatch = colName.split('<')[0]
        if stringToMatch not in familydict.keys():    
            familydict[stringToMatch] = [colName]
        else:
            familydict[stringToMatch].append(colName)

    return familydict

def get_values_before_posedge_clk(df_xvalues,
                                  df_yvalues,
                                  clk_period,
                                  eps = 0.001
                                  ):

    nx_points = df_xvalues.max() // clk_period

    x_points = np.linspace(0,clk_period*nx_points, int(nx_points)+1) - clk_period*eps
    x_points = x_points[1:]

    y_points = []
    for x in x_points:
        y_points.append(np.interp(x,df_xvalues,df_yvalues))

    return x_points,y_points

def df_getjustys(df):
    '''
    Also removes the slashes
    '''
    df = df[[i for i in df.columns if ' X' not in i]]
    df = df[[i[1:] if i[0] == '/' else i for i in df.columns]]
    df = df.rename({i: i[:-2] for i in df.columns}, axis='columns')
    return df

def df_sortcols_alphabetically(df):
    cols = [i for i in df.columns]
    cols = sorted(cols)
    df = df[cols]
    return df

def process_transient_csv(df):
    xcol = [i for i in df.columns if ' X' in i][0]
    df['time'] = df[xcol]
    df = df[[i for i in df.columns if ' X' not in i]]
    df = df.rename({i: i[:-2] for i in df.columns if 'time' not in i}, axis='columns')
    df = df.set_index('time')
    return df