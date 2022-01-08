# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 04:48:48 2021

@author: User
"""
import dash
#import dash_core_components as dcc
#import dash_html_components as html
from dash import dcc
from dash import html

import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import dash_pivottable
import os
import plotly.graph_objs as go

#css_directory = os.getcwd()
#stylesheets = ['style.css']
#static_css_route = '/assets/'


#assets_path = os.getcwd()+'/assets'

#data = pd.read_csv("D:/testdash/data/avocado.csv")
#dataori = pd.read_csv("D:/testdash/S01_CAMn2.csv")
data = pd.read_csv("siteNameList.csv")

#data['timestamp1']=pd.to_datetime(data['timestamp'])
#data['Date'] = data['timestamp1'].dt.date
#data['Time'] = data['timestamp1'].dt.time
#data.sort_values("timestamp1", inplace=True)
#data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
'''
dataori = pd.read_csv("S01_CAMn2.csv")
dataori["timestamp"] = pd.to_datetime(dataori["timestamp"])
dataori["DateT"] = pd.to_datetime(dataori["Date"])
dataori["Time"] = pd.to_datetime(dataori["Time"])
dataori["Hour"] = dataori["Time"].dt.hour
dataori["Date"] = dataori["DateT"].dt.date
'''
#data.sort_values("Date", inplace=True)

#data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
#data.sort_values("Date", inplace=True)

#dataori = [dataori.columns.values.tolist()]+dataori.values.tolist()

external_stylesheets = ['https://fonts.googleapis.com/css?family=Kanit|Prompt']
'''
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheets",
    },
]
'''
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,assets_folder = 'assets',suppress_callback_exceptions=True)
app._favicon = ("car.ico")
app.title = "Traffic Survey Summary"

app.layout = html.Div([
    html.H1('สรุปข้อมูลสำรวจจราจร'),
    html.Div(children="เลือกโครงการ", className="menu-title"),
    html.Div([
        dcc.Dropdown(
        id="site-filter",
        options=[
            {"label": i, "value": i}
            for i in np.sort(data.Site.unique())
        ],
        value='S01',
        clearable=False,
        className="dropdown1",
        ),
    ], style={"width": "14.5%"},),
    

    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[

        dcc.Tab(label='ปริมาณจราจร และ ความเร็ว ณ จุดสำรวจ', value='tab-1-example-graph'),
            
        dcc.Tab(label='ความเร็ว บน แนวเส้นโครงการฯ (วันธรรมดา)', value='tab-2-example-graph'),
        
        dcc.Tab(label='ความเร็ว บน แนวเส้นโครงการฯ (วันหยุด)', value='tab-3-example-graph'),
    ]),
    
    html.Div(id='tabs-content-example-graph'),
])

@app.callback(Output('data-select','children'),[Input('site-filter','value')]) 

def update_siteData(value):
    filename = 'D:/traffic/data/mbCount/{}.csv'.format(value)
    #filename = 'D:/testdash/data/mbCount/%s.csv'%value
    dataori = pd.read_csv(filename, encoding = 'unicode_escape')
    dataori["timestamp"] = pd.to_datetime(dataori["timestamp"])
    #dataori["DateT"] = dataori['timestamp'].dt.date
    #dataori["TimeT"] = dataori['timestamp'].dt.time
    #dataori["Date"] = pd.to_datetime(dataori["DateT"])
    #dataori["Time"] = pd.to_datetime(dataori["TimeT"])
    dataori["Hour"] = dataori['timestamp'].dt.hour
    dataori["Date"] = dataori['timestamp'].dt.date
    dataori['count']=1
    dataori = [dataori.columns.values.tolist()]+dataori.values.tolist()
    return html.Div(
                    children=[                      
                        html.Div([
                        dash_pivottable.PivotTable(
                            data = dataori,
                            cols=["class_type"],
                            rows=["Date"],
                            vals=["count"],
                        ),
                    ]),
                    ], 
                ),                                         


@app.callback(Output('section-speed','children'),Input('site-filter','value'))
def update_siteData1(sites):
    #filename = 'D:/testdash/%s.csv'%Site
    filename = 'D:/traffic/data/sectionSpeed/{}.csv'.format(sites)
    dfSpeed = pd.read_csv(filename)
      
    fig = go.Figure([
        go.Scatter(
            name='EB (NB)',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_710_EB'],
            mode='lines',
            line=dict(color='rgb(220, 20, 60)'),
        ),
        go.Scatter(
            name='Upper Bound',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_710_EB']+dfSpeed['Sdev_WD_710_EB'],
            mode='lines',
            marker=dict(color="#dc143c"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='EB (NB) - Stdev.',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_710_EB']-dfSpeed['Sdev_WD_710_EB'],
            marker=dict(color="#dc143c"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(220, 20, 60, 0.3)',
            fill='tonexty',
            showlegend=True
        ),
        go.Scatter(
            name='WB (SB)',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_710_WB'],
            mode='lines',
            line=dict(color='rgb(31, 119, 180)'),
        ),
        go.Scatter(
            name='Upper Bound-WB',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_710_WB']+dfSpeed['Sdev_WD_710_WB'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='WB (SB) - Stdev.',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_710_WB']-dfSpeed['Sdev_WD_710_WB'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=True
        ),
        ])
    
    fig1 = go.Figure([
        go.Scatter(
            name='EB (NB)',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_1016_EB'],
            mode='lines',
            line=dict(color='rgb(220, 20, 60)'),
        ),
        go.Scatter(
            name='Upper Bound',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_1016_EB']+dfSpeed['Sdev_WD_1016_EB'],
            mode='lines',
            marker=dict(color="#dc143c"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_1016_EB']-dfSpeed['Sdev_WD_1016_EB'],
            marker=dict(color="#dc143c"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(220, 20, 60, 0.3)',
            fill='tonexty',
            showlegend=False
        ),
        go.Scatter(
            name='WB (SB)',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_1016_WB'],
            mode='lines',
            line=dict(color='rgb(31, 119, 180)'),
        ),
        go.Scatter(
            name='Upper Bound-WB',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_1016_WB']+dfSpeed['Sdev_WD_1016_WB'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound-WB',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_1016_WB']-dfSpeed['Sdev_WD_1016_WB'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False
        ),
        ])
    
    fig2 = go.Figure([
        go.Scatter(
            name='EB (NB)',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_1619_EB'],
            mode='lines',
            line=dict(color='rgb(220, 20, 60)'),
        ),
        go.Scatter(
            name='Upper Bound',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_1619_EB']+dfSpeed['Sdev_WD_1619_EB'],
            mode='lines',
            marker=dict(color="#dc143c"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_1619_EB']-dfSpeed['Sdev_WD_1619_EB'],
            marker=dict(color="#dc143c"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(220, 20, 60, 0.3)',
            fill='tonexty',
            showlegend=False
        ),
        go.Scatter(
            name='WB (SB)',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_1619_WB'],
            mode='lines',
            line=dict(color='rgb(31, 119, 180)'),
        ),
        go.Scatter(
            name='Upper Bound-WB',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_1619_WB']+dfSpeed['Sdev_WD_1619_WB'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound-WB',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WD_1619_WB']-dfSpeed['Sdev_WD_1619_WB'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False
        ),
        ])
    
    fig.update_layout(
        yaxis_title='ความเร็วเฉลี่ย (กิโลเมตร/ชั่วโมง)',
        xaxis_title='ช่วงถนนโครงการฯ',
        title='ความเร็วเฉลี่ยบนช่วงถนนโครงการ (เวลา 7:00น. - 10:00น.)',
        hovermode="x"
        )
    
    fig1.update_layout(
        yaxis_title='ความเร็วเฉลี่ย (กิโลเมตร/ชั่วโมง)',
        xaxis_title='ช่วงถนนโครงการฯ',
        title='ความเร็วเฉลี่ยบนช่วงถนนโครงการ (เวลา 10:00น. - 16:00น.)',
        hovermode="x"
        )
    
    fig2.update_layout(
        yaxis_title='ความเร็วเฉลี่ย (กิโลเมตร/ชั่วโมง)',
        xaxis_title='ช่วงถนนโครงการฯ',
        title='ความเร็วเฉลี่ยบนช่วงถนนโครงการ (เวลา 16:00น. - 19:00น.)',
        hovermode="x"
        )
    '''
    fig1 = go.Figure([
        go.Scatter(
            name='Measurement',
            x=dfSpeed['Sec'],
            y=dfSpeed['EB_AvgSp'],
            mode='lines',
            line=dict(color='rgb(31, 119, 180)'),
        ),
        go.Scatter(
            name='Upper Bound',
            x=dfSpeed['Sec'],
            y=dfSpeed['EB_AvgSp']+dfSpeed['EB_SdSp'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound',
            x=dfSpeed['Sec'],
            y=dfSpeed['EB_AvgSp']-dfSpeed['EB_SdSp'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False
        )
        ])
    #fig.show()
    '''
    return html.Div(
                    children=[                      
                        html.Div([
                            dcc.Graph(figure=fig),
                            dcc.Graph(figure=fig1),
                            dcc.Graph(figure=fig2),
                    ]),
                    ], 
                ),   

@app.callback(Output('section-speed-pm','children'),Input('site-filter','value'))
def update_siteData1(sites):
    #filename = 'D:/testdash/%s.csv'%Site
    filename = 'D:/testdash/data/sectionSpeed/{}.csv'.format(sites)
    dfSpeed = pd.read_csv(filename)
      
    fig = go.Figure([
        go.Scatter(
            name='EB (NB)',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_710_EB'],
            mode='lines',
            line=dict(color='rgb(220, 20, 60)'),
        ),
        go.Scatter(
            name='Upper Bound',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_710_EB']+dfSpeed['Sdev_WE_710_EB'],
            mode='lines',
            marker=dict(color="#dc143c"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_710_EB']-dfSpeed['Sdev_WE_710_EB'],
            marker=dict(color="#dc143c"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(220, 20, 60, 0.3)',
            fill='tonexty',
            showlegend=False
        ),
        go.Scatter(
            name='WB (SB)',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_710_WB'],
            mode='lines',
            line=dict(color='rgb(31, 119, 180)'),
        ),
        go.Scatter(
            name='Upper Bound-WB',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_710_WB']+dfSpeed['Sdev_WE_710_WB'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound-WB',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_710_WB']-dfSpeed['Sdev_WE_710_WB'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False
        ),
        ])
    
    fig1 = go.Figure([
        go.Scatter(
            name='EB (NB)',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_1016_EB'],
            mode='lines',
            line=dict(color='rgb(220, 20, 60)'),
        ),
        go.Scatter(
            name='Upper Bound',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_1016_EB']+dfSpeed['Sdev_WE_1016_EB'],
            mode='lines',
            marker=dict(color="#dc143c"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_1016_EB']-dfSpeed['Sdev_WE_1016_EB'],
            marker=dict(color="#dc143c"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(220, 20, 60, 0.3)',
            fill='tonexty',
            showlegend=False
        ),
        go.Scatter(
            name='WB (SB)',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_1016_WB'],
            mode='lines',
            line=dict(color='rgb(31, 119, 180)'),
        ),
        go.Scatter(
            name='Upper Bound-WB',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_1016_WB']+dfSpeed['Sdev_WE_1016_WB'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound-WB',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_1016_WB']-dfSpeed['Sdev_WE_1016_WB'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False
        ),
        ])
    
    fig2 = go.Figure([
        go.Scatter(
            name='EB (NB)',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_1619_EB'],
            mode='lines',
            line=dict(color='rgb(220, 20, 60)'),
        ),
        go.Scatter(
            name='Upper Bound',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_1619_EB']+dfSpeed['Sdev_WE_1619_EB'],
            mode='lines',
            marker=dict(color="#dc143c"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_1619_EB']-dfSpeed['Sdev_WE_1619_EB'],
            marker=dict(color="#dc143c"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(220, 20, 60, 0.3)',
            fill='tonexty',
            showlegend=False
        ),
        go.Scatter(
            name='WB (SB)',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_1619_WB'],
            mode='lines',
            line=dict(color='rgb(31, 119, 180)'),
        ),
        go.Scatter(
            name='Upper Bound-WB',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_1619_WB']+dfSpeed['Sdev_WE_1619_WB'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound-WB',
            x=dfSpeed['BS_Id'],
            y=dfSpeed['Avg_WE_1619_WB']-dfSpeed['Sdev_WE_1619_WB'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False
        ),
        ])
    
    fig.update_layout(
        yaxis_title='ความเร็วเฉลี่ย (กิโลเมตร/ชั่วโมง)',
        xaxis_title='ช่วงถนนโครงการฯ',
        title='ความเร็วเฉลี่ยบนช่วงถนนโครงการ (เวลา 7:00น. - 10:00น.)',
        hovermode="x"
        )
    
    fig1.update_layout(
        yaxis_title='ความเร็วเฉลี่ย (กิโลเมตร/ชั่วโมง)',
        xaxis_title='ช่วงถนนโครงการฯ',
        title='ความเร็วเฉลี่ยบนช่วงถนนโครงการ (เวลา 10:00น. - 16:00น.)',
        hovermode="x"
        )
    
    fig2.update_layout(
        yaxis_title='ความเร็วเฉลี่ย (กิโลเมตร/ชั่วโมง)',
        xaxis_title='ช่วงถนนโครงการฯ',
        title='ความเร็วเฉลี่ยบนช่วงถนนโครงการ (เวลา 16:00น. - 19:00น.)',
        hovermode="x"
        )
    '''
    fig1 = go.Figure([
        go.Scatter(
            name='Measurement',
            x=dfSpeed['Sec'],
            y=dfSpeed['EB_AvgSp'],
            mode='lines',
            line=dict(color='rgb(31, 119, 180)'),
        ),
        go.Scatter(
            name='Upper Bound',
            x=dfSpeed['Sec'],
            y=dfSpeed['EB_AvgSp']+dfSpeed['EB_SdSp'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound',
            x=dfSpeed['Sec'],
            y=dfSpeed['EB_AvgSp']-dfSpeed['EB_SdSp'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False
        )
        ])
    #fig.show()
    '''
    return html.Div(
                    children=[                      
                        html.Div([
                            dcc.Graph(figure=fig),
                            dcc.Graph(figure=fig1),
                            dcc.Graph(figure=fig2),
                    ]),
                    ], 
                ),   


@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'),
              )
def render_content(tab):
    if tab == 'tab-1-example-graph':
         
        return  html.Div(id='data-select'),
                     
    elif tab == 'tab-2-example-graph':
        return  html.Div([
            html.Div(id='section-speed'),
        ])
    elif tab == 'tab-3-example-graph':
        return html.Div([
            html.Div(id='section-speed-pm'),
        ])



if __name__ == '__main__':
    app.run_server(debug=True)




