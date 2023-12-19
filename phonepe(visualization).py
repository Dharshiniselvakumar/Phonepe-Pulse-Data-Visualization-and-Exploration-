#Data Visualization

import streamlit as st
import pandas as pd
import os
import json
import plotly.express as px
import plotly.graph_objects as go
import requests


#converting dataframe from sql

import mysql.connector     #mydb-->connecting 
mydb=mysql.connector.connect(host='localhost',
                              user='root',
                              password='12345',
                              database='phonepe')#connector
mycursor=mydb.cursor()

mycursor.execute('select * from aggregate_transactions1')
t1=mycursor.fetchall()
Agg_tran = pd.DataFrame(t1,columns = ("State", "Year", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

mycursor.execute('select * from aggregate_users')
t2=mycursor.fetchall()
Agg_us = pd.DataFrame(t2,columns = ("State", "Year", "Quarter", "Mobile_brand", "percentage", "Transaction_count"))

mycursor.execute('select * from map_tranactions')
t3=mycursor.fetchall()
map_tran = pd.DataFrame(t3,columns = ("State", "District", "Year", "Quarter", "Transaction_count", "Transaction_amount"))

mycursor.execute('select * from map_users')
t4=mycursor.fetchall()
map_us = pd.DataFrame(t4,columns = ("State", "District", "Year", "Quarter", "registeredUsers"))

mycursor.execute('select * from top_tranactions')
t5=mycursor.fetchall()
top_tran = pd.DataFrame(t5,columns = ("State", "District", "Year", "Quarter", "Transaction_count", "Transaction_amount"))

mycursor.execute('select * from top_users')
t6=mycursor.fetchall()
top_us = pd.DataFrame(t6,columns = ("State", "District", "Year", "Quarter", "registeredUsers"))

#creating maps and charts

def all_amount():
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response =requests.get(url)
    data1 = json.loads(response.content)
    state_names_tran = [feature["properties"]["ST_NM"] for feature in data1["features"]]
    state_names_tran.sort()

    df_state_names_tran = pd.DataFrame({"States":state_names_tran})

    data = []

    for year in map_us["Year"].unique():
        for quarter in Agg_tran["Quarter"].unique():

            at1= Agg_tran[(Agg_tran["Year"]==year)&(Agg_tran["Quarter"]==quarter)]
            at2 = at1[["State","Transaction_amount"]]
            at2 = at2.sort_values(by="State")
            at2["Year"]=year
            at2["Quarter"]=quarter
            data.append(at2)

    merged_df = pd.concat(data)

    fig_all_amount = px.choropleth(merged_df, 
                            geojson= data1, 
                            locations= "State", 
                            featureidkey= "properties.ST_NM", 
                            color= "Transaction_amount",
                            color_continuous_scale= "tropic", 
                            range_color= (0,4000000000), 
                            hover_name= "State", 
                            title = "TRANSACTION AMOUNT",
                            animation_frame="Year", 
                            animation_group="Quarter")

    fig_all_amount.update_geos(fitbounds= "locations", visible =False)
    fig_all_amount.update_layout(width =600, height= 700,title_font= {"size":30})
    return st.plotly_chart(fig_all_amount)


def all_count():
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    state_names_tran= [feature["properties"]["ST_NM"]for feature in data1["features"]]
    state_names_tran.sort()

    df_state_names_tran= pd.DataFrame({"States":state_names_tran})


    data= []

    for year in Agg_tran["Year"].unique():
        for quarter in Agg_tran["Quarter"].unique():

            at1= Agg_tran[(Agg_tran["Year"]==year)&(Agg_tran["Quarter"]==quarter)]
            at2= at1[["State", "Transaction_count"]]
            at2=at2.sort_values(by="State")
            at2["Year"]=year
            at2["Quarter"]=quarter
            data.append(at2)

    merged_df = pd.concat(data)

    fig_all_count= px.choropleth(merged_df, 
                            geojson= data1, 
                            locations= "State",
                            featureidkey= "properties.ST_NM",
                            color= "Transaction_count", 
                            color_continuous_scale="tropic", 
                            range_color= (0,4000000),
                            title="TRANSACTION COUNT", 
                            hover_name= "State", 
                            animation_frame= "Year", 
                            animation_group= "Quarter")

    fig_all_count.update_geos(fitbounds= "locations", visible= False)
    fig_all_count.update_layout(width= 600, height= 700,title_font={"size":30})
    return st.plotly_chart(fig_all_count)

def payment_count():
    at= Agg_tran[["Transaction_type", "Transaction_count"]]
    at1= at.groupby("Transaction_type")["Transaction_count"].sum()


    df_at1= pd.DataFrame(at1).reset_index()
    fig_payment_count= px.bar(df_at1,
                   x= "Transaction_type",
                   y= "Transaction_count",
                   title= "TRANSACTION TYPE and TRANSACTION COUNT",
                   color_discrete_sequence=px.colors.sequential.Redor)
    fig_payment_count.update_layout(width=600, height= 500)
    return st.plotly_chart(fig_payment_count)

def payment_amount():
    atype= Agg_tran[["Transaction_type","Transaction_amount"]]
    atype1= atype.groupby("Transaction_type")["Transaction_amount"].sum()
    df_atype= pd.DataFrame(atype1).reset_index()
    fig_tran_type= px.bar(df_atype, 
                    x= "Transaction_type", 
                    y= "Transaction_amount", 
                    title= "TRANSACTION TYPE and TRANSACTION AMOUNT",
                    color_discrete_sequence= px.colors.sequential.Redor)
    fig_tran_type.update_layout(width= 600, height= 500)
    return st.plotly_chart(fig_tran_type)

def transaction_amount_year(select_yr):
    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    state_names_tran= [feature["properties"]['ST_NM']for feature in data1["features"]]
    state_names_tran.sort()

    year= int(select_yr)
    tamount= Agg_tran[["State","Year","Transaction_amount"]]
    tamount1= tamount.loc[(Agg_tran["Year"]==year)]
    tamount2= tamount1.groupby("State")["Transaction_amount"].sum()
    tamount3= pd.DataFrame(tamount2).reset_index()

    fig_t_amount= px.choropleth(tamount3, 
                            geojson= data1, 
                            locations= "State", 
                            featureidkey= "properties.ST_NM",
                            color= "Transaction_amount", 
                            color_continuous_scale="tropic", 
                            range_color=(0,400000000000),
                            title="TRANSACTION AMOUNT and STATE", 
                            hover_name= "State")

    fig_t_amount.update_geos(fitbounds= "locations", visible= False)
    fig_t_amount.update_layout(width=600,height=700,title_font= {"size":25})
    return st.plotly_chart(fig_t_amount)


def payment_count_year(select_yr):
    year= int(select_yr)
    ptype= Agg_tran[["Transaction_type", "Year", "Transaction_count"]]
    ptype1= ptype.loc[(Agg_tran["Year"]==year)]
    ptype2= ptype1.groupby("Transaction_type")["Transaction_count"].sum()
    ptype3= pd.DataFrame(ptype2).reset_index()

    fig_ptype= px.bar(ptype3,
                    x= "Transaction_type", 
                    y= "Transaction_count", 
                    title= "PAYMENT COUNT and PAYMENT TYPE",
                    color_discrete_sequence=px.colors.sequential.Redor)
    fig_ptype.update_layout(width=600, height=500)
    return st.plotly_chart(fig_ptype)

def transaction_count_year(select_yr):
    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1=json.loads(response.content)
    state_names_tran= [feature["properties"]["ST_NM"]for feature in data1["features"]]
    state_names_tran.sort()

    year= int(select_yr)
    tcs= Agg_tran[["State", "Year", "Transaction_count"]]
    tcs1= tcs.loc[(Agg_tran["Year"]==year)]
    tcs2= tcs1.groupby("State")["Transaction_count"].sum()
    tcs3= pd.DataFrame(tcs2).reset_index()

    fig_tcount= px.choropleth(tcs3, 
                            geojson=data1, 
                            locations= "State", 
                            featureidkey= "properties.ST_NM",
                            color= "Transaction_count", 
                            color_continuous_scale= "tropic",
                            range_color=(0,4000000000),
                            title= "TRANSACTION COUNT and STATE",
                            hover_name= "State")
    fig_tcount.update_geos(fitbounds= "locations", visible= False)
    fig_tcount.update_layout(width=600, height= 700,title_font={"size":25})
    return st.plotly_chart(fig_tcount)

def payment_amount_year(select_yr):
    year= int(select_yr)
    ptpa = Agg_tran[["Year", "Transaction_type", "Transaction_amount"]]
    ptpa1= ptpa.loc[(Agg_tran["Year"]==year)]
    ptpa2= ptpa1.groupby("Transaction_type")["Transaction_amount"].sum()
    ptpa3= pd.DataFrame(ptpa2).reset_index()

    fig_type_amount= px.bar(ptpa3, 
                    x="Transaction_type", 
                    y= "Transaction_amount", 
                    title= "PAYMENT TYPE and PAYMENT AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Redor)
    fig_type_amount.update_layout(width=600, height=500)
    return st.plotly_chart(fig_type_amount)



def state_all_trans_amount(select_yr,state):
    year= int(select_yr)
    mts= map_tran[["State", "Year","District", "Transaction_amount"]]
    mts1= mts.loc[(map_tran["State"]==state)&(map_tran["Year"]==year)]
    mts2= mts1.groupby("District")["Transaction_amount"].sum()
    mts3= pd.DataFrame(mts2).reset_index()

    fig_district_amount= px.bar(mts3, 
                                x= "District", 
                                y= "Transaction_amount", 
                                title= "DISTRICT and TRANSACTION AMOUNT",
                                color_discrete_sequence= px.colors.sequential.Redor)
    fig_district_amount.update_layout(width= 600, height= 500)
    return st.plotly_chart(fig_district_amount)

def state_all_users(select_yr,state):
    year= int(select_yr)
    mus= map_us[["State", "Year", "District", "registeredUsers"]]
    mus1= mus.loc[(map_us["State"]==state)&(map_us["Year"]==year)]
    mus2= mus1.groupby("District")["registeredUsers"].sum()
    mus3= pd.DataFrame(mus2).reset_index()

    fig_dusers= px.bar(mus3, 
                    x= "District", 
                    y="registeredUsers", 
                    title="DISTRICT and REGISTERED USER",
                    color_discrete_sequence=px.colors.sequential.Redor)
    fig_dusers.update_layout(width= 600, height= 500)
    return st.plotly_chart(fig_dusers)

def all_states(state):
    m= map_us[["State","District","registeredUsers"]]
    m1= m.loc[(m["State"]==state)]
    m2= m1[["District", "registeredUsers"]]
    m3= m2.groupby("District")["registeredUsers"].sum()
    m4= pd.DataFrame(m3).reset_index()
    fig_d_rusers= px.bar(m4, 
                x= "District", 
                y= "registeredUsers", 
                title= "DISTRICT AND REGISTERED USER",
                color_discrete_sequence=px.colors.sequential.Redor)
    fig_d_rusers.update_layout(width= 600, height= 500)
    return st.plotly_chart(fig_d_rusers)




def ques1():
    ht= Agg_tran[["State", "Transaction_amount"]]
    ht1= ht.groupby("State")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_1= px.bar(ht2, 
                    x= "State", 
                    y= "Transaction_amount",
                    title= "HIGHEST TRANSACTION AMOUNT AND STATES",
                    color_discrete_sequence= px.colors.sequential.Redor)
    return st.plotly_chart(fig_1)

def ques2():
    lt= Agg_tran[["State", "Transaction_amount"]]
    lt1= lt.groupby("State")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_2= px.bar(lt2, x= "State",
                     y= "Transaction_amount",
                     title= "LOWEST TRANSACTION AMOUNT AND STATES",
                    color_discrete_sequence= px.colors.sequential.Redor)
    return st.plotly_chart(fig_2)


def ques3():
    hc= Agg_tran[["State", "Transaction_count"]]
    hc1= hc.groupby("State")["Transaction_count"].sum().sort_values(ascending=False)
    hc2= pd.DataFrame(hc1).reset_index()

    fig_3= px.bar(hc2, 
                    x= "State", 
                    y= "Transaction_count", 
                    title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Redor)
    return st.plotly_chart(fig_3)

def ques4():
    lc= Agg_tran[["State", "Transaction_count"]]
    lc1= lc.groupby("State")["Transaction_count"].sum().sort_values(ascending=True)
    lc2= pd.DataFrame(lc1).reset_index()

    fig_4= px.bar(lc2, 
                    x= "State", 
                    y= "Transaction_count", 
                    title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Redor)
    return st.plotly_chart(fig_4)

def ques5():
    dha= map_tran[["District", "Transaction_amount"]]
    dha1= dha.groupby("District")["Transaction_amount"].sum().sort_values(ascending=False)
    dha2= pd.DataFrame(dha1).head(10).reset_index()

    fig_5= px.pie(dha2, 
                    values= "Transaction_amount", 
                    names= "District", 
                    title="TOP 10 DISTRICTS WITH HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_5)

def ques6():
    dla= map_tran[["District", "Transaction_amount"]]
    dla1= dla.groupby("District")["Transaction_amount"].sum().sort_values(ascending=True)
    dla2= pd.DataFrame(dla1).head(10).reset_index()

    fig_6= px.pie(dla2, 
                    values= "Transaction_amount", 
                    names= "District", 
                    title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_6)


def ques7():
    brand= Agg_us[["Mobile_brand","Transaction_count"]]
    brand1= brand.groupby("Mobile_brand")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, 
                    values= "Transaction_count", 
                    names= "Mobile_brand", 
                    color_discrete_sequence=px.colors.sequential.Emrld_r,
                        title= "TOP MOBILE BRANDS USED")
    return st.plotly_chart(fig_brands)



def ques8():
    dlc= map_tran[["District", "Transaction_count"]]
    dlc1= dlc.groupby("District")["Transaction_count"].sum().sort_values(ascending=True)
    dlc2= pd.DataFrame(dlc1).reset_index().head(10)

    fig_8= px.bar(dlc2, 
                x= "District", 
                y= "Transaction_count", 
                title= "DISTRICTS WITH LOWEST TRANSACTION COUNT",
                color_discrete_sequence= px.colors.sequential.Redor)
    return st.plotly_chart(fig_8)

def ques9():
    dhc= map_tran[["District", "Transaction_count"]]
    dhc1= dhc.groupby("District")["Transaction_count"].sum().sort_values(ascending=False)
    dhc2= pd.DataFrame(dhc1).reset_index().head(10)

    fig_9= px.bar(dhc2, 
                x= "District", 
                y= "Transaction_count", 
                title= "DISTRICTS WITH HIGHEST TRANSACTION COUNT",
                color_discrete_sequence= px.colors.sequential.Redor)
    return st.plotly_chart(fig_9)
   

def ques10():
    type= Agg_tran[["Transaction_type","Transaction_count"]]
    type1= type.groupby("Transaction_type")["Transaction_count"].sum().sort_values(ascending=False)
    type2= pd.DataFrame(type1).reset_index()

    fig_10= px.pie(type2, 
                    values= "Transaction_count", 
                    names= "Transaction_type", 
                    color_discrete_sequence=px.colors.sequential.Emrld_r,
                        title= "HIGHLY USED TRANSACTION TYPES")
    return st.plotly_chart(fig_10)
    


st.set_page_config(
    page_title="PHONEPE PLUSE",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded")
    



st.title("PHONEPE PLUSE | The beat of progress")



with st.sidebar:
            st.header('HOME')
            if st.button('learnings'):
                st.caption('Data extraction')
                st.caption('Data processing')
                st.caption('Database management')
                st.caption('Visualization & dashboard creation')





tab1, tab2= st.tabs(["***CHARTS***","***INSIGHTS***"])


with tab1:
    select_yr = st.selectbox("select Year",("All", "2018", "2019", "2020", "2021", "2022", "2023"))
    if select_yr == "All" :
        col1, col2 = st.columns(2)
        with col1:
            all_amount()
            payment_amount()
            
            
        with col2:
            all_count()
            payment_count()
            

        state=st.selectbox("select State",('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                'Uttarakhand', 'West Bengal'))
        all_states(state)

    else:
        col1,col2= st.columns(2)

        with col1:
            transaction_amount_year(select_yr)
            payment_amount_year(select_yr)
            

            state= st.selectbox("select state",('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                'Uttarakhand', 'West Bengal'))
        
            state_all_users(select_yr,state)
        with col2:
            transaction_count_year(select_yr)
            payment_count_year(select_yr)
            st.divider()
            state_all_trans_amount(select_yr,state)
with tab2:
    ques= st.selectbox("select  question",('States With Highest Trasaction Amount',
                                              'States With Lowest Trasaction Amount',
                                              'States With Highest Trasaction Count',
                                              'States With Lowest Trasaction Count',
                                              'Districts With Highest Transaction Amount',
                                              '10 Districts With Lowest Transaction Amount',
                                              'Top Brands Of Mobiles Used',
                                              '10 Districts With Lowest Transaction Count',
                                              'Districts With Highest Transaction Count',
                                              'Highest useage of Transaction Type'
                                              ))                      
                                                
                                                
                    
    if ques=="States With Highest Trasaction Amount":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="States With Highest Trasaction Count":
        ques3()

    elif ques=="States With Lowest Trasaction Count":
        ques4()

    elif ques=="Districts With Highest Transaction Amount":
        ques5()

    elif ques=="10 Districts With Lowest Transaction Amount":
        ques6()

    elif ques=="Top Brands Of Mobiles Used":
        ques7()

    elif ques=="Districts With Lowest Transaction Count":
        ques8()

    elif ques=="Districts With Highest Transaction Count":
        ques9()

    elif ques=="Highest useage of Transaction Type":
        ques10()
    