# ====================== Imports ======================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scripts.data_loader import load_job_data  # ✅ Load cleaned dataset

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

# ====================== Top Hiring Cities ======================

st.subheader("📍 Top Hiring Cities")

# link of differnt collor pallets: https://matplotlib.org/stable/users/explain/colors/colormaps.html
colors = plt.cm.Set3.colors[:15]  # You can try 'Accent', 'tab10', or 'Dark2' for variety.

# Top 10 locations with most data scientist jobs
location_counts = DS_jobs_df.locations.apply(pd.Series).stack().str.strip().value_counts()[:10]

# plot in a donut-style pie chart
plt.pie(
    location_counts,
    colors = colors,
    labels=location_counts.index,
    startangle=10,
    autopct='%1.1f%%',
    wedgeprops=dict(width=0.3, edgecolor='w')
)

plt.title("Top Job Locations", weight='bold')

# Add a white circle at the center to create the donut effect
centre_circle = plt.Circle((0, 0), 0.60, fc='white', linewidth=1.25)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.axis('equal') # ensure the pie is drawn as a circle
plt.tight_layout()
st.pyplot(fig)

# ====================== Most Common Job Titles ======================
st.subheader("💼 Most Common Job Titles")

role_counts = DS_jobs_df["roles"].value_counts()[:7]
role_percentages = role_counts / role_counts.sum() * 100

fig2, ax2 = plt.subplots()
role_percentages.plot.bar(color=colors, ax=ax2)
plt.xticks(rotation=45, ha='right')
plt.title("Data Scientist Roles", weight='bold')
plt.ylabel("Vacancy Percentage", rotation=90, weight='bold')
plt.xlabel("Roles", weight='bold')
st.pyplot(fig2)

# ====================== Experience Required ======================
st.subheader("👨‍💼 Experience Required")

experience_count = DS_jobs_df["experience"].value_counts()[:7]

fig3, ax3 = plt.subplots()
experience_count.plot.barh(color=colors, ax=ax3)
plt.xlabel("No. of Vacancies", weight='bold')
plt.ylabel("Experience", weight='bold')
plt.title("Required Experience Levels", weight='bold')
st.pyplot(fig3)
