
import json
import streamlit as st
import pandas as pd
import requests
import psycopg2
import plotly.express as px
import plotly.graph_objects as go


#CREATE DATAFRAMES FROM SQL
#sql connection

mydb=psycopg2.connect(host ="localhost",
                      user = "postgres",
                      password = "Karthika",
                      database = "phonepe_data",
                      port = "5432"
                     )
cursor =mydb.cursor()
# aggregated_transaction
cursor.execute("select * from aggregated_transaction;")
mydb.commit()
table1=cursor.fetchall()
aggre_trans = pd.DataFrame(table1,columns =("states","years" ,"Quarter" ,"Transaction_type", "Transaction_count","Transaction_amount"))

# aggregated_user
cursor.execute("select * from aggregated_user;")
mydb.commit()
table2=cursor.fetchall()
aggre_user = pd.DataFrame(table2,columns =("states", "years", "Quarter", "Brands", "Transaction_count", "Percentage"))

# map_transaction
cursor.execute("select * from map_transaction;")
mydb.commit()
table3=cursor.fetchall()
map_trans = pd.DataFrame(table3,columns=("states", "years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

#map user
cursor.execute("select * from map_user;")
mydb.commit()
table4=cursor.fetchall()
map_user = pd.DataFrame(table4,columns=("states", "years", "Quarter", "Districts", "RegisteredUsers", "AppOpens"))

#top transaction
cursor.execute("select * from top_transaction;")
mydb.commit()
table5= cursor.fetchall()
top_trans=pd.DataFrame(table5,columns=("states", "years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

# top user
cursor.execute("select * from top_user;")
mydb.commit()
table6= cursor.fetchall()
top_user=pd.DataFrame(table6,columns=("states", "years", "Quarter", "Pincodes", "RegisteredUser"))

def animate_all_amount():
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
  
    response = requests.get(url)
    data1= json.loads(response.content)
    state_names_tra = [feature["properties"]["ST_NM"]for feature in data1["features"]]
    state_names_tra.sort()
    
    df_state_name_tra = pd.DataFrame({"states": state_names_tra})
    
    frames =[]
    for year in map_user["years"].unique():
        for quarter in aggre_trans["Quarter"].unique():
            
            at1 = aggre_trans[(aggre_trans["years"]==year)&(aggre_trans["Quarter"]==quarter)]
            atf1 = at1[["states","Transaction_amount"]]
            atf1 = atf1.sort_values(by="states")
            atf1["years"]=year
            atf1["Quarter"]=quarter
            frames.append(atf1)
            
    merged_df = pd.concat(frames)   
        
    fig_tra = px.choropleth(merged_df , geojson=data1,locations= "states", featureidkey= "propertise.ST_NM", color = "Transaction_amount",
                            color_continuous_scale= "Sunsetdark", range_color=(0,4000000000), hover_name="states", title = "TRANSACTION AMOUNT",
                            animation_frame="years", animation_group="Quarter")
    fig_tra.update_geos(fitbounds="locations" , visible= False)
    fig_tra.update_layout(width = 600, height= 700)
    fig_tra.update_layout(title_font={"size":25})
    return st.plotly_chart(fig_tra)

def payment_count():
    attype=aggre_trans[["Transaction_type","Transaction_count"]]
    att1= attype.groupby("Transaction_type")["Transaction_count"].sum()
    df_att1=pd.DataFrame(att1).reset_index()
    fig_pc=px.bar(df_att1,x ="Transaction_type",y="Transaction_count",title="TRANSACTION TYPE and TRANSACTION COUNT",
                 color_discrete_sequence=px.colors.sequential.Redor_r)
    fig_pc.update_layout(width=600,height= 500)
    return st.plotly_chart(fig_pc)

def animate_all_count():
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

    response= requests.get(url)
    data1= json.loads(response.content)
    state_names_tra=[feature["properties"]["ST_NM"] for feature in data1["features"]]
    state_names_tra.sort()
    
    df_state_names_tra=pd.DataFrame({"states":state_names_tra})
    
    frames=[]
    
    for year in aggre_trans["years"].unique():
        for quarter in aggre_trans["Quarter"].unique():
            
            at1=aggre_trans[(aggre_trans["years"]==year)&(aggre_trans["Quarter"]==quarter)]
            atf1= at1[["states","Transaction_count"]]
            atf1=atf1.sort_values(by="states")
            atf1["years"]=year
            atf1["Quarter"]=quarter
            frames.append(atf1)
    merged_df = pd.concat(frames)    
    
    fig_tra=px.choropleth(merged_df, geojson= data1, locations ="states", featureidkey="properties.ST_NM",
                           color="Transaction_count", color_continuous_scale="Sunsetdark", range_color=(0,3000000),
                           title="TRANSACTION COUNT", hover_name="states", animation_frame="years", animation_group="Quarter")
    fig_tra.update_geos(fitbounds="locations", visible= False)
    fig_tra.update_layout(width=600, height=700)
    fig_tra.update_layout(title_font={"size":25})
    return st.plotly_chart(fig_tra)

def payment_amount():
    attype= aggre_trans[["Transaction_type", "Transaction_amount"]]
    att1= attype.groupby("Transaction_type")["Transaction_amount"].sum()
    df_att1=pd.DataFrame(att1).reset_index()
    fig_tra_pa= px.bar(df_att1, x="Transaction_type", y="Transaction_amount", title="TRANSACTION TYPE and TRANSACTION AMOUNT",
                       color_discrete_sequence= px.colors.sequential.Blues_r)
    fig_tra_pa.update_layout(width=600, height=500)
    return st.plotly_chart(fig_tra_pa)

def reg_all_states(state):
    mu=map_user[["states","Districts","RegisteredUsers"]]
    mu1= mu.loc[(mu["states"]==state)]
    mu2= mu1[["Districts","RegisteredUsers"]]
    mu3 = mu2.groupby("Districts")["RegisteredUsers"].sum()
    mu4 = pd.DataFrame(mu3).reset_index()
    fig_mu=px.bar(mu4, x ="Districts", y="RegisteredUsers", title= "DISTRICTS and REGISTERED USER", 
                   color_discrete_sequence=px.colors.sequential.Bluered_r)
    fig_mu.update_layout(width=1000 , height= 500)
    return st.plotly_chart(fig_mu)
    
def transaction_amount_year(sel_year):
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                
    response= requests.get(url)
    data1= json.loads(response.content)
    state_name_tra = [feature["properties"]["ST_NM"]for feature in data1["features"]]
    state_name_tra.sort()
    
    year= int(sel_year)
    atay= aggre_trans[["states","years","Transaction_amount"]]
    atay1 = atay.loc[(aggre_trans["years"]==year)]
    atay2 = atay1.groupby("states")["Transaction_amount"].sum()
    atay3 = pd.DataFrame(atay2).reset_index()
    
    fig_atay= px.choropleth(atay3, geojson= data1, locations="states", featureidkey="properties.ST_NM",
                             color="Transaction_amount" , color_continuous_scale="rainbow",range_color=(0,800000000000),
                             title= "TRANSACTION AMOUNT and STATES",hover_name="states")
    
    fig_atay.update_geos(fitbounds="locations", visible=False)
    fig_atay.update_layout(width=600, height=700)
    fig_atay.update_layout(title_font={"size":25})
    return st.plotly_chart(fig_atay)
    
 
def payment_count_year(sel_year):
    year= int(sel_year)
    apc= aggre_trans[["Transaction_type", "years", "Transaction_count"]]
    apc1 = apc.loc[(aggre_trans["years"]==year)]
    apc2 = apc1.groupby("Transaction_type")["Transaction_count"].sum()
    apc3= pd.DataFrame(apc2).reset_index()
    
    fig_apc= px.bar(apc3,x="Transaction_type",y ="Transaction_count", title="PAYMENT COUNT and PAYMENT TYPE",
                     color_discrete_sequence=px.colors.sequential.Brwnyl_r)
    fig_apc.update_layout(width=600, height=500)
    return st. plotly_chart(fig_apc)

def transaction_count_year(sel_year):
   
    url ="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1= json.loads(response.content)
    state_names_tra = [feature["properties"]["ST_NM"]for feature in data1["features"]]
    state_names_tra.sort()
    
    year= int(sel_year)
    atcy= aggre_trans[["states","years","Transaction_count"]]
    atcy1= atcy.loc[(aggre_trans["years"]==year)]
    atcy2= atcy.groupby("states")["Transaction_count"].sum()
    atcy3= pd.DataFrame(atcy2).reset_index()
    
    fig_atcy= px.choropleth(atcy3 , geojson= data1, locations="states", featureidkey="properties.ST_NM",
                            color="Transaction_count", color_continuous_scale="rainbow", range_color=(0,3000000000),
                            title="TRANSACTION COUNT and STATES", hover_name="states")
    fig_atcy.update_geos(fitbounds="locations", visible=False)
    fig_atcy.update_layout(width= 600, height=700)
    fig_atcy.update_layout(title_font={"size":25})
    return st.plotly_chart(fig_atcy)

def payment_amount_year(sel_year):
    year= int(sel_year)
    apay=aggre_trans[["years","Transaction_type","Transaction_amount"]]
    apay1=apay.loc[(aggre_trans["years"]==year)]
    apay2=apay1.groupby("Transaction_type")["Transaction_amount"].sum()
    apay3=pd.DataFrame(apay2).reset_index()
    
    fig_apay= px.bar(apay3, x="Transaction_type", y="Transaction_amount", title="PAYMENT TYPE and PAYMENT AMOUNT",
                      color_discrete_sequence=px.colors.sequential.Burg_r)
    fig_apay.update_layout(width=600, height=500)
    return st.plotly_chart(fig_apay)

def reg_state_all_RU(sel_year,state):
    year= int(sel_year)
    mus= map_user[["states","years", "Districts", "RegisteredUsers"]]
    mus1 = mus.loc[(map_user["states"]==state)&(map_user["years"]==year)]
    mus2 = mus1.groupby("Districts")["RegisteredUsers"].sum()
    mus3= pd.DataFrame(mus2).reset_index() 
    
    fig_mus=px.bar(mus3, x="Districts", y="RegisteredUsers", title="DISTRICTS and REGISTERED USER",
                    color_discrete_sequence=px.colors.sequential. Cividis_r)
    fig_mus.update_layout(width= 600,height=500)
    return st.plotly_chart(fig_mus)
                   

def reg_state_all_TA(sel_year,state):
    year= int(sel_year)
    mts = map_trans[["states","years","Districts","Transaction_amount"]]
    mts1 = mts.loc[(map_trans["states"]==state)&(map_trans["years"]==year)]
    mts2 = mts1.groupby("Districts")["Transaction_amount"].sum()
    mts3= pd.DataFrame(mts2).reset_index()
    
    fig_mts= px.bar(mts3, x="Districts",y="Transaction_amount", title="DISTRICTS and TRANSACTION AMOUNT",
                    color_discrete_sequence= px.colors.sequential.Darkmint_r)
    fig_mts.update_layout(width= 600, height=500)
    return st.plotly_chart(fig_mts)

def ques1():
    brand= aggre_user[["Brands", "Transaction_count"]]
    brand1 = brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2 = pd.DataFrame(brand1).reset_index()
    
    fig_brands= px.pie(brand2, values="Transaction_count", names="Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= aggre_trans[["states", "Transaction_amount"]]
    lt1 = lt.groupby("states")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)
    
    fig_lts= px.bar(lt2, x ="states", y="Transaction_amount", title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px. colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= map_trans[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()
    
    fig_htd= px.pie(htd2, values="Transaction_amount", names="Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                   color_discrete_sequence=px. colors.sequential.Emrld_r)
    
    return st. plotly_chart(fig_htd)

def ques4():
    htd= map_trans[["Districts","Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2 = pd.DataFrame(htd1).head(10).reset_index()
    
    fig_htd= px.pie(htd2, values="Transaction_amount", names="Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                        color_discrete_sequence=px. colors.sequential.Greens_r)
    
    return st.plotly_chart(fig_htd)

def ques5():
    sa = map_user[["states","AppOpens"]]
    sa1 = sa.groupby("states")["AppOpens"].sum().sort_values(ascending=False)
    sa2 = pd.DataFrame(sa1).head(10).reset_index()
    
    fig_sa = px.bar(sa2, x="states" ,y="AppOpens", title="Top 10 states with AppOpens",
                     color_discrete_sequence=px. colors.sequential.deep_r)
    
    return st.plotly_chart(fig_sa)

def ques6():
    sa = map_user[["states","AppOpens"]]
    sa1 = sa.groupby("states")["AppOpens"].sum().sort_values(ascending = True)
    sa2 = pd.DataFrame(sa1).head(10).reset_index()
    
    fig_sa = px.bar(sa2, x="states", y="AppOpens", title="lowest 10 states with Appopens",
                     color_discrete_sequence=px. colors.sequential.dense_r)
    
    return st.plotly_chart(fig_sa)

def ques7():
    stc = aggre_trans[["states","Transaction_count"]]
    stc1 = stc.groupby("states")["Transaction_count"].sum().sort_values(ascending =True )
    stc2 = pd.DataFrame(stc1).reset_index()
    
    fig_stc = px.bar(stc2, x="states", y="Transaction_count", title="STATES WITH LOWEST TRANSACTION COUNT",
                      color_discrete_sequence=px. colors.sequential.Jet_r)
    
    return st.plotly_chart(fig_stc)

def ques8():
    stc= aggre_trans[["states", "Transaction_count"]]
    stc1 = stc.groupby("states")["Transaction_count"].sum().sort_values(ascending = False)
    stc2 = pd.DataFrame(stc1).reset_index()
    
    fig_stc = px.bar(stc2, x="states", y="Transaction_count", title="STATES WITH HIGHEST TRANSACTION COUNT",
                       color_discrete_sequence=px.colors.sequential.Magenta_r)
    
    return st.plotly_chart(fig_stc)

def ques9():
    ht= aggre_trans[["states","Transaction_amount"]]
    ht1= ht.groupby("states")["Transaction_amount"].sum().sort_values(ascending =False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)
    
    fig_lts = px.bar(ht2, x= "states", y="Transaction_amount" , title="HIGHEST TRANSACTION AMOUNT and STATES",
                      color_discrete_sequence=px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt = map_trans[["Districts","Transaction_amount"]]
    dt1 = dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending = True)
    dt2 = pd.DataFrame(dt1).reset_index().head(10)
    
    fig_dt = px.bar(dt2, x="Districts", y="Transaction_amount", title="DISTRICTS WITH LOWEST NUMBER OF AMOUNT",
                     color_discrete_sequence=px.colors.sequential.Mint_r)
    
    return st.plotly_chart(fig_dt)

st.set_page_config(layout= "wide")

st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
tab1, tab2, tab3 = st.tabs(["***HOME***","***EXPLORE DATA***","***TOP CHARTS***"])
with tab1:
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("   **-> Credit & Debit card linking**")
        st.write("   **-> Bank Balance check**")
        st.write("   **->Money Storage**")
        st.write("   **->PIN Authorization**")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("c:\\Users\\USER\\Downloads\\phonepe pluse.jpg")

    col3,col4= st.columns(2)
    
    with col3:
        st.video("c:\\Users\\USER\\Downloads\\phonepe pluse.jpg")

    with col4:
        st.write("**-> Easy Transactions**")
        st.write("**-> One App For All Your Payments**")
        st.write("**-> Your Bank Account Is All You Need**")
        st.write("**-> Multiple Payment Modes**")
        st.write("**-> PhonePe Merchants**")
        st.write("**-> Multiple Ways To Pay**")
        st.write("**-> 1.Direct Transfer & More**")
        st.write("**-> 2.QR Code**")
        st.write("**-> Earn Great Rewards**")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("**->No Wallet Top-Up Required**")
        st.write("**->Pay Directly From Any Bank To Any Bank A/C**")
        st.write("**->Instantly & Free**")

    with col6:
        st.video("c:\\Users\\USER\\Downloads\\phonepe pluse.jpg")
        

with tab2:
    sel_year = st.selectbox("select the Year",("All", "2018", "2019", "2020", "2021", "2022", "2023"))
    if sel_year == "All" :
        col1, col2 = st.columns(2)
        with col1:
            animate_all_amount()
            payment_count()
            
        with col2:
            animate_all_count()
            payment_amount()

        state=st.selectbox("selecet the state",('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                'Uttarakhand', 'West Bengal'))
        reg_all_states(state)

    else:
        col1,col2= st.columns(2)

        with col1:
            transaction_amount_year(sel_year)
            payment_count_year(sel_year)

        with col2:
            transaction_count_year(sel_year)
            payment_amount_year(sel_year)
            state= st.selectbox("selecet the state",('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                                  'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                'Uttarakhand', 'West Bengal'))
            reg_state_all_RU(sel_year,state)
            reg_state_all_TA(sel_year,state)

with tab3:
    ques= st.selectbox("select the question",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="Districts With Highest Transaction Amount":
        ques3()

    elif ques=="Top 10 Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="Top 10 States With AppOpens":
        ques5()

    elif ques=="Least 10 States With AppOpens":
        ques6()

    elif ques=="States With Lowest Trasaction Count":
        ques7()

    elif ques=="States With Highest Trasaction Count":
        ques8()

    elif ques=="States With Highest Trasaction Amount":
        ques9()

    elif ques=="Top 50 Districts With Lowest Transaction Amount":
        ques10()

                                                        

                            
