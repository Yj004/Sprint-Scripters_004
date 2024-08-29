import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
data_path = "D:/masai projects/Sprint-Scripters_004/project_data/Detailed Cases (Registered) sexual Assault 2001-2008.csv"
try:
    detailed_cases_df = pd.read_csv(data_path)
except FileNotFoundError:
    st.error(f"File not found at {data_path}. Please check the file path.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the data: {e}")
    st.stop()

st.title('Rape Cases Data Display')

# Sidebar for state selection
states = detailed_cases_df['States/ UTs/Cities'].unique()
selected_state = st.sidebar.selectbox('Select a State/UT/City', states)

# Sidebar for year selection
years = detailed_cases_df['Year'].unique()
selected_years = st.sidebar.multiselect('Select Year(s)', years, default=years)

# Age group display names mapping
age_group_display_names = {
    'Rape Cases (Total) No. of Victims - Upto 10 Years': 'Victims Upto 10 Years',
    'Rape Cases (Total) No. of Victims - (10-14) Years': 'Victims (10-14) Years',
    'Rape Cases (Total) No. of Victims - (14-18) Years': 'Victims (14-18) Years',
    'Rape Cases (Total) No. of Victims - (18-30) Years': 'Victims (18-30) Years',
    'Rape Cases (Total) No. of Victims - (30-50) Years': 'Victims (30-50) Years',
    'Rape Cases (Total) No. of Victims - Above 50 Years': 'Victims Above 50 Years'
}

# Reverse mapping for easy access to original column names
age_group_reverse_mapping = {v: k for k, v in age_group_display_names.items()}

# Sidebar for age group selection with user-friendly names (single select)
selected_age_group_display = st.sidebar.selectbox(
    'Select Age Group', list(age_group_display_names.values())
)

# Map selected display name back to original column name
selected_age_group = age_group_reverse_mapping[selected_age_group_display]

# Filter the DataFrame based on the selected state, year, and age group
filtered_df = detailed_cases_df[
    (detailed_cases_df['States/ UTs/Cities'] == selected_state) & 
    (detailed_cases_df['Year'].isin(selected_years))
]

# EDA: Calculate the change in cases
if not filtered_df.empty:
    # Sort by year
    filtered_df.sort_values(by='Year', inplace=True)
    
    # Calculate year-over-year change
    filtered_df['Change'] = filtered_df[selected_age_group].diff().fillna(0)
    
    # Calculate percentage change with a small constant to avoid division by zero
    filtered_df['Percentage Change'] = (
        (filtered_df['Change'] / (filtered_df[selected_age_group].shift(1) + 1e-6)) * 100
    ).fillna(0)

    # Remove 'Change' column if not needed in the display
    filtered_df = filtered_df.drop(columns=['Change'])

    # Display the filtered DataFrame
    st.write(f'Detailed Cases DataFrame for {selected_state} in {selected_years} for {selected_age_group_display}:')
    st.dataframe(filtered_df[['Year', 'States/ UTs/Cities', selected_age_group, 'Percentage Change']])

    # Create a layout for full-screen charts
    col1, col2 = st.columns([1, 1])  # Adjust column ratio as needed

    with col1:
        # Bar Graph for the filtered data using Plotly
        fig_bar = px.bar(filtered_df, x='Year', y=selected_age_group, title=f'Total {selected_age_group_display} in {selected_state} by Year')
        fig_bar.update_layout(
            xaxis_title='Year',
            yaxis_title=f'Total {selected_age_group_display}',
            title_font_color='white',
            xaxis_title_font_color='white',
            yaxis_title_font_color='white',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            margin=dict(l=0, r=0, t=40, b=0)  # Adjust margins to reduce excess space
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # Pie Chart for the filtered data using Plotly
        fig_pie = px.pie(filtered_df, names='Year', values=selected_age_group, title=f'{selected_age_group_display} Distribution in {selected_state}')
        fig_pie.update_layout(
            title_font_color='white',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            margin=dict(l=0, r=0, t=40, b=0)  # Adjust margins to reduce excess space
        )
        st.plotly_chart(fig_pie, use_container_width=True)

else:
    st.write("No data available for the selected filters.")
