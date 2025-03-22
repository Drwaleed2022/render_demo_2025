import pandas as pd
import plotly 
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash
from dash import html,dcc,dash_table
import numpy as np
import calendar
import datetime
import webbrowser
from threading import Timer
import calendar
import datetime
import gunicorn
import openpyxl
df_sales=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/df_sales.xlsx")
df_sales.set_index('Area',inplace=True)
rep_25=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/rep_25.xlsx")
rep_25.set_index('Area_rep',inplace=True)
rep_profit_25=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/rep_profit_25.xlsx")
rep_profit_25.set_index('Area_rep',inplace=True)
Area_global=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/Area_global.xlsx")
Area_global.set_index('Area_rep',inplace=True)
Area_rep_25=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/Area_rep_25.xlsx")
Area_rep_25.set_index('Area_rep',inplace=True)
Area_25=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/Area_25.xlsx")
Area_25.set_index('Area',inplace=True)
rep_target=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/rep_target.xlsx")
rep_target.set_index('Sales_rep',inplace=True)
area_rep_target=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/area_rep_target.xlsx")
area_rep_target.set_index('area_rep',inplace=True)
debts_area=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/debts_area.xlsx")
debts_area.set_index('المنطقة',inplace=True)
Area_Area__rep_25=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/Area_Area__rep_25.xlsx")
Area_Area__rep_25.set_index('Area_rep',inplace=True)
Area_Area__rep_profit_25=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/Area_Area__rep_profit_25.xlsx")
Area_Area__rep_profit_25.set_index('Area_rep',inplace=True)
Area_rep_Area_rep_25=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/Area_rep_Area_rep_25.xlsx")
Area_rep_Area_rep_25.set_index('Area_rep',inplace=True)
Area_Area__rep_25.sort_values('Feb_2025',inplace=True)
Date=['Jan_2025', 'Feb_2025', 'Mar_2025', 'Apr_2025', 'May_2025', 'Jun_2025','Jul_2025', 'Aug_2025', 'Sep_2025', 'Oct_2025', 'Nov_2025', 'Dec_2025']
for i in Date:
    date=i
    print(date)
SALES_REP=df_sales['Sales_rep'].unique()
for i in SALES_REP:
    sales_rep=i
    print(sales_rep)
PHARMACY=(df_sales[df_sales['Customer'].str.startswith('ص')].groupby('Customer').agg({"Sales":sum,"Profit":sum}).sort_values('Sales',ascending=False)).index
for i in PHARMACY:
    pharmacy=i
    print(pharmacy)    
AREA=Area_25.index.to_list()
for i in AREA:
    area=i
    print(area)
AREA_REP=Area_Area__rep_25.index
for i in AREA_REP:
    area_rep=i
    print(area_rep)  
from dash import Output
from dash import Dash
from dash.dash import Input    
import flask, multiprocessing
app = Dash(__name__, suppress_callback_exceptions=True)
server=app.server
# Build dash app layout
app.layout = html.Div(children=[ html.H1('Sales Statistics Dashboard', 
                                style={'textAlign': 'center','color': 'green','font-size': 40}),
                                
                                html.Div([
                                        html.Div(["Date:"  ,dcc.Dropdown(Date,id='date',value='Mar_2025', 
                                style={'height':'100px','width':'1500px','margin':'black','background':' lightgreen','bordercolor':'black', 'color': 'darkblue','font-size': 35})]),
                                        html.Div(["AREA_REP:",dcc.Dropdown(AREA_REP,id='area_rep', value='Shimaa', 
                                style={'height':'100px','width':'1500px','background':'yellow','bordercolor':'black','color': 'darkgreen','font-size': 35})])  
                                                                                                    
                                ],style={'font-size': 35,'display': 'flex','color': 'green'}),
                                 # Segment 1
                                html.Div([                                        
                                        html.Div(dcc.Graph(id='fig_0'),style={'font-size': 35,'background':'white','height':'300px','width':'3000px'})
                                ], style={'font-size': 35,'display': 'flex'}),  
                                 # Segment 2
                            
                                        html.Div([                                        
                                        html.Div(dcc.Graph(id='curve1'), style={'font-size': 25,'height':'900px','width':'1000px'}),                                        
                                        html.Div(dcc.Graph(id='fig_egy'), style={'font-size': 25,'height':'900px','width':'1000px'}),
                                        html.Div(dcc.Graph(id='curve2'), style={'font-size': 15,'height':'900px','width':'1000px'})
                                ], style={'font-size': 25,'display': 'flex'}),  
                                # Segment 3
                            
                                        html.Div([                                        
                                        html.Div(dcc.Graph(id='curve3'), style={'font-size': 25,'height':'900px','width':'1500px'}),
                                        html.Div(dcc.Graph(id='curve4'), style={'font-size': 25,'height':'900px','width':'1500px'})
                                ], style={'font-size': 25,'display': 'flex'}),
                                # Segment 4
                                html.Div([
                                        html.Div(dcc.Graph(id='curve12'),style={'font-size': 25,'height':'900px','width':'3000px'})
                                ], style={'font-size': 25,'display': 'flex'}),
                                
                                
                                ])


'''def compute_info(df_month_number,month):
    df_X =df_month_number[df_month_number[Month]==int(month)]
    return df_X'''
# Callback decorator
@app.callback( [ Output(component_id='fig_0', component_property='figure'),
                Output(component_id='curve1', component_property='figure'),
                Output(component_id='fig_egy', component_property='figure'),
                Output(component_id='curve2', component_property='figure'),
               Output(component_id='curve3', component_property='figure'),
               Output(component_id='curve4', component_property='figure'),
               Output(component_id='curve12', component_property='figure')
            ],
               [
                Input(component_id='date', component_property='value'),
                Input(component_id='area_rep', component_property='value')
                ])
# Computation to callback function and return graph
def update_output(date,area_rep): 
    fig_0 = plotly.subplots.make_subplots(rows=1, cols=3)
    sales =Area_Area__rep_25[date].loc[area_rep].sum()
    profit = Area_Area__rep_profit_25[date].loc[area_rep].sum()
    acheivement = sales/area_rep_target['MONTHLY TARGET'].loc[area_rep].sum()*100
    kpi_annotations = [
    dict(
        text=f"£{sales/1000000:.2f} M",
        font=dict(size=30, color='blue'),
        showarrow=False
    ),
    dict(
        text=f"£{profit/1000000:.2f} M",
        font=dict(size=30, color='green'),
        showarrow=False,
        xanchor="center",
        yanchor="middle"
    ),
   dict(
        text=f"%{acheivement:.2f}",
        font=dict(size=30, color='purple'),
        showarrow=False
    )
    ]

   # Define titles for each KPI
    kpi_titles = ["Total sales", "Total profit", "Acheivement"]
    # Add KPIs as annotations to subplots
    for i in range(3):
       fig_0.add_annotation(
        kpi_annotations[i],
        xref=f"x{i+1}",
        yref="paper",
        xanchor="center",
        yanchor="middle"
        )
       fig_0.update_xaxes(title_text=kpi_titles[i], row=1, col=i+1, 
                     showticklabels=False, showline=True, showgrid=False, 
                     zeroline=False,side="top")
       fig_0.update_yaxes(showticklabels=False, showline=True, showgrid=False,
                     zeroline=False)
    
    # Update layout
    fig_0.update_layout(
      height=200,
      margin=dict(t=50, b=0),
      showlegend=False,
      font=dict(color='blue', size=30))
    curve1=px.sunburst(Area_rep_Area_rep_25, path=['Area','Sales_rep'],values=date,title='Sales per Area & rep in specific Month')
    curve1.update_layout(paper_bgcolor = "white",width=1000,height=750,title_automargin=False,legend_font_size=35,font=dict(color='blue', size=30))
    fig_egy = go.Figure(go.Scattergeo(    
    lon = Area_global['Longitude'],
    lat = Area_global['Latitude'],
    text = "                            "+Area_global.index+""+"("+((Area_global[date]/1000000).round(2)).astype('str')+""+"M"+""+")",
    mode = 'markers+text',
    marker = dict(
        size = 15,
        color = ['green','blue','red'],
        symbol = 'circle'

    )
))

    fig_egy.update_geos(
     
    lataxis_range=[27,32.5], lonaxis_range=[26.2,34],visible=False, resolution=50,
    showcountries=True, countrycolor="Black",
    showsubunits=True, subunitcolor="Blue",
    showcoastlines=True, coastlinecolor="RebeccaPurple",
    showland=True, landcolor="white",
    showocean=True, oceancolor="LightBlue",
    showlakes=False, lakecolor="Blue",
    showrivers=True, rivercolor="Blue",
     projection_scale=1.3,
    )
    fig_egy.update_layout(title={'text': "Sales per Governorate in specific Month"},height=750,width=1000, margin={"r":0,"t":100,"l":0,"b":0},font=dict(color='blue', size=25))
    curve2=px.bar(Area_Area__rep_25,y=Date,x=Area_Area__rep_25.index,text_auto=True,title='Retail Sales per Area & rep YTD')
    curve2.update_layout(paper_bgcolor = "white",height=750,legend_font_size=15,font=dict(color='blue', size=20))
    curve3=px.scatter(Area_Area__rep_25.loc[['Shimaa','Israa','Aya','Ihab','Isupply','Omet','Konty']],y=Area_Area__rep_25[date].loc[['Shimaa','Israa','Aya','Ihab','Isupply','Omet','Konty']],text=Area_Area__rep_25[date].loc[['Shimaa','Israa','Aya','Ihab','Isupply','Omet','Konty']],size=Area_Area__rep_25[date].loc[['Shimaa','Israa','Aya','Ihab','Isupply','Omet','Konty']], color=date,hover_name=['Shimaa','Israa','Aya','Ihab','Isupply','Omet','Konty'],size_max=160,title='Retail Sales in specific month ')
    curve3.update_layout(paper_bgcolor = "white",width=1500,height=750,title_automargin=False,legend_font_size=35,font=dict(color='blue', size=30))
    curve4=px.bar(Area_Area__rep_25.loc[area_rep],y=area_rep,color=Date,text_auto=True,title='Retail Sales per rep')
    curve4.update_layout(paper_bgcolor = "white",width=1500,height=750,font=dict(color='blue', size=30))
    curve12= px.imshow(rep_25,x=rep_25.columns,y=rep_25.index,text_auto=True,color_continuous_scale='RdBu_r', aspect="auto",title='Reps Sales YTD')
    curve12.update_xaxes(side="top")
    curve12.update_layout(paper_bgcolor = "white",height=750,title_automargin=False,font=dict(color='blue', size=30))
      
    return[fig_0,curve1,fig_egy,curve2,curve3,curve4,curve12]

if __name__ == '__main__':
    #Timer(1,open_browser).start();
        
    app.run_server(debug=False)
    app.enable_dev_tools(debug=True)

    
