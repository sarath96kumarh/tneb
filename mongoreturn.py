from pymongo import  MongoClient
import csv
import random
import pandas as pd
import numpy as np

client=MongoClient('mongodb+srv://sarath:ronaldo@cluster0.bylev.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db=client.get_database('enbot')
records=db.supplier
cursor = records.find()
da=list(cursor)
#print(da[0])

p_da=pd.DataFrame(da)
#ss=p_da.groupby(["supplier_name","spare_parts"])["spend"].agg('sum')
#ss=p_da.loc[(p_da['year']>=1996) & (p_da['year']< 1998)]
'''
ssb=p_da.groupby(["spare_parts"], as_index=False)["spend"].agg('sum')

ss=ssb[ssb.spare_parts=='engine']   #=='engine')]
'''
f=p_da[p_da.spare_parts=='engine']
ss=f['spend'].sum()
print(ss)
#print('total_spend '+str(ss['spend'].to_list()[0]))
