# ====================== Imports ======================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scripts.data_loader import load_job_data
from operator import itemgetter

# ====================== Load Data ======================
DS_jobs_df, DS_jobs_df_exploded = load_job_data()

# ====================== Page Setup ======================
st.set_page_config(page_title="Job Market Overview", layout="wide")
st.title("📊 Job Market Overview")
st.markdown("A snapshot of job listings across cities, roles, and experience levels in India.")

# ====================== Dataset Summary ======================
st.subheader("📌 Dataset Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs", f"{len(DS_jobs_df):,}")
col2.metric("Unique Roles", DS_jobs_df['roles'].nunique())
col3.metric("Companies", DS_jobs_df['companies'].nunique())
st.markdown("---")

# ====================== Tabs for Visualization ======================
st.subheader("📍 Explore Job Insights by Category")
tab1, tab2, tab3 = st.tabs(["🏙 Top Hiring Cities", "🧑‍💼 Experience Levels", "📌 Job Roles"])

colors = plt.cm.Set3.colors[:15]

with tab1:
    st.markdown("#### 📍 Top Hiring Cities")
    location_counts = DS_jobs_df.locations.apply(pd.Series).stack().str.strip().value_counts().head(10)
    fig1, ax1 = plt.subplots()
    ax1.pie(
        location_counts,
        labels=location_counts.index,
        colors=colors,
        startangle=90,
        autopct="%1.1f%%",
        wedgeprops=dict(width=0.3, edgecolor='w')
    )
    ax1.set_title("Top Job Locations")
    centre_circle = plt.Circle((0, 0), 0.60, fc='white')
    fig1.gca().add_artist(centre_circle)
    ax1.axis('equal')
    st.pyplot(fig1)

with tab2:
    st.markdown("#### 👨‍💼 Experience Required")
    experience_count = DS_jobs_df["experience"].value_counts().head(7)
    fig2, ax2 = plt.subplots()
    experience_count.plot.barh(color=colors, ax=ax2)
    ax2.set_xlabel("No. of Vacancies", weight='bold')
    ax2.set_ylabel("Experience", weight='bold')
    ax2.set_title("Required Experience Levels", weight='bold')
    st.pyplot(fig2)

with tab3:
    st.markdown("#### 💼 Most Common Job Titles")
    role_counts = DS_jobs_df["roles"].value_counts().head(7)
    role_percentages = role_counts / role_counts.sum() * 100
    fig3, ax3 = plt.subplots()
    role_percentages.plot.bar(color=colors, ax=ax3)
    ax3.set_title("Top Data Science Job Titles", weight='bold')
    ax3.set_ylabel("Vacancy Percentage", weight='bold')
    ax3.set_xlabel("Roles", weight='bold')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig3)
