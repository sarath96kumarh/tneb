import pandas as pd
import numpy as np
import os
import glob
import plotly.express as px
import pickle
from math import asin, cos, radians, sin, sqrt

from urllib.request import urlopen
import json
#from geopy.geocoders import Nominatim

def Gear_position(file,other_data_save_path):
  gear_data=pd.read_csv(file,encoding="utf8")

  print('ggggggggggggggggggggggg',gear_data.dtypes['LONG'],gear_data.dtypes['LAT'])
  #cleaning data
  gear_ratio_required_data=gear_data[['GDL','RPM','ANR','T','LONG','LAT','ALT','GS']]
  gear_ratio_required_data['GDL']=gear_ratio_required_data['GDL'].astype('str')
  gear_ratio_required_data['RPM']=gear_ratio_required_data['RPM'].astype('str')
  gear_ratio_required_data['ANR']=gear_ratio_required_data['ANR'].astype('str')
  gear_ratio_required_data['T']=gear_ratio_required_data['T']
  gear_ratio_required_data['LONG']=gear_ratio_required_data['LONG'].astype('str')
  gear_ratio_required_data['LAT']=gear_ratio_required_data['LAT'].astype('str')
  gear_ratio_required_data['GS']=gear_ratio_required_data['GS'].astype('str')




  without_null=gear_ratio_required_data[~gear_ratio_required_data.GDL.isin(['nan'])]
  without_null_2=without_null[~without_null.RPM.isin(['nan'])]
  without_null_2=without_null_2[~without_null_2.ANR.isin(['nan'])]
  without_null_2=without_null_2[~without_null_2.LONG.isin(['nan'])]
  without_null_2=without_null_2[~without_null_2.LAT.isin(['nan'])]
  without_null_2=without_null_2[~without_null_2.GS.isin(['nan'])]

  without_null_2['GDL']=without_null_2['GDL'].astype('float')
  without_null_2['RPM']=without_null_2['RPM'].astype('float')
  #without_null_2['RPM']=without_null_2['RPM']
  without_null_2['ANR']=without_null_2['ANR'].astype('float')
  without_null_2['LONG']=without_null_2['LONG'].astype('float')
  without_null_2['LAT']=without_null_2['LAT'].astype('float')
  without_null_2['GS']=without_null_2['GS'].astype('float')
  
  print(without_null_2.RPM.max())
  #outlier removal
  without_null_2=without_null_2[without_null_2.RPM < without_null_2.RPM.max()]
  
  print(without_null_2['RPM'].max())

  #city_name_for_each_lat_lon
  cities=[]
  for ind in without_null_2.index:
    url = "http://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false" % (without_null_2['LAT'][ind], without_null_2['LONG'][ind])
    v = urlopen(url).read()
    j = json.loads(v)
    components = j['results'][0]['address_components']
    country = town = None
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
        if "postal_town" in c['types']:
            town = c['long_name']
    cities.append(country)
    print(country)
  
  #Gear ratio 
  without_null_2['gear_ratio']=without_null_2['GDL']/without_null_2['RPM']
  without_null_2['gear_ratio'] = without_null_2['gear_ratio'].round(decimals = 1)
  
  
  #neutral
  without_null_2['gear'] = ['neutral' if x >15.95 or x<0.9 else 'need' for x in without_null_2['gear_ratio'] ]
  neutral_dataframe=without_null_2[(without_null_2['gear']=='neutral')]
  neutral_dataframe=neutral_dataframe[['GDL','RPM','ANR','T','LONG','LAT','ALT','GS','gear_ratio','gear']]
  #neutral_dataframe.to_csv('neutral.csv')
  

  #other_gears_position
  gear_value=[[15.9,14.5],[14.5,9.4],[9.4,6.6],[6.6,4.8],[4.8,3.6]
            ,[3.6,2.5],[2.5,1.8],[1.8,1.3],[1.3,1]] 
  gear=[['neutral','cr'],['cr','1'],['1','2'],['2','3'],['3','4'],['4','5'],['5','6']
      ,['6','7'],['7','8']]

  final_df=pd.DataFrame(columns=['GDL','RPM','ANR','T','LONG','LAT','ALT','GS','gear_ratio','gear'])
  for ss in range(0,len(gear_value)):
    first_half_mid_way=[gear_value[ss][0]]
    sec_half_mid_way=[gear_value[ss][1]]
    
    
    #mid_point_finder
    while first_half_mid_way[-1]!=sec_half_mid_way[-1] and sec_half_mid_way[-1]!=round(first_half_mid_way[-1]-.1,1) :
      first_half_mid_way.append(round(first_half_mid_way[-1]-.1,1))
      sec_half_mid_way.append(round(sec_half_mid_way[-1]+.1,1))
      
    filter=without_null_2[(without_null_2['gear_ratio'] >= gear_value[ss][1]) & (without_null_2['gear_ratio'] <=gear_value[ss][0] )]
    filter=filter[['GDL','RPM','ANR','T','LONG','LAT','ALT','GS','gear_ratio']]
    filter['gear'] = [gear[ss][0] if x >=first_half_mid_way[-1]  else gear[ss][1] for x in filter['gear_ratio'] ]
    final_df=pd.concat([final_df,filter])
  
  
  #final_df.to_csv('without_neutral.csv')
  save_dataframe_data=pd.concat([neutral_dataframe,final_df],ignore_index=True)
  save_dataframe_data['Vehicle']=str(str(file.split('/')[-1])).split('.')[0]
  
  
  # initialize Nominatim API
  #geolocator = Nominatim(user_agent="geoapiExercises")
  
  save_dataframe_data.to_csv(other_data_save_path+'Gear_ratio_with_gear.csv')
  
  
  #RPM range
  rpm_max=save_dataframe_data['RPM'].max()
  rpm_min=save_dataframe_data['RPM'].min()
  rpm_range_list=[[round(rpm_min),round(rpm_min)+150]]
  while rpm_range_list[-1][1]<=rpm_max:
           rpm_range_list.append([rpm_range_list[-1][1]+1,rpm_range_list[-1][1]+1+150])


  #torque range
  torque_max=   1500                                        #save_dataframe_data['ANR'].max()
  torque_min=    -1500                                        #save_dataframe_data['ANR'].min()

  torque_range_list=[[round(torque_min),round(torque_min)+50]]
  while torque_range_list[-1][1]<=torque_max:
           torque_range_list.append([torque_range_list[-1][1]+1,torque_range_list[-1][1]+1+50])

  print(torque_range_list[-10:])
  #range_combination_rpm_tor_gearv
  rpm_tor_comb=[]
  gear_pos=['neutral','cr','1','2','3','4','5','6','7','8','9']

  for ssn in rpm_range_list:
    for ssk in torque_range_list:
      for gg in gear_pos:
        rpm_tor_comb.append([ssn,ssk,gg])
  
  
  #gear_wise_filter
  gear_wise_filter=[]
  append_list=[]

  for qq in gear_pos:
    if append_list:
      gear_wise_filter.append(append_list)
      append_list=[]
    for kkl in rpm_tor_comb:
          if kkl[-1] == qq:
              append_list.append(kkl)
  
  #-----print('gear-wise_filter',gear_wise_filter[:3])
  #calculation_data
  calculation_data=[]
  con_calculation_data=[]
  
  #function_to_calculated_timeframecount_accros_tor_rpm_gear_&&_formula_cal
  def rotation_calculation(gear_wise_combo):
    gears_to_be_calculated_for=gear_wise_combo[0][-1]
    data_for_gear_to_be_calculated_only=save_dataframe_data[
                                        (save_dataframe_data['gear'] == str(gears_to_be_calculated_for))]
    

    def count_of_time_stamp_inrange(single_data_range):
        ccount=len(data_for_gear_to_be_calculated_only[
                                ((data_for_gear_to_be_calculated_only['RPM']>=single_data_range[0][0])&(data_for_gear_to_be_calculated_only['RPM']<=single_data_range[0][1])) 
                                 & 
                                ((data_for_gear_to_be_calculated_only['ANR']>=single_data_range[1][0])&(data_for_gear_to_be_calculated_only['ANR']<=single_data_range[1][1]))
                     
                                                      ]
                  )
        
        
        rpmss_f=(round((single_data_range[0][0]+single_data_range[0][1])/2)/60)*(ccount*5)
        calculation_data.append([single_data_range[1][0],single_data_range[1][1],single_data_range[0][0],single_data_range[0][1],
                                                gears_to_be_calculated_for,ccount,rpmss_f])

        
        #continous_timeframe
        
        if ccount==1:
            #print('running')
            can_data=data_for_gear_to_be_calculated_only[
                                ((data_for_gear_to_be_calculated_only['RPM']>=single_data_range[0][0])&(data_for_gear_to_be_calculated_only['RPM']<=single_data_range[0][1])) 
                                 & 
                                ((data_for_gear_to_be_calculated_only['ANR']>=single_data_range[1][0])&(data_for_gear_to_be_calculated_only['ANR']<=single_data_range[1][1]))           
                                                         ]  

            rpm_conx=(round((single_data_range[0][0]+single_data_range[0][1])/2)/60)*(1*5)

            con_calculation_data.append([single_data_range[1][0],single_data_range[1][1],single_data_range[0][0],
                                          single_data_range[0][1],can_data['T'].to_list(),can_data['LONG'].to_list(),can_data['LAT'].to_list(),
                                          can_data['ALT'].to_list(), can_data['GS'].to_list(),gears_to_be_calculated_for,1,rpm_conx])                                         
        if ccount>1:
            can_data=data_for_gear_to_be_calculated_only[
                                ((data_for_gear_to_be_calculated_only['RPM']>=single_data_range[0][0])&(data_for_gear_to_be_calculated_only['RPM']<=single_data_range[0][1])) 
                                 & 
                                ((data_for_gear_to_be_calculated_only['ANR']>=single_data_range[1][0])&(data_for_gear_to_be_calculated_only['ANR']<=single_data_range[1][1]))           
                                                         ]
            can_data.reset_index(inplace=True)    
            
            dt_data=pd.to_datetime(can_data['T'])
            
            start_index=0
            #hour=[00,23]
            #min=[00,59]
            end_index=0
            
            
            for kk in range(0,len(dt_data)):
              list_for_lat_lon_gps=[]
              try:
                  dif=dt_data[kk+1]-dt_data[kk]
                  d=str(dif).split(' ')[0]
                  h=str(dif).split(' ')[2].split(':')[0]
                  m=str(dif).split(' ')[2].split(':')[1]
                  
                  if int(d)!=0 or int(h)!=00 or int(m)!=00:
                    #print('kkk',kk) #
                    
                    end_index=kk
                    #print('running')
                    # print('running',start_index,end_index) #
                    loc_time_col=['T','LONG','LAT','ALT','GS']
                    for cok in loc_time_col:
                        list_for_lat_lon_gps.append(can_data.loc[start_index:end_index][cok].to_list())
                    countinous_count=len(can_data.loc[start_index:end_index])
                    
                    rpm_con=(round((single_data_range[0][0]+single_data_range[0][1])/2)/60)*(countinous_count*5)
                    # print('con+len',countinous_count,'rpm',rpm_con) #
                    #print('impo',list_for_lat_lon_gps) #
                    con_calculation_data.append([single_data_range[1][0],single_data_range[1][1],single_data_range[0][0],
                                                single_data_range[0][1],list_for_lat_lon_gps[0],
                                                list_for_lat_lon_gps[1],list_for_lat_lon_gps[2],list_for_lat_lon_gps[3],
                                                list_for_lat_lon_gps[4],gears_to_be_calculated_for,countinous_count,rpm_con])
                    start_index=end_index+1
                    
                  else:
                    #print('else_check')
                    kkvskl=00
              except Exception :
                       print('indexs')    
            #print(con_calculation_data) #
            #print(len(con_calculation_data)) #
            

    for xxt in gear_wise_combo:
         count_of_time_stamp_inrange(xxt)
         
    
  #print(len(gear_wise_filter)) #
  for yy in gear_wise_filter:
    #print('gggggggg',len(yy)) #
    rotation_calculation(yy)
    
    
  

  return calculation_data,con_calculation_data,other_data_save_path


#source_data

file_name=os.listdir(r'C:\Users\SARATHH\internal_data_manupulation (1)\webpage_flask\web_app\Diamler_project\54t')
path_of_fol=r'C:\Users\SARATHH\internal_data_manupulation (1)\webpage_flask\web_app\Diamler_project\54t'
combined_csv = pd.concat([pd.read_csv(path_of_fol+'/'+f) for f in file_name ])
combined_csv.to_csv('C:/Users/SARATHH/internal_data_manupulation (1)/webpage_flask/web_app/Diamler_project/combined_data/'+str(file_name[0].split("_")[0])+'.csv', 
                    index=False, encoding='utf-8-sig')
gear_pos_run,gear_pos_run_con,other_data_save_path=Gear_position('C:/Users/SARATHH/internal_data_manupulation (1)/webpage_flask/web_app/Diamler_project/combined_data/'+str(file_name[0].split("_")[0])+'.csv',
                'C:/Users/SARATHH/internal_data_manupulation (1)/webpage_flask/web_app/Diamler_project/rev_heat_map_project/other_data_file_returned_from_code_creation_file/')



def Writing_cal_and_con_cal_result_with_tor_rpm_rev_matrix(gear_pos_run,gear_pos_run_con,other_data_save_path):
  #Writing_calculated_result
  cal_result=pd.DataFrame(gear_pos_run,columns=['torque_y1','torque_y2','RPM_x1','RPM_x2',
                                                'Gear','Count_of_Timeframe_fall_across_tor_rpm_gear',
                                                'Formula_value'])
  cal_result['vehicle']='c'+str(file_name[0].split('_')[0])
  cal_result.to_csv(other_data_save_path+'calculation_across_tor_rpm_gear.csv')

  
  #torque alone revolution
  torque_alone_rev=cal_result.groupby(['torque_y1','torque_y2','Gear'])['Formula_value'].agg('sum').reset_index()
  torque_alone_rev.to_csv('testing_groupby_function.csv')
  torque_alone_rev[['torque_y1','torque_y2','Gear','Formula_value']].to_csv(other_data_save_path+'torque_alone_range_rev.csv')
  
  #RPM alone 
  rpm_alone=cal_result.groupby(['RPM_x1','RPM_x2','Gear'])['Formula_value'].agg('sum').reset_index()
  rpm_alone['vehicle']='c'+str(file_name[0].split('_')[0])
  rpm_alone[['RPM_x1','RPM_x2','Gear','Formula_value']].to_csv(other_data_save_path+'rpm_alone_range.csv')
  
  
  #tor matrix
  gear=['torque1','torque2','neutral','cr','1','2','3','4','5','6','7','8']
  list_gear_wise=[]
  tor_pat=[]
  ttor=0
  for pvd in gear:
    if ttor<2:
      print('1')
      if ttor==0:
        tor_pat.append(torque_alone_rev[(torque_alone_rev['Gear'] == 'neutral')]['torque_y1'].to_list())
        
        list_gear_wise.append(tor_pat[0])
        ttor+=1
        continue

      if ttor==1:
        tor_pat.append(torque_alone_rev[(torque_alone_rev['Gear']=='neutral')]['torque_y2'].to_list())
        list_gear_wise.append(tor_pat[1])
        ttor+=1
        continue
    list_gear_wise.append(torque_alone_rev[(torque_alone_rev['Gear'] == pvd)]['Formula_value'].to_list())

  columnss=['torque1','torque2','neutral','cr','1','2','3','4','5','6','7','8']
  print(len(list_gear_wise))
  dictionary = dict(zip(columnss, list_gear_wise))

  ff_res=pd.DataFrame.from_dict(dictionary)
  ff_res['vehicle']='c'+str(file_name[0].split('_')[0])
  ff_res.to_csv(other_data_save_path+'tor_gear_matrix.csv')

  
  #rpm matrix

  gear_rpm=['rpm1','rpm2','neutral','cr','1','2','3','4','5','6','7','8']
  list_gear_wise_rpm=[]
  rpm_pat=[]
  rrpm=0
  for pvd in gear_rpm:
    if rrpm<2:
      print('1')
      if rrpm==0:
        rpm_pat.append(rpm_alone[(rpm_alone['Gear'] == 'neutral')]['RPM_x1'].to_list())
        list_gear_wise_rpm.append(rpm_pat[0])
        rrpm+=1
        continue

      if rrpm==1:
        rpm_pat.append(rpm_alone[(rpm_alone['Gear']=='neutral')]['RPM_x2'].to_list())
        list_gear_wise_rpm.append(rpm_pat[1])
        rrpm+=1
        continue
    list_gear_wise_rpm.append(rpm_alone[(rpm_alone['Gear'] == pvd)]['Formula_value'].to_list())

  columnss_rpm=['rpm1','rpm2','neutral','cr','1','2','3','4','5','6','7','8']
  print(len(list_gear_wise_rpm))
  dictionary_rpm = dict(zip(columnss_rpm, list_gear_wise_rpm))

  ff_res_rpm=pd.DataFrame.from_dict(dictionary_rpm)
  ff_res_rpm['vehicle']='c'+str(file_name[0].split('_')[0])
  ff_res_rpm.to_csv(other_data_save_path+'rpm_gear_matrix.csv')


  #Writing_con_calculated_result
  con_cal_result=pd.DataFrame(gear_pos_run_con,columns=['torque_y1','torque_y2','RPM_x1','RPM_x2',
                                                        'TIME','LONG','LAT','ALT','GS',
                                                        'Gear','Con_Count_of_Timeframe_fall_across_tor_rpm_gear',
                                                        'Formula_value'])
  con_cal_result['vehicle']='c'+str(file_name[0].split('_')[0])
  con_cal_result.to_csv('continues_calculation_across_tor_rpm_gear_time_wise_continue_split.csv')

  return ff_res,ff_res_rpm,other_data_save_path




def torque_rpm_graph_data_and_distance_gear_wise(ff_res,ff_res_rpm,heat_graph_save_path,distance_path):

  #torque graph value

  s_data=ff_res  #pd.read_csv('tor_gear_matrix.csv')
  s_data=s_data[['torque1','torque2','neutral','cr','1','2','3','4','5','6','7','8']]
  use_s_data=s_data[['neutral','cr','1','2','3','4','5','6','7','8']]
  sum_col_wise=use_s_data.sum(axis = 0, skipna = True)

  overall_row_which_hold_sum_of_each_col_sum=sum_col_wise.sum(axis=0,skipna=True)
  print(sum_col_wise)
  print(overall_row_which_hold_sum_of_each_col_sum)
  #print(type(s_data['neutral']/sum_col_wise['neutral']))
  name_list=['neutral_precentage','cr_precentage','1_precentage',
          '2_precentage','3_precentage','4_precentage','5_precentage',
            '6_precentage','7_precentage','8_precentage']
  cal_list=['neutral','cr','1','2','3','4','5','6','7','8']
  for ssk in range(0,len(name_list)):
      s_data[name_list[ssk]]=s_data[cal_list[ssk]]/sum_col_wise[cal_list[ssk]]

  #s_data['neutral_precentage']=s_data['neutral']/sum_col_wise['neutral']
  #row_s_data=s_data[['neutral','cr','1','2','3','4','5','6','7','8']]
  s_data['bar_str_torque']=s_data['torque1'].astype(str)+' to '+s_data['torque2'].astype(str)
  sum_row_wise=use_s_data.sum(axis = 1, skipna = True)
  s_data['row_sum']=sum_row_wise
  s_data['neutral_ration_in_each_row_sum']=s_data['neutral']/sum_row_wise
  s_data['engine_row_wise_precentage']=sum_row_wise/overall_row_which_hold_sum_of_each_col_sum
  gear_ratio=[15.95,14.573,9.478,6.635,4.821,3.667,2.585,1.81,1.315,1]
  total_rev_gear_list=sum_col_wise.to_list()
  print(total_rev_gear_list)
  final_value=[]
  for ll in range(0,len(gear_ratio)):
      print('DDDDDDDDDD',total_rev_gear_list[ll])
      final_value.append(2*3.14*(0.534/1000)*(total_rev_gear_list[ll]/(gear_ratio[ll]*4.55)))
  s_data['vehicle']='c'+str(file_name[0].split('_')[0])
  s_data.to_csv(heat_graph_save_path+'torque_graph_all_value.csv')
  print(len(cal_list),len(final_value))



  

  # rpm graph value

  s_data_rpm=ff_res_rpm  #pd.read_csv('tor_gear_matrix.csv')
  s_data_rpm=s_data_rpm[['rpm1','rpm2','neutral','cr','1','2','3','4','5','6','7','8']]
  use_s_data_rpm=s_data_rpm[['neutral','cr','1','2','3','4','5','6','7','8']]
  sum_col_wise_rpm=use_s_data_rpm.sum(axis = 0, skipna = True)
  overall_row_which_hold_sum_of_each_col_sum_rpm=sum_col_wise_rpm.sum(axis=0,skipna=True)
  print(sum_col_wise_rpm)
  print(overall_row_which_hold_sum_of_each_col_sum_rpm)
  #print(type(s_data_rpm['neutral']/sum_col_wise_rpm['neutral']))
  name_list_rpm=['neutral_precentage','cr_precentage','1_precentage',
          '2_precentage','3_precentage','4_precentage','5_precentage',
            '6_precentage','7_precentage','8_precentage']
  cal_list_rpm=['neutral','cr','1','2','3','4','5','6','7','8']
  for ssk_rpm in range(0,len(name_list_rpm)):
      s_data_rpm[name_list_rpm[ssk_rpm]]=s_data_rpm[cal_list_rpm[ssk_rpm]]/sum_col_wise_rpm[cal_list_rpm[ssk_rpm]]

  #s_data_rpm['neutral_precentage']=s_data_rpm['neutral']/sum_col_wise_rpm['neutral']
  sum_row_wise_rpm=use_s_data_rpm.sum(axis = 1, skipna = True)
  s_data_rpm['bar_str_rpm']=s_data_rpm['rpm1'].astype(str)+' to '+s_data_rpm['rpm2'].astype(str)
  s_data_rpm['row_sum']=sum_row_wise_rpm
  s_data_rpm['neutral_ration_in_each_row_sum']=s_data_rpm['neutral']/sum_row_wise_rpm
  s_data_rpm['engine_row_wise_precentage']=sum_row_wise_rpm/overall_row_which_hold_sum_of_each_col_sum_rpm


  fig_rpm = px.bar(s_data_rpm, x='bar_str_rpm', y='engine_row_wise_precentage', color='engine_row_wise_precentage',
              labels={'engine_row_wise_precentage':'engine_rev','bar_str_rpm':'rpm'}, height=400)
  fig_rpm.write_html("rpm_bar_plot.html")
  s_data_rpm['vehicle']='c'+str(file_name[0].split('_')[0])
  #gear_ratio_rpm=[15.95,14.573,9.478,6.635,4.821,3.667,2.585,1.81,1.315,1]
  #total_rev_gear_list_rpm=sum_col_wise_rpm.to_list()
  #final_value_rpm=[]
  #for ll in range(0,len(gear_ratio_rpm)):
      #final_value_rpm.append(2*3.14*(0.534/1000)*(total_rev_gear_list_rpm[ll]/(gear_ratio_rpm[ll]*4.55)))
  s_data_rpm.to_csv(heat_graph_save_path+'rpm_graph_all_value.csv')





  #Distance_calculation
  final_value=pd.DataFrame([cal_list,final_value]).transpose()
  final_value.columns=['gear','Distance_traveled']
  final_value.to_csv(heat_graph_save_path+'distance_traveled_in_each_gear.csv')
  #fig_tor = px.bar(s_data, x='bar_str_torque', y='engine_row_wise_precentage', color='engine_row_wise_precentage',
             #labels={'engine_row_wise_precentage':'engine_rev','bar_str_torque':'torque'}, height=400)
  #fig_tor.write_html("tor_bar_plot.html")




ff_res,ff_res_rpm=Writing_cal_and_con_cal_result_with_tor_rpm_rev_matrix(gear_pos_run,gear_pos_run_con,other_data_save_path)
run_final=torque_rpm_graph_data_and_distance_gear_wise(ff_res,ff_res_rpm,
                 'C:/Users/SARATHH/internal_data_manupulation (1)/webpage_flask/web_app/Diamler_project/rev_heat_map_project/rev_heat_map_project_using_data/')

#torque_alone_rev['torque']=(torque_alone_rev['torque_y1']+torque_alone_rev['torque_y2'])/2
#torque_alone_rev[['Gear','torque','Formula_value']].to_excel('torque_alone_revolution.xlsx')




















