#Data Extraction

import streamlit as st
import pandas as pd
import numpy as np
import os
import pandas as pd
import plotly.express as px
import json
import plotly.graph_objects as go
import requests


#Agg_transaction
path=r"D:\python workings\New folder\pulse\data\aggregated\transaction\country\india\state"
Agg_state_list=os.listdir(path)

col = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [], 'Transaction_amount': []}

for state in Agg_state_list:
    state_path = os.path.join(path, state)
    years_list = os.listdir(state_path)

    for year in years_list:
        year_path = os.path.join(state_path, year)
        quarters_list = os.listdir(year_path)

        for quarter in quarters_list:
            quarter_path = os.path.join(year_path, quarter)
            with open(quarter_path, 'r') as data_file:
                dt = json.load(data_file)

            for i in dt['data']['transactionData']:
                name = i['name']
                count = i['paymentInstruments'][0]['count']
                amount = i['paymentInstruments'][0]['amount']

                col['Transaction_type'].append(name)
                col['Transaction_count'].append(count)
                col['Transaction_amount'].append(amount)
                col['State'].append(state)
                col['Year'].append(year)
                col['Quarter'].append(int(quarter.strip('.json')))


Agg_Trans = pd.DataFrame(col)

Agg_Trans["State"] = Agg_Trans["State"].str.title()
Agg_Trans["State"] = Agg_Trans["State"].str.replace("-"," ")
Agg_Trans["State"] = Agg_Trans["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
Agg_Trans['State'] = Agg_Trans['State'].str.replace("dadra-&-nagar-haveli-&-daman-&-diu","Dadra and Nagar Haveli and Daman and Diu")

#agg_users
path2=r"D:\python workings\New folder\pulse\data\aggregated\user\country\india\state"
Agg_state_listuser=os.listdir(path2)


col2 = {'State': [], 'Year': [], 'Quarter': [],'Mobile_brand':[],'percentage': [], 'Transaction_count': []}


for state in Agg_state_listuser:
    state_path2 = os.path.join(path2, state)
    years_list2 = os.listdir(state_path2)

    for year in years_list2:
        year_path2 = os.path.join(state_path2, year)
        quarters_list2 = os.listdir(year_path2)

        for quarter in quarters_list2:
            quarter_path2 = os.path.join(year_path2, quarter)
            with open(quarter_path2, 'r') as data_file:
                dt2 = json.load(data_file)

                if dt2['data']['usersByDevice']!=None:
                    
                    for i in dt2['data']['usersByDevice']:
                        
                        brand = i['brand']
                        count = i['count']
                        percentage = i['percentage']
                        col2['Mobile_brand'].append(brand)
                        col2['Transaction_count'].append(count)
                        col2['percentage'].append(percentage)
                        col2['State'].append(state)
                        col2['Year'].append(year)
                        col2['Quarter'].append(int(quarter.strip('.json')))
                
          
Agg_user = pd.DataFrame(col2)

Agg_user["State"] = Agg_user["State"].str.title()
Agg_user["State"] = Agg_user["State"].str.replace("-"," ")
Agg_user["State"] = Agg_user["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
Agg_user['State'] = Agg_user['State'].str.replace("dadra-&-nagar-haveli-&-daman-&-diu","Dadra and Nagar Haveli and Daman and Diu")

          
#map_trasactions
path1=r"D:\python workings\New folder\pulse\data\map\transaction\hover\country\india\state"
Agg_state_listu=os.listdir(path1)


col1= {'State': [],'District':[],'Year': [], 'Quarter': [], 'Transaction_count': [], 'Transaction_amount': []}

for state in Agg_state_listu:
    state_path1 = os.path.join(path1, state)
    years_list1 = os.listdir(state_path1)

    for year in years_list1:
        year_path1 = os.path.join(state_path1, year)
        quarters_list1 = os.listdir(year_path1)

        for quarter in quarters_list1:
            quarter_path1 = os.path.join(year_path1, quarter)
            with open(quarter_path1, 'r') as data_file:
                dt1 = json.load(data_file)
                for i in dt1['data']['hoverDataList']:
                    name = i['name']
                    count = i['metric'][0]['count']
                    amount = i['metric'][0]['amount']

                    
                    col1['Transaction_count'].append(count)
                    col1['Transaction_amount'].append(amount)
                    col1['State'].append(state)
                    col1['District'].append(name)
                    col1['Year'].append(year)
                    col1['Quarter'].append(int(quarter.strip('.json')))

            
map_Trans = pd.DataFrame(col1)

map_Trans["State"] = map_Trans["State"].str.title()
map_Trans["State"] = map_Trans["State"].str.replace("-"," ")
map_Trans["State"] = map_Trans["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
map_Trans['State'] = map_Trans['State'].str.replace("dadra-&-nagar-haveli-&-daman-&-diu","Dadra and Nagar Haveli and Daman and Diu")


#map_users

path3=r"D:\python workings\New folder\pulse\data\map\user\hover\country\india\state"
Agg_state_listmapu=os.listdir(path3)

col3= {'State': [],'District':[],'Year': [], 'Quarter': [], 'registeredUsers': []}

for state in Agg_state_listmapu:
    state_path3 = os.path.join(path3, state)
    years_list3 = os.listdir(state_path3)

    for year in years_list3:
        year_path3 = os.path.join(state_path3, year)
        quarters_list3 = os.listdir(year_path3)

        for quarter in quarters_list3:
            quarter_path3 = os.path.join(year_path3, quarter)
            with open(quarter_path3, 'r') as data_file:
                dt3 = json.load(data_file)

                for i in dt3['data']['hoverData'].items():
                    District= i[0]
                    registeredUsers = i[1]['registeredUsers']
                    
                    col3['registeredUsers'].append(registeredUsers)
                    col3['State'].append(state)
                    col3['District'].append(District)
                    col3['Year'].append(year)
                    col3['Quarter'].append(int(quarter.strip('.json')))
                

map_users = pd.DataFrame(col3)

map_users["State"] = map_users["State"].str.title()
map_users["State"] = map_users["State"].str.replace("-"," ")
map_users["State"] = map_users["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
map_users['State'] = map_users['State'].str.replace("dadra-&-nagar-haveli-&-daman-&-diu","Dadra and Nagar Haveli and Daman and Diu")

#Top_transactions
path4=r"D:\python workings\New folder\pulse\data\top\transaction\country\india\state"
Top_trans_list=os.listdir(path4)

col4= {'State': [],'District':[],'Year': [], 'Quarter': [],'Transaction_count': [], 'Transaction_amount': []}

for state in Top_trans_list:
    state_path4 = os.path.join(path4, state)
    years_list4 = os.listdir(state_path4)

    for year in years_list4:
        year_path4 = os.path.join(state_path4, year)
        quarters_list4 = os.listdir(year_path4)

        for quarter in quarters_list4:
            quarter_path4 = os.path.join(year_path4, quarter)
            with open(quarter_path4, 'r') as data_file:
                dt4 = json.load(data_file)

                for i in dt4['data']['districts']:
                    for i in dt4['data']['districts']:
                        District=i['entityName']
                        count=i['metric']['count']
                        amount=i['metric']['amount']

                        col4['Transaction_count'].append(count)
                        col4['Transaction_amount'].append(amount)
                        col4['State'].append(state)
                        col4['District'].append(District)
                        col4['Year'].append(year)
                        col4['Quarter'].append(int(quarter.strip('.json')))

                
top_trans= pd.DataFrame(col4)

top_trans["State"] = top_trans["State"].str.title()
top_trans["State"] = top_trans["State"].str.replace("-"," ")
top_trans["State"] = top_trans["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
top_trans['State'] = top_trans['State'].str.replace("dadra-&-nagar-haveli-&-daman-&-diu","Dadra and Nagar Haveli and Daman and Diu")

#Top_users
path5=r"D:\python workings\New folder\pulse\data\top\user\country\india\state"
Top_users_list=os.listdir(path5)

col5= {'State': [],'District':[],'Year': [], 'Quarter': [],'registeredUsers': [],}

for state in Top_users_list:
    state_path5 = os.path.join(path5, state)
    years_list5 = os.listdir(state_path5)

    for year in years_list5:
        year_path5 = os.path.join(state_path5, year)
        quarters_list5= os.listdir(year_path5)

        for quarter in quarters_list5:
            quarter_path5 = os.path.join(year_path5, quarter)
            with open(quarter_path5, 'r') as data_file:
                dt5 = json.load(data_file)

                
                for i in dt5['data']['districts']:
                    District=i['name']
                    users=i['registeredUsers']

                    col5['registeredUsers'].append(users)
                    col5['State'].append(state)
                    col5['District'].append(District)
                    col5['Year'].append(year)
                    col5['Quarter'].append(int(quarter.strip('.json')))

                
top_user = pd.DataFrame(col5)

top_user["State"] = top_user["State"].str.title()
top_user["State"] = top_user["State"].str.replace("-"," ")
top_user["State"] = top_user["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
top_user['State'] = top_user['State'].str.replace("dadra-&-nagar-haveli-&-daman-&-diu","Dadra and Nagar Haveli and Daman and Diu")


#inserting to sql

#create aggregate_transactions1 table

import mysql.connector     #mydb-->connecting 
mydb=mysql.connector.connect(host='localhost',
                              user='root',
                              password='12345',
                              database='phonepe')#connector
mycursor=mydb.cursor()

drop_query='''drop table if exists aggregate_transactions1'''
mycursor.execute(drop_query)
mydb.commit()

sql='''create table if not exists aggregate_transactions1(State varchar(100),
                                                         Year int,
                                                         Quarter int,
                                                         Transaction_type text,
                                                         Transaction_count bigint,
                                                         Transaction_amount bigint)'''

mycursor.execute(sql)
mydb.commit()

for index,row in Agg_Trans.iterrows():
    sql= '''insert into aggregate_transactions1(State,
                                        Year,
                                        Quarter,
                                        Transaction_type,
                                        Transaction_count,
                                        Transaction_amount)
                                        values(%s,%s,%s,%s,%s,%s)'''
    values=(row['State'],
            row['Year'],
            row['Quarter'],
            row['Transaction_type'],
            row['Transaction_count'],
            row['Transaction_amount'])
    
    mycursor.execute(sql,values)
    mydb.commit()
    
#create aggregate_users table

sql='''create table if not exists aggregate_users(State varchar(100),
                                                 Year int,
                                                 Quarter int,
                                                 Mobile_brand varchar(100),
                                                 percentage float,
                                                 Transaction_count bigint)'''

mycursor.execute(sql)
mydb.commit()

for index,row in Agg_user.iterrows():
    sql= '''insert into aggregate_users(State,
                                        Year,
                                        Quarter,
                                        Mobile_brand,
                                        percentage,
                                        Transaction_count)
                                        values(%s,%s,%s,%s,%s,%s)'''
    values=(row['State'],
            row['Year'],
            row['Quarter'],
            row['Mobile_brand'],
            row['percentage'],
            row['Transaction_count'])
    
    mycursor.execute(sql,values)
    mydb.commit()
            

#create map_transaction table

sql='''create table if not exists map_tranactions(State varchar(100),
                                                    District varchar(100),
                                                    Year int,
                                                    Quarter int,
                                                    Transaction_count bigint,
                                                    Transaction_amount bigint)'''

mycursor.execute(sql)
mydb.commit()

for index,row in map_Trans.iterrows():
    sql= '''insert into map_tranactions(State,
                                        District,
                                        Year,
                                        Quarter,
                                        Transaction_count,
                                        Transaction_amount)
                                        values(%s,%s,%s,%s,%s,%s)'''
    values=(row['State'],
            row['District'],
            row['Year'],
            row['Quarter'],
            row['Transaction_count'],
            row['Transaction_amount'])
    
    mycursor.execute(sql,values)
    mydb.commit()

#create map_user table

sql='''create table if not exists map_users(State varchar(100),
                                            District varchar(100),
                                            Year int,
                                            Quarter int,
                                            registeredUsers bigint )'''

mycursor.execute(sql)
mydb.commit()

for index,row in map_users.iterrows():
    sql= '''insert into map_users(State,
                                District,
                                Year,
                                Quarter,
                                registeredUsers)
                                values(%s,%s,%s,%s,%s)'''
    values=(row['State'],
            row['District'],
            row['Year'],
            row['Quarter'],
            row['registeredUsers'])
    
    mycursor.execute(sql,values)
    mydb.commit()

#create top_transaction table

sql='''create table if not exists top_tranactions(State varchar(100),
                                                    District varchar(100),
                                                    Year int,
                                                    Quarter int,
                                                    Transaction_count bigint,
                                                    Transaction_amount bigint)'''

mycursor.execute(sql)
mydb.commit()

for index,row in top_trans.iterrows():
    sql= '''insert into top_tranactions(State,
                                        District,
                                        Year,
                                        Quarter,
                                        Transaction_count,
                                        Transaction_amount)
                                        values(%s,%s,%s,%s,%s,%s)'''
    values=(row['State'],
            row['District'],
            row['Year'],
            row['Quarter'],
            row['Transaction_count'],
            row['Transaction_amount'])
    
    mycursor.execute(sql,values)
    mydb.commit()


#create top_user table

sql='''create table if not exists top_users(State varchar(100),
                                            District varchar(100),
                                            Year int,
                                            Quarter int,
                                            registeredUsers bigint )'''

mycursor.execute(sql)
mydb.commit()

for index,row in top_user.iterrows():
    sql= '''insert into top_users(State,
                                District,
                                Year,
                                Quarter,
                                registeredUsers)
                                values(%s,%s,%s,%s,%s)'''
    values=(row['State'],
            row['District'],
            row['Year'],
            row['Quarter'],
            row['registeredUsers'])
    
    mycursor.execute(sql,values)
    mydb.commit()

