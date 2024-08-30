import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
summary_cases = pd.read_csv('project_data\Summary of cases (rape) 2015-2020.csv',encoding="ISO-8859-1")

# Set the page configuration
st.set_page_config(page_title="Rape Violation Insights Chatbot", layout="wide")

# Function to plot trends for a specific state
def plot_trend(state):
    plt.figure(figsize=(12, 6))
    trend = summary_cases[summary_cases['State/UT'] == state].iloc[:, 2:].values.flatten()
    years = summary_cases.columns[2:]
    plt.plot(years, trend, marker='o', color='purple', linewidth=2, markersize=8)
    plt.title(f'📈 Trend of Rape Cases in {state} (2015-2020)', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of Cases', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)
    st.write(f"The trend shows the number of reported rape cases in **{state}** from 2015 to 2020. Notable fluctuations can be observed, particularly in 2020.")

# Function to create a presentation-like slide
def presentation_slide(title, content):
    st.subheader(title)
    st.write(content)

# Chatbot interface
st.title("🔍 Rape Violation Data Chatbot")
st.write("Explore the data by asking questions about rape violation statistics!")

# User input with a compact design
user_input = st.text_input("Your question:", "", max_chars=100, placeholder="Type your question here...")

if st.button("Submit"):
    if user_input:
        user_input = user_input.lower()

        if "trend" in user_input:
            state = st.selectbox("Select a state:", summary_cases['State/UT'].unique())
            plot_trend(state)
            presentation_slide("Trend Analysis", f"The trend of rape cases in **{state}** shows how the number of reported incidents has changed over the years.")

        elif "total cases in 2018" in user_input:
            total_cases = summary_cases['2018 - CR'].sum()
            st.write(f"The total number of reported rape cases in 2018 was **{total_cases}**.")
            presentation_slide("Total Cases in 2018", f"In 2018, the total number of reported rape cases across all states was **{total_cases}**.")

        elif "highest cases in 2015" in user_input:
            highest_state = summary_cases.loc[summary_cases['2015 - CR'].idxmax(), 'State/UT']
            highest_cases = summary_cases['2015 - CR'].max()
            st.write(f"The state with the highest number of reported cases in 2015 was **{highest_state}** with **{highest_cases}** cases.")
            presentation_slide("Highest Cases in 2015", f"In 2015, **{highest_state}** reported the highest number of rape cases, totaling **{highest_cases}**.")

        elif "compare" in user_input:
            cases_2015 = summary_cases['2015 - CR'].sum()
            cases_2020 = summary_cases['2020 - CR'].sum()
            st.write(f"In 2015, there were **{cases_2015}** cases reported, while in 2020, there were **{cases_2020}** cases.")
            presentation_slide("Comparison of 2015 and 2020", f"The comparison between 2015 and 2020 shows a change in the number of reported cases.")

        else:
            st.write("I'm sorry, I don't understand that question. Please ask about trends or total cases.")
    else:
        st.write("Please enter a question.")