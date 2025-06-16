import streamlit as st
import pandas as pd

def apply_filters(df):
    """
    Apply sidebar filters to the DataFrame and return the filtered DataFrame.
    """

    st.sidebar.header("🔎 Filter Jobs")

    # Filter by location
    all_locations = sorted(set([loc.strip() for sublist in df['locations'] for loc in sublist]))
    selected_locations = st.sidebar.multiselect("📍 Select Location(s)", all_locations)

    # Filter by experience
    all_experience = sorted(df['experience'].unique())
    selected_experience = st.sidebar.multiselect("💼 Experience Level", all_experience)

    # Filter by role
    all_roles = sorted(df['roles'].unique())
    selected_roles = st.sidebar.multiselect("🧪 Role", all_roles)

    # Apply filters
    filtered_df = df.copy()

    if selected_locations:
        filtered_df = filtered_df[filtered_df['locations'].apply(
            lambda locs: any(loc in selected_locations for loc in locs)
        )]

    if selected_experience:
        filtered_df = filtered_df[filtered_df['experience'].isin(selected_experience)]

    if selected_roles:
        filtered_df = filtered_df[filtered_df['roles'].isin(selected_roles)]

    return filtered_df
