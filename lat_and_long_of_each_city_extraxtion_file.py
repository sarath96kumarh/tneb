import pickle

ind_data=pd.read_csv('india_city_with_name_along_latlog.csv')
city_name={}  #ind_data.iloc[:,1].to_list()

lat_long_dic_list=[]
for ind in range(len(ind_data)):
    lat_long_dic_list.append({'lat':ind_data.iloc[:,2][ind],'lon':ind_data.iloc[:,3][ind]})
    city_name[str(ind_data.iloc[:,2][ind])+'_'+str(ind_data.iloc[:,3][ind])]=ind_data.iloc[:,1][ind]
        



with open(r"C:\Users\SARATHH\internal_data_manupulation (1)\webpage_flask\web_app\Diamler_project\rev_heat_map_project\india_geo_data\lat_long_dic_list.txt", "wb") as fp:   #Pickling
    pickle.dump(lat_long_dic_list, fp)
with open(r"C:\Users\SARATHH\internal_data_manupulation (1)\webpage_flask\web_app\Diamler_project\rev_heat_map_project\india_geo_data\city_name.p", 'wb') as fp:
    pickle.dump(city_name, fp, protocol=pickle.HIGHEST_PROTOCOL)
