import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
st.title("landing page")

# Read data
df = pd.read_csv("project_data/World Wide Cases detail.csv",encoding="ISO-8859-1")
st.dataframe(df)

# Get data for the selected years
selected_years = st.sidebar.multiselect(label="Year", options=df["Year"].drop_duplicates())
filter1 = df["Year"].isin(selected_years)
filtered_data = df[filter1]

# get numnber of cases category wise
category_crime = filtered_data.groupby(["Category"],as_index=False).agg({"VALUE":"sum"})
st.dataframe(category_crime)
st.bar_chart(data=category_crime,x="Category",y="VALUE",x_label="category",y_label="Rape_cases")

# Region wise crime cases
region_crime = filtered_data.groupby("Region",as_index=False).agg({"VALUE":"sum"})
st.dataframe(region_crime)
fig = px.pie(data_frame=region_crime,names="Region",values="VALUE",title="Region wise cases")
st.plotly_chart(fig)
