import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output  
from plotly.subplots import make_subplots

app = dash.Dash()  




app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'DAIMLER TRUCK INSIGHT', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),

        dcc.RadioItems(id = 'radioitems',
    options=[
        {'label': 'RPM', 'value': 'RPM'},
        {'label': 'Torque', 'value': 'Torque'},
        {'label': 'Distance_covered_gear_wise', 'value': 'Distance_covered_gear_wise'}
    ],
    value='Torque',
    labelStyle={'display': 'inline-block'}
     ),
     dcc.Dropdown( id = 'dropdown',
        options = [
            {'label':'Distance For All Gear', 'value':'default' },
            {'label':'Neutral to All Gear ration','value':['row_sum','neutral']},
            {'label': 'Engine', 'value':'engine_row_wise_precentage'},
            {'label': 'Neutral', 'value':'neutral_precentage'},
            {'label':'Crawler','value':'cr_precentage'},
            {'label':'First Gear','value':'1_precentage'},
            {'label':'Second Gear','value':'2_precentage'},
            {'label':'Third Gear','value':'3_precentage'},
            {'label':'Fourth Gear','value':'4_precentage'},
            {'label':'Fivth Gear','value':'5_precentage'},
            {'label':'Sixth Gear','value':'6_precentage'},
            {'label':'Seventh Gear','value':'7_precentage'},
            {'label':'Eighth Gear','value':'8_precentage'}
            ],
        value = 'engine_row_wise_precentage'),
        dcc.Graph(id = 'bar_plot')
    ])


@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')],
              [Input(component_id='radioitems', component_property= 'value')])

def select_data(dropdown_value,radioitems_value):
    global fig
    print(dropdown_value,radioitems_value)
    pre_list=['engine_row_wise_precentage',
            'neutral_precentage','cr_precentage',
             '1_precentage','2_precentage','3_precentage','4_precentage'
             ,'5_precentage','6_precentage','7_precentage','8_precentage' ]
    
    if radioitems_value=='RPM':
        df=pd.read_csv(r'C:\Users\SARATHH\internal_data_manupulation (1)\webpage_flask\web_app\data\rpm_graph_all_value.csv')
        xx='bar_str_rpm'
        if dropdown_value in pre_list:
           yy=dropdown_value
           fig = px.bar(df, x=xx, y=yy, color=yy,
             labels={xx:'Rpm_Range'}, height=400)

           fig.update_layout(title = str(yy.split('_')[0])+' Gear Rev Percentage Across RPM Range ',
                     )

        else :
            print('llllllllllll',dropdown_value)
            fig = go.Figure(data=[go.Bar(
                name = 'All_gear_row_sum',
                x = df[xx],
                y =df[dropdown_value[0]]

            ),
                                go.Bar(
                name = 'neutral',
                x = df[xx],
                y =df[dropdown_value[1]]
            )
            ])


            fig.update_layout(
                title='Neutral to All Gear ration RPM',
                xaxis_title="Rpm_Range"  ,
                yaxis_title="Tot_Rev_Between_Range_For_all_Gr_and_N")

            #fig.add_trace(px.bar(df, x=xx, y=dropdown_value[1],
            #color_continuous_scale='Bluered_r', 
            #labels={dropdown_value[0]:'Total_Rev_Between_Range',xx:'Rpm_Range'}, height=400,).data[0])

            #fig.update_layout(title = 'Neutral to All Gear ration RPM')



    if radioitems_value=='Torque':
        df=pd.read_csv(r'C:\Users\SARATHH\internal_data_manupulation (1)\webpage_flask\web_app\data\torque_graph_all_value.csv')
        xx='bar_str_torque'
        if dropdown_value in pre_list:
           yy=dropdown_value
           fig = px.bar(df, x=xx, y=yy, color=yy,
             labels={xx:'Torque_Range'}, height=400)
           fig.update_layout(title = str(yy.split('_')[0])+' Gear Rev Percentage Across Torque Range ',
                     )
        else:
            print('llllllllllll',dropdown_value)
            fig = go.Figure(data=[go.Bar(
                name = 'All_gear_sum',
                x = df[xx],
                y =df[dropdown_value[0]]

            ),
                                go.Bar(
                name = 'neutral',
                x = df[xx],
                y =df[dropdown_value[1]]
            )
            ])


            fig.update_layout(
                title='Neutral to All Gear ration Torque',
                xaxis_title="Torque_Range"  ,
                yaxis_title="Tot_Rev_Between_Range_For_all_Gr_and_N")

    if radioitems_value=='Distance_covered_gear_wise':
       
        df=pd.read_csv(r'C:\Users\SARATHH\internal_data_manupulation (1)\webpage_flask\web_app\data\distance_traveled_in_each_gear.csv')
        xx='gear'
        yy='Distance_traveled'
        fig = px.bar(df, x=xx, y=yy, color=yy,
             labels={yy:'Distance_covered',xx:'Gears'}, height=400)
        fig.update_layout(title = 'Distance covered in each gear'
            )
    
    return fig  

if __name__ == '__main__': 
    app.run_server()