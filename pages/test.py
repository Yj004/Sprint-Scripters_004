import streamlit as st
import pandas as pd
st.title("Test_Page")

st.write("I am Satyajit, this is my page. I will add all my changes here.")
df = pd.read_csv("project_data\Cases (Oldest) 1970.csv")
st.dataframe(df)