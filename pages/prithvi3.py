import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
summary_cases = pd.read_csv('project_data/Summary of cases (rape) 2015-2020.csv')

# Set the page configuration
st.set_page_config(page_title="Rape Violation Insights", layout="wide")

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

# Function to create a presentation-like slide
def presentation_slide(title, content):
    st.subheader(title)
    st.write(content)

# Interactive storytelling interface
st.title("🔍 Prithvi3 - Story Telling")
st.write("Explore the data through interactive slides and visualizations!")

# Slide navigation
slide_number = st.slider("Select Slide:", 1, 6)

if slide_number == 1:
    st.header("📖 Introduction")
    st.write("This interactive presentation explores the trends and statistics of rape cases in India from 2015 to 2020.")
    st.write("The data highlights the ongoing issue of sexual violence in India and the need for effective policies.")

elif slide_number == 2:
    st.header("📊 Total Cases in 2018")
    total_cases = summary_cases['2018 - CR'].sum()
    st.write(f"The total number of reported rape cases in 2018 was **{total_cases}**.")
    presentation_slide("Total Cases in 2018", f"In 2018, the total number of reported rape cases across all states was **{total_cases}**. This figure highlights the ongoing issue of sexual violence in India.")

elif slide_number == 3:
    st.header("📈 Trend Analysis")
    state = st.selectbox("Select a state:", summary_cases['State/UT'].unique())
    plot_trend(state)
    presentation_slide("Trend Analysis", f"The trend of rape cases in **{state}** shows how the number of reported incidents has changed over the years. This can help identify patterns and inform policy decisions.")

elif slide_number == 4:
    st.header("  Highest Cases in 2015")
    highest_state = summary_cases.loc[summary_cases['2015 - CR'].idxmax(), 'State/UT']
    highest_cases = summary_cases['2015 - CR'].max()
    st.write(f"The state with the highest number of reported cases in 2015 was **{highest_state}** with **{highest_cases}** cases.")
    presentation_slide("Highest Cases in 2015", f"In 2015, **{highest_state}** reported the highest number of rape cases, totaling **{highest_cases}**. This raises questions about the factors contributing to this statistic.")

elif slide_number == 5:
    st.header("🔄 Comparison of 2015 and 2020")
    cases_2015 = summary_cases['2015 - CR'].sum()
    cases_2020 = summary_cases['2020 - CR'].sum()
    st.write(f"In 2015, there were **{cases_2015}** cases reported, while in 2020, there were **{cases_2020}** cases.")
    presentation_slide("Comparison of 2015 and 2020", f"The comparison between 2015 and 2020 shows a change in the number of reported cases, which can be analyzed to understand trends over time.")

elif slide_number == 6:
    st.header("🔚 Conclusion")
    st.write("The data highlights the ongoing issue of sexual violence in India and the need for effective policies.")
    st.write("By understanding the trends and statistics, we can work towards creating a safer environment for all.")

# Additional Features: User Feedback
st.sidebar.header("💬 User Feedback")
feedback = st.sidebar.text_area("Please provide your feedback or suggestions:")
if st.sidebar.button("Submit Feedback"):
    st.sidebar.success("Thank you for your feedback! We appreciate your input.")