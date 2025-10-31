import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

st.title("📊 Netflix Insights")
url = "https://raw.githubusercontent.com/manasacharyagit/Netflix-analysis/refs/heads/master/mymoviedb.csv"
df = pd.read_csv(url, lineterminator='\n')

# Preparing data genre-based
dfg = df.copy()
dfg['Genre'] = dfg['Genre'].str.split(', ')
dfg = dfg.explode('Genre').reset_index(drop=True)

#1. 
st.subheader("🎭 Number of Movies by Genre")

genre_counts = dfg['Genre'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Count']
plt.figure(figsize=(8,4))

sns.barplot(data=genre_counts, x='Count', y = 'Genre', palette = 'rocket')
plt.title("Top 10 Genres on Netflix")
plt.xlabel("Number of Movies")
plt.ylabel("Genre")

st.pyplot(plt)

#2.
st.subheader("⭐ 5 Most Popular Movies")

top5 = dfg.drop_duplicates(subset="Title").nlargest(5, "Popularity")
plt.figure(figsize=(8,4))

sns.barplot(data=top5, y='Popularity', x='Title', palette='flare')
plt.xlabel("Movies")
plt.ylabel("Popularity")
plt.title("Top 5 Most Popular Movies on Netflix")
plt.xticks(rotation=45)

st.pyplot(plt)

#3. Years with Most Movie Releases
st.subheader("📅 Years with Most Movie Releases")

df['Release_Date'] = pd.to_datetime(df['Release_Date'])
df['Release_year'] = df['Release_Date'].dt.year
year_count = df['Release_year'].value_counts().reset_index().head(10)
year_count.columns = ['Year', 'Count']

plt.figure(figsize=(8,5))
sns.barplot(data = year_count, x = 'Year', y = 'Count')
plt.xlabel("Years")
plt.ylabel("Number of Movies Released")
plt.title("Top 5 Most Popular Movies on Netflix")
plt.xticks(rotation=90)

st.pyplot(plt)


#4 Movie release trend over the years
st.subheader("📈 Movie Release Trend Over the Years")

year_trend = df['Release_year'].value_counts().reset_index()
year_trend.columns = ['Year', 'Count']
plt.figure(figsize=(8,5))

sns.lineplot(data = year_trend, x='Year', y = 'Count', marker='o')

plt.xlabel("Years")
plt.ylabel("Number of Movies Released")
plt.title("Movie Release Trend Over the Years")
plt.xticks(rotation=90)
st.pyplot(plt)


