from pymongo import  MongoClient
import csv
import random
import pandas as pd
import numpy as np
    
#data_population():
with open('supplier_name.csv', newline='') as f:
      read_suppli_name=csv.reader(f)
      list_name=list(read_suppli_name)
      supplier_name_list=list_name[0]
      supplier_name=(random.choices(supplier_name_list, k = 10000))
      spare_parts_list=['engine','clutch','transmission gears','differential unit','final drive','rear wheels','front wheel','steering mechanism' ,'hydraulic','Brakes','power takeoff units' ,'tractor pulley' ,'contol panel']
      spare_parts=(random.choices(spare_parts_list, k = 10000))
      year_list=[ss for ss in range(1970,2021)]
      year=(random.choices(year_list, k = 10000))
      df = pd.DataFrame(list(zip(supplier_name,spare_parts,year)), columns = ["supplier_name", "spare_parts","year"])
      df=df.drop_duplicates()
      spend=random.choices(np.arange(100000, 1000000, 14335),k=10000)[:len(df)]   #[random.randrange()]
      revenue=random.choices(np.arange(245790, 3570980, 14335),k=10000)[:len(df)]
      high=random.choices(np.arange(10000,40000),k=10000)
      low=random.choices(np.arange(1000,10000),k=10000)
      sale=[][:len(df)]
      for ss in revenue:
          if ss >200000:
               sale.append(random.choice(high))
          else:
              sale.append(random.choice(low))
      df['spend']=spend
      df['revenue']=revenue
      df['sale']=sale
      data=df.to_dict('records')
print(data)

'''

client=MongoClient('mongodb+srv://sarath:ronaldo@cluster0.bylev.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db=client.get_database('enbot')
records=db.supplier
records.insert_many(data,ordered=False)
'''