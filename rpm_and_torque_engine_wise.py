import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


s_data=pd.read_csv('tor_gear_matrix.csv')
s_data=s_data[['neutral','cr','1','2','3','4','5','6','7','8']]
sum_col_wise=s_data.sum(axis = 0, skipna = True)
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

sum_row_wise=s_data.sum(axis = 1, skipna = True)
s_data['row_sum']=sum_row_wise
s_data['neutral_ration_in_each_row_sum']=s_data['neutral']/sum_row_wise
s_data['engine_row_wise_precentage']=sum_row_wise/overall_row_which_hold_sum_of_each_col_sum
gear_ratio=[15.95,14.573,9.478,6.635,4.821,3.667,2.585,1.81,1.315,1]
total_rev_gear_list=sum_col_wise.to_list()
final_value=[]
for ll in range(0,len(gear_ratio)):
    final_value.append(2*3.14*(0.534/1000)*(total_rev_gear_list[ll]/(gear_ratio[ll]*4.55)))
s_data.to_csv('testt.csv')
print(len(gear_ratio),len(total_rev_gear_list),'sssssssssss',final_value)
pd.DataFrame(final_value).to_csv('Distance_covered_gear_wise.csv')
#plt.title('Distance_covered_gear_wise [86.6658321471799, 0.0034981416032988663, 0.007335639502672972, 0.0, 0.0, 0.0, 8.555929824118147, 225.66784387695802, 110.98792489850622, 2542.0022479979225]')
f_d=pd.DataFrame(
    {'gear': cal_list,
     'dis': final_value,
     })
kq=sns.barplot(x='gear', y='dis',data=f_d)
kq.set_title('Distance_covered_gear_wise'
            , fontsize = 20)
for index, row in f_d.iterrows():
    kq.text(row.name,row.dis, round(row.dis,1), color='black', ha="center")
plt.savefig('plt_Distance_covered_gear_wise')



