import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


# Load the dataset
df = pd.read_csv("project_data/Detailed Cases (Registered) sexual Assault 2001-2008.csv")

# Sidebar for filtering
st.sidebar.title("Filter Options")

# Year filter
years = df['Year'].unique()
selected_years = st.sidebar.multiselect('Select Year(s):', options=years, default=years)

# Age category filter
age_categories = [
    'Upto 10 Years',
    '10-14 Years',
    '14-18 Years',
    '18-30 Years',
    '30-50 Years',
    'Above 50 Years'
]
selected_age_categories = st.sidebar.multiselect('Select Age Categories:', options=age_categories, default=age_categories)

# Filter data based on selections
filtered_df = df[df['Year'].isin(selected_years)]

# Sample data for age categories (replace these with actual data from your dataset)
age_data = {
    'Age Category': [
        'Upto 10 Years',
        '10-14 Years',
        '14-18 Years',
        '18-30 Years',
        '30-50 Years',
        'Above 50 Years'
    ],
    'Victim Count': [
        100,  # rape_upto_10
        150,  # rape_upto_10to14
        200,  # rape_upto_14to18
        300,  # rape_upto_18to30
        250,  # rape_upto_30to50
        100   # rape_above_50
    ]
}

# Convert age data to DataFrame
age_df = pd.DataFrame(age_data)

# Filtering the age-related data
filtered_age_df = age_df[age_df['Age Category'].isin(selected_age_categories)]

# Group by Year and sum the cases for the rape cases by category
ins1 = filtered_df[["Year", "Incest (Rape) - No. of Cases Reported", "Other (Rape) - No. of Cases Reported","Rape Cases (Total) - No. of Cases Reported"]].groupby("Year").sum().reset_index()

# Calculate total cases and percentages
total_rape = ins1["Rape Cases (Total) - No. of Cases Reported"].sum()
total_incest_rape = ins1["Incest (Rape) - No. of Cases Reported"].sum() / total_rape * 100
total_other_rape = ins1["Other (Rape) - No. of Cases Reported"].sum() / total_rape * 100

# Data for the chart
categories = ['Incest Rape', 'Other Rape']
percentages = [total_incest_rape, total_other_rape]

# Streamlit section for Rape Cases by Category
st.title('Percentage of Rape Cases by Category')

# Create the bar chart with enhanced style
fig, ax = plt.subplots(figsize=(10, 6))
sns.set(style="whitegrid")
colors = sns.color_palette("pastel")[0:2]
bars = ax.bar(categories, percentages, color=colors, edgecolor='black')

# Add labels and title
ax.set_xlabel('Rape Category', fontsize=14, fontweight='bold')
ax.set_ylabel('Percentage (%)', fontsize=14, fontweight='bold')
ax.set_title('Percentage of Rape Cases by Category', fontsize=16, fontweight='bold')

# Add numbers above bars with a more readable font
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.1f}%', ha='center', va='bottom', fontsize=12, color='black')

# Show gridlines for better readability
ax.yaxis.grid(True, linestyle='--', alpha=0.7)

# Improve layout and aesthetics
fig.tight_layout()
st.pyplot(fig)

# Display additional information
st.write(f"**Total Rape Cases (Filtered):** {total_rape}")
st.write(f"**Total Incest Rape Cases (Filtered):** {ins1['Incest (Rape) - No. of Cases Reported'].sum()}")
st.write(f"**Total Other Rape Cases (Filtered):** {ins1['Other (Rape) - No. of Cases Reported'].sum()}")

# Streamlit section for Number of Rape Victims by Age Category
st.title('Number of Rape Victims by Age Category (2001 - 2008)')

# Create the bar chart with enhanced style
fig, ax = plt.subplots(figsize=(12, 8))
sns.set(style="whitegrid")
bars = ax.bar(filtered_age_df['Age Category'], filtered_age_df['Victim Count'], color='skyblue', edgecolor='black')

# Add labels and title
ax.set_xlabel('Age Categories', fontsize=14, fontweight='bold')
ax.set_ylabel('Number of Victims', fontsize=14, fontweight='bold')
ax.set_title('Number of Rape Victims by Age Category (2001 - 2008)', fontsize=16, fontweight='bold')

# Add numbers above bars with a more readable font
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 10, f'{yval:,}', ha='center', va='bottom', fontsize=12, color='black')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Show gridlines for better readability
ax.yaxis.grid(True, linestyle='--', alpha=0.7)

# Improve layout and aesthetics
fig.tight_layout()
st.pyplot(fig)

# Calculate age group distribution
age_below18 = filtered_age_df[filtered_age_df['Age Category'].isin(['Upto 10 Years', '10-14 Years', '14-18 Years'])]['Victim Count'].sum()
age_above18 = filtered_age_df[filtered_age_df['Age Category'].isin(['18-30 Years', '30-50 Years', 'Above 50 Years'])]['Victim Count'].sum()

# Streamlit section for Distribution of Rape Cases by Age Group
st.title('Distribution of Rape Cases by Age Group')

# Create the pie chart
fig, ax = plt.subplots(figsize=(8, 8))
colors = sns.color_palette("pastel")[2:4]
wedges, texts, autotexts = ax.pie([age_below18, age_above18], labels=['Below 18 Years', 'Above 18 Years'],
                                  colors=colors, autopct='%1.1f%%', startangle=140)

# Add legend
ax.legend(wedges, ['Below 18 Years', 'Above 18 Years'], title="Age Group", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

# Set title
ax.set_title('Distribution of Rape Cases by Age Group')

# Style pie chart
for text in autotexts:
    text.set_color('black')
    text.set_fontsize(12)

# Show the plot in Streamlit
st.pyplot(fig)

# Display additional information
st.write("The pie chart above shows the distribution of rape cases categorized by age group for the selected years and age categories.")
