import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import ast
import numpy as np

# Load the CSV file
df = pd.read_csv('10_pages_movies.csv')

# Replace NaN values with empty strings
df['genres'] = df['genres'].fillna('')
df['themes'] = df['themes'].fillna('')

# Parse genres and themes into lists
df['genres'] = df['genres'].apply(lambda x: x.split(',') if x else [])
df['themes'] = df['themes'].apply(lambda x: x.split(',') if x else [])

# Parse histogram into a list of ratings
df['histogram'] = df['histogram'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])

# Add a decade column
df['decade'] = (df['year'] // 10) * 10

# Expand histogram data into individual ratings
def expand_histogram(histogram):
    ratings = []
    for rating, count in enumerate(histogram, start=1):
        ratings.extend([rating] * count)
    return ratings

# Add expanded ratings as a new column
df['expanded_ratings'] = df['histogram'].apply(expand_histogram)

# Create a new DataFrame with individual ratings and genres
df_exploded_genres = df.explode('genres')[['genres', 'histogram']]
df_exploded_directors = df.explode('director')[['director', 'histogram']]
df_exploded_decade = df[['decade', 'histogram']]

# Function to calculate average histogram
def calculate_average_histogram(df_grouped):
    histogram_sum = df_grouped['histogram'].apply(lambda x: np.sum(np.array(x.tolist()), axis=0))
    histogram_count = df_grouped['histogram'].count()
    return histogram_sum / histogram_count

# Sidebar options
st.sidebar.title("Movie Data Analysis")
option = st.sidebar.selectbox(
    'Select Analysis Type',
    ['Genre Distribution', 'Theme Analysis', 'Director Analysis', 'Yearly Trends', 'Average Histogram by']
)

# Function to extract unique values and their counts
def get_value_counts(column):
    all_values = df[column].explode()
    return all_values.value_counts()

# Function to plot bar chart
def plot_bar_chart(data, title, xlabel, ylabel):
    fig, ax = plt.subplots()
    data.plot(kind='bar', ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)

# Genre Distribution
if option == 'Genre Distribution':
    st.header("Genre Distribution")
    genre_counts = get_value_counts('genres')
    plot_bar_chart(genre_counts, "Genre Distribution", "Genres", "Counts")

# Theme Analysis
elif option == 'Theme Analysis':
    st.header("Theme Analysis")
    theme_counts = get_value_counts('themes')
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(theme_counts)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# Director Analysis
elif option == 'Director Analysis':
    st.header("Top 10 Directors")
    director_counts = df['director'].value_counts().head(10)
    plot_bar_chart(director_counts, "Top 10 Directors", "Directors", "Counts")

# Yearly Trends
elif option == 'Yearly Trends':
    st.header("Yearly Trends")
    year_counts = df['year'].value_counts().sort_index()
    fig, ax = plt.subplots()
    year_counts.plot(kind='line', ax=ax)
    ax.set_title("Yearly Trends")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Movies")
    st.pyplot(fig)

# Average Histogram by selected group
elif option == 'Average Histogram by':
    st.sidebar.subheader("Group Average Histogram by")
    group_by_options = st.sidebar.radio(
        '',
        ['Genres', 'Decades', 'Directors (Top 10)']
    )

    st.header("Average Histogram by Group")
    
    if group_by_options == 'Genres':
        grouped_df = df.explode('genres').groupby('genres')
    elif group_by_options == 'Decades':
        grouped_df = df.groupby('decade')
    elif group_by_options == 'Directors (Top 10)':
        top_10_directors = df['director'].value_counts().head(10).index
        grouped_df = df[df['director'].isin(top_10_directors)].groupby('director')

    average_histogram_by_group = calculate_average_histogram(grouped_df)
    average_histogram_by_group = average_histogram_by_group.apply(pd.Series)

    num_plots = len(average_histogram_by_group)
    num_cols = 4
    num_rows = (num_plots + num_cols - 1) // num_cols

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(16, num_rows * 4))
    if num_rows == 1:
        axs = [axs]
    for i, (group, hist) in enumerate(average_histogram_by_group.iterrows()):
        row = i // num_cols
        col = i % num_cols
        axs[row][col].bar(range(1, 11), hist)
        axs[row][col].set_title(f"{group}")
        axs[row][col].set_xlabel("Rating")
        axs[row][col].set_ylabel("Average Count")

    # Hide any unused subplots
    for i in range(num_plots, num_rows * num_cols):
        row = i // num_cols
        col = i % num_cols
        axs[row][col].axis('off')

    plt.tight_layout()
    st.pyplot(fig)
