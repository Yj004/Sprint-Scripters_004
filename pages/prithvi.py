import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Sexual Assault Data Analysis App")

# Load the datasets (Make sure the CSV files are in the same directory as your streamlit app)
summary_cases = pd.read_csv('project_data\Summary of cases (rape) 2015-2020.csv', encoding='ISO-8859-1')
detailed_cases_2001_2008 = pd.read_csv('project_data\Detailed Cases (Registered) sexual Assault 2001-2008.csv', encoding='ISO-8859-1')
cases_oldest_1970 = pd.read_csv('project_data\Cases (Oldest) 1970.csv', encoding='ISO-8859-1')
worldwide_cases = pd.read_csv('project_data\World Wide Cases detail.csv', encoding='ISO-8859-1')
detailed_registered_unregistered_2018 = pd.read_csv('project_data\Detailed Register and Unregistered cases (Sexual assault) (Punished Release) 2018.csv', encoding='ISO-8859-1')
state_wise_sexual_assault_1999_2013 = pd.read_csv('project_data\State wise Sexual Assault (Detailed) 1999 - 2013.csv', encoding='ISO-8859-1')

# Display the first few rows of each dataset
st.subheader("Summary of Cases (Rape) 2015-2020:")
st.dataframe(summary_cases.head())

st.subheader("Detailed Cases (Registered) Sexual Assault 2001-2008:")
st.dataframe(detailed_cases_2001_2008.head())

st.subheader("Cases (Oldest) 1970:")
st.dataframe(cases_oldest_1970.head())

st.subheader("Worldwide Cases Details:")
st.dataframe(worldwide_cases.head())

st.subheader("Detailed Registered and Unregistered Cases (Sexual Assault) 2018:")
st.dataframe(detailed_registered_unregistered_2018.head())

st.subheader("State-wise Sexual Assault (Detailed) 1999-2013:")
st.dataframe(state_wise_sexual_assault_1999_2013.head())

# Function to clean the dataset
def clean_data(df, name):
    print(f"\nCleaning Data for {name}:")

    # Check for duplicates
    duplicates = df.duplicated().sum()
    print(f"Number of duplicate rows: {duplicates}")

    # Handle missing values for Detailed Cases (Registered) Sexual Assault 2001-2008
    if name == "Detailed Cases (Registered) Sexual Assault 2001-2008":
        for col in df.select_dtypes(include=['float64']).columns:
            if df[col].isnull().sum() > 0:
                mean_value = df[col].mean()
                df[col].fillna(mean_value, inplace=True)
                print(f"Filled missing values in {col} with mean: {mean_value}")

    # Handle missing values for Cases (Oldest) 1970
    if name == "Cases (Oldest) 1970":
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                df[col].fillna(method='ffill', inplace=True)  # Forward fill as an example
                print(f"Filled missing values in {col} using forward fill.")

    # Convert data types if necessary
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = df[col].astype(int)

    # Check for missing values after cleaning
    print("Missing Values After Cleaning:")
    print(df.isnull().sum())

# Clean the datasets
clean_data(detailed_cases_2001_2008, "Detailed Cases (Registered) Sexual Assault 2001-2008")
clean_data(cases_oldest_1970, "Cases (Oldest) 1970")
clean_data(state_wise_sexual_assault_1999_2013, "State-wise Sexual Assault (Detailed) 1999-2013")

# Function to convert data types
def convert_data_types(df, name):
    print(f"\nConverting Data Types for {name}:")

    # Convert float64 to int64 where appropriate
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = df[col].astype(int)
        print(f"Converted {col} to int64.")

    # Check data types after conversion
    print("Data Types After Conversion:")
    print(df.dtypes)

# Convert data types for each dataset
convert_data_types(summary_cases, "Summary of Cases (Rape) 2015-2020")
convert_data_types(detailed_cases_2001_2008, "Detailed Cases (Registered) Sexual Assault 2001-2008")
convert_data_types(cases_oldest_1970, "Cases (Oldest) 1970")
convert_data_types(worldwide_cases, "Worldwide Cases Details")
convert_data_types(detailed_registered_unregistered_2018, "Detailed Registered and Unregistered Cases (Sexual Assault) 2018")
convert_data_types(state_wise_sexual_assault_1999_2013, "State-wise Sexual Assault (Detailed) 1999-2013")

# Function to convert object columns to numeric
def convert_object_to_numeric(df, name):
    print(f"\nConverting Object Columns to Numeric for {name}:")

    # Convert relevant columns to numeric, coercing errors
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = pd.to_numeric(df[col], errors='coerce')
            print(f"Converted {col} to numeric.")

    # Check data types after conversion
    print("Data Types After Conversion:")
    print(df.dtypes)

# Convert object columns for State-wise Sexual Assault (Detailed) 1999-2013
convert_object_to_numeric(state_wise_sexual_assault_1999_2013, "State-wise Sexual Assault (Detailed) 1999-2013")

# Set the style for the plots
sns.set(style="whitegrid")

# Function to plot trends over the years for Summary of Cases
def plot_trends(df):
    plt.figure(figsize=(12, 6))
    years = df.columns[2:]  # Get the year columns
    plt.plot(years, df.iloc[0, 2:], marker='o', label='Andhra Pradesh')  # Example for one state
    plt.title('Trends in Rape Cases (2015-2020) for Andhra Pradesh')
    plt.xlabel('Year')
    plt.ylabel('Number of Cases Reported')
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(plt) # Add this line to display the plot in Streamlit

# Plot trends for Summary of Cases (Rape) 2015-2020
plot_trends(summary_cases)

# Function to plot the distribution of cases in Detailed Cases
def plot_distribution(df, column):
    plt.figure(figsize=(12, 6))
    sns.histplot(df[column], bins=30, kde=True)
    plt.title(f'Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    st.pyplot(plt) # Add this line to display the plot in Streamlit

# Plot distribution for a specific column in Detailed Cases
plot_distribution(detailed_cases_2001_2008, 'Incest (Rape) - No. of Cases Reported')


def plot_multiple_states_trends(df, states):
    plt.figure(figsize=(12, 6))
    for state in states:
        plt.plot(df[df['State/UT'] == state].columns[2:], df[df['State/UT'] == state].iloc[0, 2:], marker='o', label=state)
    plt.title('Trends in Rape Cases (2015-2020) for Selected States')
    plt.xlabel('Year')
    plt.ylabel('Number of Cases Reported')
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(plt) # Add this line to display the plot in Streamlit

# Example: Plot trends for multiple states
selected_states = ['Andhra Pradesh', 'Bihar', 'Maharashtra']  # Add more states as needed
plot_multiple_states_trends(summary_cases, selected_states)

# Example: Analyze the number of cases reported for Incest and Other Rape
incest_cases = detailed_cases_2001_2008[['Incest (Rape) - No. of Cases Reported', 
                                           'Incest (Rape) No. of Victims - Upto 10 Years',
                                           'Incest (Rape) No. of Victims - (10-14) Years',
                                           'Incest (Rape) No. of Victims - (14-18) Years',
                                           'Incest (Rape) No. of Victims - (18-30)Years',
                                           'Incest (Rape) No. of Victims - (30-50) Years',
                                           'Incest (Rape) No. of Victims - Above 50 Years']].sum()

other_cases = detailed_cases_2001_2008[['Other (Rape) - No. of Cases Reported', 
                                          'Other (Rape) No. of Victims - Upto 10 Years',
                                          'Other (Rape) No. of Victims - (10-14) Years',
                                          'Other (Rape) No. of Victims - (14-18) Years',
                                          'Other (Rape) No. of Victims - (18-30)Years',
                                          'Other (Rape) No. of Victims - (30-50) Years',
                                          'Other (Rape) No. of Victims - Above 50 Years']].sum()

# Create a bar chart for Incest Cases
plt.figure(figsize=(12, 6))
sns.barplot(x=incest_cases.index, y=incest_cases.values)
plt.title('Number of Incest Rape Cases Reported by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Number of Cases')
plt.xticks(rotation=45)
st.pyplot(plt) # Add this line to display the plot in Streamlit

# Create a bar chart for Other Rape Cases
plt.figure(figsize=(12, 6))
sns.barplot(x=other_cases.index, y=other_cases.values)
plt.title('Number of Other Rape Cases Reported by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Number of Cases')
plt.xticks(rotation=45)
st.pyplot(plt) # Add this line to display the plot in Streamlit