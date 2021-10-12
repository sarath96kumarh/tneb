import pandas as pd
import numpy as np


gear_data=pd.read_csv(r'C:\Users\SARATHH\internal_data_manupulation\internal_data.csv')

gear_ration_required_data=gear_data[['GDL','RPM']]
gear_ration_required_data['GDL']=gear_ration_required_data['GDL'].astype('str')
gear_ration_required_data['RPM']=gear_ration_required_data['RPM'].astype('str')
print(len(gear_ration_required_data))


without_null=gear_ration_required_data[~gear_ration_required_data.GDL.isin(['nan'])]
without_null_2=without_null[~without_null.RPM.isin(['nan'])]
print(len(without_null_2))



without_null_2['GDL']=without_null_2['GDL'].astype('float')
without_null_2['RPM']=without_null_2['RPM'].astype('float')
without_null_2['gear_ration']=without_null_2['GDL']/without_null_2['RPM']
without_null_2['gear_ration'] = without_null_2['gear_ration'].round(decimals = 1)
print(without_null_2.dtypes)
#neutral

without_null_2['gear'] = ['neutral' if x >17.5 and x<0.9 else 'need' for x in without_null_2['gear_ration'] ]
  

without_null_2['gear'] = np.where(without_null_2['gear_ration']>17.5,without_null_2['gear_ration'], 'neutral')
without_null_2['gear'] = np.where(without_null_2['gear_ration']<0.9,without_null_2['gear_ration'], 'neutral')


#rest_othe_gears

testttt=without_null_2[(without_null_2['gear_ration'] >=1) &  (without_null_2['gear_ration'] <1.3) ]
testttt.to_csv('test.csv')
without_null_2.to_csv('gear_ratio.csv')
#pd.DataFrame(without_null_2['gear_ration'].unique()).to_csv('unique_gear_ratio.csv')