import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Use Streamlit's native backend for rendering matplotlib charts
def show_pie_chart(data, title, colors=None):
    """
    Draw a donut-style pie chart.
    """
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        data.values,
        labels=data.index,
        autopct='%1.1f%%',
        startangle=30,
        wedgeprops=dict(width=0.3, edgecolor='w'),
        colors=colors
    )

    # Donut center
    centre_circle = plt.Circle((0, 0), 0.60, fc='white')
    fig.gca().add_artist(centre_circle)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    ax.set_title(title)
    st.pyplot(fig)


def show_bar_chart(data, title, xlabel, ylabel, orientation='v', color='skyblue'):
    """
    Render a vertical or horizontal bar chart.
    """
    fig, ax = plt.subplots()
    if orientation == 'v':
        sns.barplot(x=data.index, y=data.values, ax=ax, color=color)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    else:
        sns.barplot(y=data.index, x=data.values, ax=ax, color=color)
        ax.set_ylabel(xlabel)
        ax.set_xlabel(ylabel)
    ax.set_title(title)
    st.pyplot(fig)
