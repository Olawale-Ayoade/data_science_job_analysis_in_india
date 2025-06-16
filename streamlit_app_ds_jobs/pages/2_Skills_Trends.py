import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scripts.data_loader import load_job_data
from operator import itemgetter

# -----------------------------
# Load Data
# -----------------------------
DS_jobs_df, _ = load_job_data()

# -----------------------------
# Page Config & Title
# -----------------------------
st.set_page_config(page_title="Skills Trends", layout="wide")
st.title("⚙️ Skills Trends in Data Science Jobs")
st.markdown("Explore the most in-demand tools, platforms, and skills in the Indian job market.")

# -----------------------------
# Prepare Skills Series
# -----------------------------
skills_series = DS_jobs_df['skills'].str.split(',').explode().str.strip()
colors = plt.cm.Set3.colors[:15]  # Color palette

# -----------------------------
# Tabs for Interactive Navigation
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔝 Top Skills",
    "💻 Programming Languages",
    "☁️ Cloud Platforms",
    "📊 Visualization Tools",
    "🧠 Deep Learning"
])

# -----------------------------
# Top Skills
# -----------------------------
with tab1:
    st.subheader("🔝 Top Skills")
    top_skills = skills_series.value_counts().head(15)
    fig1, ax1 = plt.subplots()
    top_skills.plot(kind="bar", color=colors, ax=ax1)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Frequency", weight='bold')
    plt.xlabel("Skills", weight='bold')
    plt.title("Top Required Skills for Data Science Jobs", weight='bold')
    st.pyplot(fig1)

# -----------------------------
# Programming Languages
# -----------------------------
with tab2:
    st.subheader("💻 Programming Languages")
    languages = {
        "python": "python",
        "r": "^r$",
        "java": "java$",
        "c++": "c\+",
        "matlab": "matlab",
        "sas": "sas",
        "sql": "sql(?!.*no)"
    }
    lang_counts = {
        lang: skills_series[skills_series.str.contains(pattern, case=False, regex=True)].count()
        for lang, pattern in languages.items()
    }
    lang_series = pd.Series(lang_counts).sort_values(ascending=False)
    fig2, ax2 = plt.subplots()
    lang_series.plot(kind="bar", color=colors, ax=ax2)
    ax2.set_title("Programming Language Mentions", weight='bold')
    ax2.set_ylabel("Count", weight='bold')
    st.pyplot(fig2)

# -----------------------------
# Cloud Platforms
# -----------------------------
with tab3:
    st.subheader("☁️ Cloud Platforms")
    skl_df = pd.DataFrame(DS_jobs_df.skills.apply(pd.Series).stack().value_counts()).reset_index()
    skl_df.columns = ["skills", "count"]
    cloud = {
        'aws': skl_df["count"][skl_df['skills'].str.contains('aws', regex=True)].sum(),
        'azure': skl_df["count"][skl_df['skills'].str.contains('azure', regex=True)].sum(),
        'gcp': skl_df["count"][skl_df['skills'].str.contains('gcp')].sum(),
    }
    cloud = dict(sorted(cloud.items(), key=itemgetter(1), reverse=True))
    fig3, ax3 = plt.subplots()
    plt.bar(cloud.keys(), cloud.values(), color=colors, width=.45)
    plt.xticks(rotation=45)
    plt.title("Cloud Platforms Demand", weight='bold')
    st.pyplot(fig3)

# -----------------------------
# Visualization Tools
# -----------------------------
with tab4:
    st.subheader("📊 Visualization Tools")
    viz_patterns = {
        "Tableau": r"tableau",
        "Power BI": r"power\s*bi",
        "Looker": r"looker",
        "Qlik": r"qlik",
        "Plotly/Dash": r"plotly|dash"
    }
    viz_count = {
        name: skills_series[skills_series.str.contains(pattern, case=False, regex=True)].count()
        for name, pattern in viz_patterns.items()
    }
    viz_series = pd.Series(viz_count).sort_values(ascending=False)
    fig4, ax4 = plt.subplots()
    viz_series.plot(kind="bar", color=colors, ax=ax4)
    ax4.set_title("Data Visualization Tools", weight='bold')
    ax4.set_ylabel("Mentions", weight='bold')
    st.pyplot(fig4)

# -----------------------------
# Deep Learning Frameworks
# -----------------------------
with tab5:
    st.subheader("🧠 Deep Learning Frameworks")
    dl_frameworks = ['tensorflow', 'keras', 'torch']
    dl_counts = {
        fw: skills_series[skills_series.str.contains(fw, case=False)].count()
        for fw in dl_frameworks
    }
    dl_series = pd.Series(dl_counts).sort_values(ascending=False)
    fig5, ax5 = plt.subplots()
    dl_series.plot(kind="bar", color=colors, ax=ax5)
    ax5.set_title("Deep Learning Libraries", weight='bold')
    st.pyplot(fig5)
