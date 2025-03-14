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
rep_25.set_index('Sales_rep',inplace=True)
rep_profit_25=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/rep_profit_25.xlsx")
rep_profit_25.set_index('Sales_rep',inplace=True)
Area_global=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/Area_global.xlsx")
Area_global.set_index('Area',inplace=True)
Area_rep_25=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/Area_rep_25.xlsx")
Area_rep_25.set_index('Area_rep',inplace=True)
Area_25=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main//Area_25.xlsx")
Area_25.set_index('Area',inplace=True)
rep_target=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/rep_target.xlsx")
rep_target.set_index('Sales_rep',inplace=True)
debts_area=pd.read_excel("https://raw.githubusercontent.com/Drwaleed2022/render_demo_2025/main/debts_area.xlsx")
debts_area.set_index('المنطقة',inplace=True)
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
                                        html.Div(["SALES_REP:",dcc.Dropdown(SALES_REP,id='sales_rep', value='Shimaa', 
                                style={'height':'100px','width':'1500px','background':'yellow','bordercolor':'black','color': 'darkgreen','font-size': 35})])  
                                                                                                    
                                ],style={'font-size': 35,'display': 'flex','color': 'green'}),
                                 # Segment 1
                                html.Div([                                        
                                        html.Div(dcc.Graph(id='fig_0'),style={'font-size': 35,'background':'white','height':'300px','width':'3000px'})
                                ], style={'font-size': 35,'display': 'flex'}),    
                                # Segment 2
                            
                                        html.Div([                                        
                                        html.Div(dcc.Graph(id='curve3'), style={'font-size': 25,'height':'900px','width':'1500px'}),
                                        html.Div(dcc.Graph(id='curve4'), style={'font-size': 25,'height':'900px','width':'1500px'})
                                ], style={'font-size': 25,'display': 'flex'}),
                                # Segment 3
                                html.Div([
                                        html.Div(dcc.Graph(id='curve12'),style={'font-size': 25,'height':'900px','width':'3000px'})
                                ], style={'font-size': 25,'display': 'flex'}),
                                
                                
                                ])


'''def compute_info(df_month_number,month):
    df_X =df_month_number[df_month_number[Month]==int(month)]
    return df_X'''
# Callback decorator
@app.callback( [ Output(component_id='fig_0', component_property='figure'),
               Output(component_id='curve3', component_property='figure'),
               Output(component_id='curve4', component_property='figure'),
               Output(component_id='curve12', component_property='figure')
            ],
               [
                Input(component_id='date', component_property='value'),
                Input(component_id='sales_rep', component_property='value')
                ])
# Computation to callback function and return graph
def update_output(date,sales_rep): 
    fig_0 = plotly.subplots.make_subplots(rows=1, cols=3)
    sales =rep_25[date].loc[sales_rep].sum()
    profit = rep_profit_25[date].loc[sales_rep].sum()
    acheivement = sales/rep_target['Target'].loc[sales_rep].sum()*100
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
    curve3=px.scatter(rep_25.loc[['Shimaa','Israa','Aya','Ihab','Isupply','Omet','Konty']],y=rep_25[date].loc[['Shimaa','Israa','Aya','Ihab','Isupply','Omet','Konty']],text=rep_25[date].loc[['Shimaa','Israa','Aya','Ihab','Isupply','Omet','Konty']],size=rep_25[date].loc[['Shimaa','Israa','Aya','Ihab','Isupply','Omet','Konty']], color=date,hover_name=['Shimaa','Israa','Aya','Ihab','Isupply','Omet','Konty'],size_max=160,title='Retail Sales in specific month ')
    curve3.update_layout(paper_bgcolor = "white",height=750,title_automargin=False,legend_font_size=35,font=dict(color='blue', size=30))
    curve4=px.bar(rep_25.loc[sales_rep],y=sales_rep,color=Date,text_auto=True,title='Retail Sales per rep')
    curve4.update_layout(paper_bgcolor = "white",height=750,font=dict(color='green', size=30))
    curve12= px.imshow(rep_25,x=rep_25.columns,y=rep_25.index,text_auto=True,color_continuous_scale='RdBu_r', aspect="auto",title='Reps Sales YTD')
    curve12.update_xaxes(side="top")
    curve12.update_layout(paper_bgcolor = "white",height=750,title_automargin=False,font=dict(color='blue', size=30))
      
    return[fig_0,curve3,curve4,curve12]

if __name__ == '__main__':
    #Timer(1,open_browser).start();
        
    app.run_server(debug=False)
    app.enable_dev_tools(debug=True)
