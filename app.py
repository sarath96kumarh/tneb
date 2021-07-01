from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS,cross_origin
import requests
#import pymongo
import json
import os
from pymongo import  MongoClient
from bson import json_util
import pandas as pd
#from saveConversation import saveConversation
#from pymongo import MongoClient







app = Flask(__name__)  # initialising the flask app with the name 'app'


# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    #client=MongoClient('mongodb+srv://sarath:ronaldo@cluster0.bylev.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    #db=client.get_database('enbot')
    #records=db.supplier
    #cursor = records.find()
    #da=list(cursor)
    #p_da=pd.DataFrame(da)
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):
    # dbConn = pymongo.MongoClient("mongodb://localhost:27017/")  # opening a connection to Mongo
    #log = Conversations.Log()
    sessionID = req.get('responseId')
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')
    query_text = result.get("queryText")
    parameters = result.get("parameters")
    cust_name = parameters.get("cust_name")
    cust_contact = parameters.get("cust_contact")
    cust_email = parameters.get("cust_email")
    #db = configureDataBase()
    client=MongoClient('mongodb+srv://sarath:ronaldo@cluster0.bylev.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db=client.get_database('enbot')
    records=db.supplier
    cursor = records.find()
    da=list(cursor)
    p_da=pd.DataFrame(da)

    if intent == 'supplier_option - total_spend - custom':
        
        user_replace=query_text.replace('  ',' ')
        user_split=user_replace.split(' ')
        year_count=[ss for ss in user_split if ss.isnumeric()]
        spare_parts=['engine','clutch','Brakes','hydraulic']
        two_string_spare_parts=['transmission','differential',
                   'final','rear','front','steering',
                   'tractor','control']
        three_string_spare_parts=['power']
        user_given_spare_parts=[]
        for dd in range(0,len(user_split)):
            if user_split[dd] in spare_parts:
                user_given_spare_parts.append(user_split[dd])
            if user_split[dd] in two_string_spare_parts:
                user_given_spare_parts.append(user_split[dd]+' '+user_split[dd+1])
            if user_split[dd] in three_string_spare_parts:
                user_given_spare_parts.append(user_split[dd]+' '+user_split[dd+1]+' '+user_split[dd+2])
        if len(year_count)==2:
            index_of_end_year=user_split.index(year_count[-1])
            word_seperate_two_year=user_split[index_of_end_year-1].lower()
            if word_seperate_two_year=='to':
                y_between=p_da.loc[(p_da['year']>=int(year_count[0])) & (p_da['year']<=int(year_count[1]))]
                spare_wise_sum=y_between[y_between.spare_parts==user_given_spare_parts[0]]                              #y_between.groupby(["spare_parts"], as_index=False)["spend"].agg('sum')
                spare_wise_table=spare_wise_sum[["supplier_name","spare_parts","revenue"]]
                result_spend=spare_wise_sum['spend'].sum()
                return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "Total spend made in "+ user_given_spare_parts[0]+' '+'from '+year_count[0]+' to '+year_count[1]+' is '+str(result_spend)
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }
            if word_seperate_two_year=='and':
                y1=p_da.loc[(p_da['year']==int(year_count[0]))] 
                spare1=y1[y1.spare_parts==user_given_spare_parts[0]] 
                spare1_tab=spare1[["supplier_name","spare_parts","revenue"]]
                result_spend1=spare1['spend'].sum()
                y2=p_da.loc[(p_da['year']== int(year_count[1]))]
                spare2=y2[y2.spare_parts==user_given_spare_parts[0]] 
                spare2_tab=spare2[["supplier_name","spare_parts","revenue"]]
                result_spend2=spare2['spend'].sum()
                return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "total spend made in "+year_count[0]+' for '+user_given_spare_parts[0]+' is '+str(result_spend1)+' and '+str(result_spend2)+' in '+year_count[1]
                                ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }

        if len(year_count)==1:
            y=p_da.loc[(p_da['year']==int(year_count[0]))] 
            spare=y[y.spare_parts==user_given_spare_parts[0]] 
            spare_tavle=spare[["supplier_name","spare_parts","revenue"]]
            result_spend_single=spare['spend'].sum()
            return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "total spend made in "+year_count[0]+' for '+user_given_spare_parts[0]+' is '+str(result_spend_single)
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }

    if intent =='supplier_option - highest sales - number of supplier':
        user_replace=query_text.replace('  ',' ')
        user_split=user_replace.split(' ')
        top_count=[]
        year=[]
        for ss in user_split:
            if ss.isnumeric() and int(ss)<=100:
                top_count.append(ss)
            if ss.isnumeric() and int(ss)>1970 and int(ss)<2021:
                 year.append(ss)
        spare_parts=['engine','clutch','Brakes','hydraulic']
        two_string_spare_parts=['transmission','differential',
                   'final','rear','front','steering',
                   'tractor','control']
        three_string_spare_parts=['power']
        user_given_spare_parts=[]
        for dd in range(0,len(user_split)):
            if user_split[dd] in spare_parts:
                user_given_spare_parts.append(user_split[dd])
            if user_split[dd] in two_string_spare_parts:
                user_given_spare_parts.append(user_split[dd]+' '+user_split[dd+1])
            if user_split[dd] in three_string_spare_parts:
                user_given_spare_parts.append(user_split[dd]+' '+user_split[dd+1]+' '+user_split[dd+2])
        
        

        #return {
               #"print":[top_count,year,user_given_spare_parts]
               #}

        if len(user_given_spare_parts)==1 or len(user_given_spare_parts)==0 :
            if len(year)==0:
                return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "please try again by  mentioning for which year insight is need"
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }

            if top_count and len(user_given_spare_parts)==1 and len(year)==1:
                y_filter=p_da[p_da.year ==int(year[0])]
                sale_group=y_filter.groupby(["supplier_name","spare_parts"], as_index=False)["sale"].agg('sum')
                spec_part=sale_group[sale_group.spare_parts==user_given_spare_parts[0]]
                sorted_sale=spec_part.sort_values('sale',ascending=False)
                

                return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "Top 10 suppliers list "+str(sorted_sale['supplier_name'].iloc[0:10].to_list())+" and there sale list "+str(sorted_sale['sale'].iloc[0:10].to_list())+' for '+user_given_spare_parts[0]+' in '+year[0]
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }

            if len(top_count)==0 and len(user_given_spare_parts)==1  and len(year)==1:
                y_filter=p_da[p_da.year ==int(year[0])]
                sale_group=y_filter.groupby(["supplier_name","spare_parts"], as_index=False)["sale"].agg('sum')
                spec_part=sale_group[sale_group.spare_parts==user_given_spare_parts[0]]
                sorted_sale=spec_part.sort_values('sale',ascending=False)
                return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "Top 10 suppliers list "+str(sorted_sale['supplier_name'].iloc[0:10].to_list())+" and there sale list "+str(sorted_sale['sale'].iloc[0:10].to_list())+' for '+user_given_spare_parts[0]+' in '+year[0]
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }

            if len(top_count)==1 and len(user_given_spare_parts)==0 and len(year)==1:
                
                return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "please try again by mentioning anyone of the department given to get insight  ==> 1 engine  2 clutch   3 transmission gears   4 differential unit    5 final drive    6 rear wheels    7 front wheel   8 steering mechanism   9  hydraulic control    10 Brakes   11 power takeoff units   12 tractor pulley  13 contol panel " 
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }



            if len(top_count)==0 and len(user_given_spare_parts)==0 and len(year)==1:
                return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "please try again by mentioning anyone of the department given to get insight  ==> 1 engine  2 clutch   3 transmission gears   4 differential unit    5 final drive    6 rear wheels    7 front wheel   8 steering mechanism   9  hydraulic control    10 Brakes   11 power takeoff units   12 tractor pulley  13 contol panel " 
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }



            if top_count and len(user_given_spare_parts)==1 and len(year)==2:
                         
                y_filter=p_da.loc[(p_da['year']>=int(year[0])) & (p_da['year']< int(year[1]))]
                sale_group=y_filter.groupby(["supplier_name","spare_parts"], as_index=False)["sale"].agg('sum')
                spec_part=sale_group[sale_group.spare_parts==user_given_spare_parts[0]]
                sorted_sale=spec_part.sort_values('sale',ascending=False)
                return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "Top 10 suppliers list "+str(sorted_sale['supplier_name'].iloc[0:10].to_list())+" and there sale list "+str(sorted_sale['sale'].iloc[0:10].to_list())+' for '+user_given_spare_parts[0]+' from '+year[0]+' to '+year[1]
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }

            if len(top_count)==0 and len(user_given_spare_parts)==1  and len(year)==2:
                y_filter=p_da.loc[(p_da['year']>=int(year[0])) & (p_da['year']< int(year[1]))]
                sale_group=y_filter.groupby(["supplier_name","spare_parts"], as_index=False)["sale"].agg('sum')
                spec_part=sale_group[sale_group.spare_parts==user_given_spare_parts[0]]
                sorted_sale=spec_part.sort_values('sale',ascending=False)
                return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "Top 10 suppliers list "+str(sorted_sale['supplier_name'].iloc[0:10].to_list())+" and there sale list "+str(sorted_sale['sale'].iloc[0:10].to_list())+' for '+user_given_spare_parts[0]+' from '+year[0]+' to '+year[1]
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }

            if len(top_count)==1 and len(user_given_spare_parts)==0 and len(year)==2:
                return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "please try again by mentioning anyone of the department given to get insight  ==> 1 engine  2 clutch   3 transmission gears   4 differential unit    5 final drive    6 rear wheels    7 front wheel   8 steering mechanism   9  hydraulic control    10 Brakes   11 power takeoff units   12 tractor pulley  13 contol panel " 
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }

            if len(top_count)==0 and len(user_given_spare_parts)==0 and len(year)==2:
                return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "please try again by mentioning anyone of the department given to get insight  ==> 1 engine  2 clutch   3 transmission gears   4 differential unit    5 final drive    6 rear wheels    7 front wheel   8 steering mechanism   9  hydraulic control    10 Brakes   11 power takeoff units   12 tractor pulley  13 contol panel " 
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }

    if intent=='supplier_option - list of suppliers - department':
        user_replace=query_text.replace('  ',' ')
        user_split=user_replace.split(' ')
        spare_parts=['engine','clutch','Brakes','hydraulic']
        two_string_spare_parts=['transmission','differential',
                   'final','rear','front','steering',
                   'tractor','control']
        three_string_spare_parts=['power']
        user_given_spare_parts=[]
        for dd in range(0,len(user_split)):
            if user_split[dd] in spare_parts:
                user_given_spare_parts.append(user_split[dd])
            if user_split[dd] in two_string_spare_parts:
                user_given_spare_parts.append(user_split[dd]+' '+user_split[dd+1])
            if user_split[dd] in three_string_spare_parts:
                user_given_spare_parts.append(user_split[dd]+' '+user_split[dd+1]+' '+user_split[dd+2])
        if  len(user_given_spare_parts)==0:
            return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "please try again by mentioning anyone of the department given to get insight  ==> 1 engine  2 clutch   3 transmission gears   4 differential unit    5 final drive    6 rear wheels    7 front wheel   8 steering mechanism   9  hydraulic control    10 Brakes   11 power takeoff units   12 tractor pulley  13 contol panel " 
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }
        if len(user_given_spare_parts)==1:
            dep_filter=p_da[p_da.spare_parts==user_given_spare_parts[0]]
            supplier=dep_filter["supplier_name"]

            return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            'List of suppliers for'+' '+user_given_spare_parts[0]+' is '+str(supplier.to_list()[:100])
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }
        if len(user_given_spare_parts)==2:
            dep_filter_1=set(p_da[p_da.spare_parts==user_given_spare_parts[0]]['supplier_name'].to_list())
            dep_filter_2=p_da[p_da.spare_parts==user_given_spare_parts[1]]['supplier_name'].to_list()
            common_supplier=list(dep_filter_1.intersection(dep_filter_2))
            #comm_tab=pd.DataFrame(common_supplier)
            #supplier=dep_filter["supplier_name"]
            return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "List of suppliers who supply both"+' '+user_given_spare_parts[0]+" and "+user_given_spare_parts[1]+' are '+str(common_supplier[:100])
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }

    if intent == 'supplier_option - Total_revenue - in given year':
        user_replace=query_text.replace('  ',' ')
        user_split=user_replace.split(' ')
        high_key=['higher','highest','high']
        total=['total','sum']
        h=[]
        t=[]
        for dd in range(0,len(user_split)):
            if user_split[dd] in high_key:
                h.append(1)
            if user_split[dd] in total:
                t.append(1)
        year=[]
        for ss in user_split:
            if ss.isnumeric() and int(ss)>1970 and int(ss)<2021:
                 year.append(ss)
        if len(year)==1 and len(h)==1 and len(t)==0:
            return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "To get the higest revenue please try again by mentioning start year and end year"
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }
        if len(year)==1 and len(h)==0 and len(t)==0:
            rev=p_da[p_da.year==int(year[0])]["revenue"].sum()
            return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "Total revenue for "+year[0]+" is "+str(rev)
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }

        if len(year)==1 and len(h)==0 and len(t)==1:
            rev=p_da[p_da.year==int(year[0])]["revenue"].sum()
            return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "Total revenue for "+year[0]+" is "+str(rev)
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }

        if len(year)==2 and len(h)==1 and len(t)==0:
            
            hig_rev=p_da.loc[(p_da['year']>=int(year[0])) & (p_da['year']< int(year[1]))]["revenue"].max()
            return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "Highest revenue obtained between"+' '+year[0]+' to '+ year[1]+" is "+str(hig_rev)
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }
        
        if len(year)==2 and len(h)==0 and len(t)==1:
            
            tot_rev=p_da.loc[(p_da['year']>=int(year[0])) & (p_da['year']< int(year[1]))]["revenue"].sum()
            return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "Total revenue obtained between"+' '+year[0]+' to '+ year[1]+" is "+str(tot_rev)
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }

        if len(year)==2 and len(h)==0 and len(t)==0:
            
            tot_rev=p_da.loc[(p_da['year']>=int(year[0])) & (p_da['year']< int(year[1]))]["revenue"].sum()
            return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "Total revenue obtained between"+' '+year[0]+' to '+ year[1]+" is "+str(tot_rev)
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }


    if intent=='sales trend - parts - custom':
        user_replace=query_text.replace('  ',' ')
        user_split=user_replace.split(' ')
        top_count=[]
        year=[]
        for ss in user_split:
            if ss.isnumeric() and int(ss)<=100:
                top_count.append(ss)
            if ss.isnumeric() and int(ss)>1970 and int(ss)<2021:
                 year.append(ss)
        spare_parts=['engine','clutch','Brakes','hydraulic']
        two_string_spare_parts=['transmission','differential',
                   'final','rear','front','steering',
                   'tractor','control']
        three_string_spare_parts=['power']
        user_given_spare_parts=[]
        for dd in range(0,len(user_split)):
            if user_split[dd] in spare_parts:
                user_given_spare_parts.append(user_split[dd])
            if user_split[dd] in two_string_spare_parts:
                user_given_spare_parts.append(user_split[dd]+' '+user_split[dd+1])
            if user_split[dd] in three_string_spare_parts:
                user_given_spare_parts.append(user_split[dd]+' '+user_split[dd+1]+' '+user_split[dd+2])
        h=[ss for ss in user_split if ss=='high']
        l=[ss for ss in user_split if ss=='low']
        
        if len(year)!=2 and len(year)!=0:
                return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "Please try again by giving proper duration both start year and end year need, If looking for year were sale is high or low dont mention year"
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }


        if len(user_given_spare_parts)==0 and len(year)==2 and len(h)==1 or len(l)==1:
          if len(year)==2:
            if h and len(l)==0:
                y_filter=p_da.loc[(p_da['year']>=int(year[0])) & (p_da['year']<=int(year[1]))]
                sum_data=y_filter.groupby(["spare_parts"], as_index=False)["spend"].agg('sum')
                hig_tr=sum_data.sort_values('spend',ascending=False)
                return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "The spare part which have "+str(hig_tr['spend'].iloc[0])+' as highest spend is '+str(hig_tr['spare_parts'].iloc[0])
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }
            if l and len(h)==0:
                y_filter=p_da.loc[(p_da['year']>=int(year[0])) & (p_da['year']<=int(year[1]))]
                sum_data=y_filter.groupby(["spare_parts"], as_index=False)["spend"].agg('sum')
                low_tr=sum_data.sort_values('spend',ascending=True)
                return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "The spare part which have "+str(low_tr['spend'].iloc[0])+' as least spend is '+str(low_tr['spare_parts'].iloc[0])
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }

        if len(user_given_spare_parts)==1 and len(year)==0 and len(h)==1 or len(l)==1:  
            if h and len(l)==0:     
                part_filter=p_da[p_da.spare_parts==user_given_spare_parts[0]]
                y_sum=part_filter.groupby(["spare_parts","year"], as_index=False)["spend"].agg('sum')
                hig_y_res=y_sum.sort_values('spend',ascending=False)
                return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "In "+ str(hig_y_res['year'].iloc[0])+' for '+ user_given_spare_parts[0]+ ' high spend have been made'
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }

            if l and len(h)==0:     
                part_filter=p_da[p_da.spare_parts==user_given_spare_parts[0]]
                y_sum=part_filter.groupby(["spare_parts","year"], as_index=False)["spend"].agg('sum')
                low_y_res=y_sum.sort_values('spend',ascending=True)
                return {

                    "fulfillmentMessages": [
                     {
                    "text": {
                        "text": [
                            "In "+ str(low_y_res['year'].iloc[0])+' for '+ user_given_spare_parts[0]+ ' low spend have been made'
                        ]

                    }
                   },
                    {
                    "text": {
                        "text": [
                            "* To go back to [information about supplier menu] enter => INFO \n *To go back to [insight about sales trend menu] enter => TREND \n *To exit enter => Exit"
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                      }
                    }
                   ]
                   }


@app.route('/')
def indexs():
    client=MongoClient('mongodb+srv://sarath:ronaldo@cluster0.bylev.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db=client.get_database('enbot')
    records=db.supplier
    cursor = records.find()
    da=list(cursor)
    return json.loads(json_util.dumps(str(da[:])))



'''
@app.route('/flasktest',methods=['POST'])
def index():
    if request.method == "POST":
        d = request.get_json()
    return jsonify({'data':d['hi']})
'''
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=True)