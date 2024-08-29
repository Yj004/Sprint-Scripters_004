import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

st.title( u"\u2757" + "World Data Analysis")

# Read data
df = pd.read_csv("project_data/World Wide Cases detail.csv",encoding="ISO-8859-1")

# Get data for the selected years
selected_years = st.sidebar.multiselect(label="select years", options=df["Year"].drop_duplicates(),default=2003)
filter1 = df["Year"].isin(selected_years)
filtered_data = df[filter1]

# get numnber of cases category wise
category_crime = filtered_data.groupby(["Category"],as_index=False).agg({"VALUE":"sum"})
st.bar_chart(data=category_crime,x="Category",y="VALUE",x_label="category",y_label="Rape_cases")

# Region wise crime cases
region_crime = filtered_data.groupby("Region",as_index=False).agg({"VALUE":"sum"})
col1,col2=st.columns(2)
with col1:
    fig = px.pie(data_frame=region_crime,names="Region",values="VALUE",title="Region wise cases")
    st.plotly_chart(fig)
with col2:
    st.header("Region wise crimes")
    st.dataframe(region_crime)

selected_column = st.sidebar.selectbox(label="select column",options=["Country","Category","Region"])
    
    
if selected_column=="Country":
    default_value= "Bulgaria"
elif selected_column=="Category":
    default_value="Kidnapping"
else:
    default_value="Americas"
        
selected_members = st.sidebar.multiselect(label="select members", options=df[selected_column].drop_duplicates(),default=default_value)

filter2= df["Year"].isin(selected_years) & df[selected_column].isin(selected_members)
filtered_df = df[filter2]
col3, col4, col5, col6 = st.columns(4)
with col3:
    st.header("Min")
    st.write(np.min(filtered_df["VALUE"]))
with col4:
    st.header("Max")
    st.write(np.max(filtered_df["VALUE"]))
with col5:
    st.header("Mean")
    st.write(np.mean(filtered_df["VALUE"]))
with col6:
    st.header("Variance")
    st.write(np.std(filtered_df["VALUE"]))
st.dataframe(filtered_df)
    
st.title("State wise summary of cases")  
df1 = pd.read_csv("project_data/Summary of cases (rape) 2015-2020.csv")
st.dataframe(df1)

option = st.radio("Choose one option:", ("State wise trend","Anuual trend"))
if option == "State wise trend":
    select_state = st.selectbox(label="select a state",options=df1["State/UT"].drop_duplicates())
    filter4 = df1["State/UT"] == select_state
    filtered_state = df1[filter4]
    st.dataframe(filtered_state)
    filtered_state.drop(columns=["Sl. No.","State/UT"],inplace=True)
    final_data = filtered_state.iloc[0]
    
    df2 = pd.DataFrame({"Year":final_data.index,"Case_reported":final_data.values})
    
    st.line_chart(data=df2,x="Year",y="Case_reported",x_label="Years",y_label="Case_repoted")
else:
    select_year = st.selectbox(label="select a year",options=["2015 - CR","2016 - CR","2017 - CR","2018 - CR","2019 - CR","2020 - CR"])
    st.bar_chart(data=df1,x="State/UT",y=select_year,x_label="States",y_label="case_reported")
