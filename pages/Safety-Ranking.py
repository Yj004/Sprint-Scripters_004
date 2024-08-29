import pandas as pd
import streamlit as st
import plotly.express as px

# Set page config to wide layout
st.set_page_config(layout="wide")

# Load data
data_path = "D:/masai projects/Sprint-Scripters_004/project_data/Detailed Cases (Registered) sexual Assault 2001-2008.csv"
data_path2 = "Y:/masai projects/Sprint-Scripters_004/project_data/World Wide Cases detail.csv"

try:
    detailed_cases_df = pd.read_csv(data_path)
    worldwide_cases_df = pd.read_csv(data_path2,encoding='ISO-8859-1')
except FileNotFoundError:
    st.error(f"File not found. Please check the file path.")
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
    'Rape Cases (Total) No. of Victims - (30-50) Years': 'Victims (30-50) Years',
    'Rape Cases (Total) No. of Victims - Above 50 Years': 'Victims Above 50 Years'
}

age_group_reverse_mapping = {v: k for k, v in age_group_display_names.items()}

# Sidebar for age group selection with user-friendly names (single select)
selected_age_group_display = st.sidebar.selectbox(
    'Select Age Group', list(age_group_display_names.values())
)
selected_age_group = age_group_reverse_mapping[selected_age_group_display]

# Filter the DataFrame based on the selected state, year, and age group
filtered_df = detailed_cases_df[
    (detailed_cases_df['States/ UTs/Cities'] == selected_state) & 
    (detailed_cases_df['Year'].isin(selected_years))
]

# Merge the 18-30 age group into the 30-50 age group
if 'Rape Cases (Total) No. of Victims - (18-30) Years' in filtered_df.columns and 'Rape Cases (Total) No. of Victims - (30-50) Years' in filtered_df.columns:
    filtered_df['Rape Cases (Total) No. of Victims - (30-50) Years'] += filtered_df['Rape Cases (Total) No. of Victims - (18-30) Years']
    filtered_df = filtered_df.drop(columns=['Rape Cases (Total) No. of Victims - (18-30) Years'])

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

    # Create a layout for full-screen charts and explanation
    with st.container():
        col1, col2 = st.columns([1, 1])  # Equal width for both columns

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
        
        # Calculate state rankings for girl safety
        state_totals = detailed_cases_df.groupby('States/ UTs/Cities')[selected_age_group].sum().sort_values(ascending=False)
        state_ranking = state_totals.reset_index()
        state_ranking.columns = ['State', 'Total Cases']

        # Find the rank of the selected state
        selected_state_rank = state_ranking[state_ranking['State'] == selected_state].index[0] + 1
        total_states = len(state_ranking)
        rank_info = f"{selected_state} is ranked {selected_state_rank} out of {total_states} states based on the total number of {selected_age_group_display} cases."

        # Add state ranking to explanation
        explanation = f"""
        <div style="background-color: #2e2e2e; padding: 20px; border-radius: 10px; color: #ffffff; border: 1px solid #2e2e2e;">
            <h3 style="color: #ff9900;">Insights on {selected_age_group_display}</h3>
            <p>Here's how the distribution of {selected_age_group_display} cases has evolved in {selected_state} over the selected years.</p>
            <p><strong>Total cases:</strong> {filtered_df[selected_age_group].sum()}</p>
            <p>If recent years show an increase in cases, it might indicate greater awareness or improved reporting mechanisms. For instance, a significant rise in {filtered_df[filtered_df[selected_age_group] == filtered_df[selected_age_group].max()]['Year'].values[0]} may reflect heightened attention during that period.</p>
            <p>Conversely, if the numbers are stable or decreasing, it could suggest successful preventive measures or better support systems. For example, the decline in {filtered_df[filtered_df[selected_age_group] == filtered_df[selected_age_group].min()]['Year'].values[0]} might be due to effective outreach and prevention strategies.</p>
            <h4 style="color: #ff9900;">State Ranking for Girl Safety</h4>
            <b>{rank_info}</b>
        </div>
        """
        st.markdown(explanation, unsafe_allow_html=True)

else:
    st.write("No data available for the selected filters.")

