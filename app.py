import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load data
df = pd.read_csv("metadata.csv", nrows=10000)
# Save as a smaller CSV
df.to_csv("sample_metadata.csv", index=False)


df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year
df['journal'] = df['journal'].fillna("Unknown")

st.title("CORD-19 Data Explorer")
st.write("Explore COVID-19 research publications")

# Filter by year
years = df['year'].dropna().astype(int)
year_range = st.slider("Select year range", int(years.min()), int(years.max()), (2020, 2021))
filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Show sample data
st.subheader("Sample Data")
st.write(filtered.head())

# Publications over time
st.subheader("Publications by Year")
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values)
st.pyplot(fig)

# Top Journals
st.subheader("Top Journals")
top_journals = filtered['journal'].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(x=top_journals.values, y=top_journals.index, ax=ax)
st.pyplot(fig)

# Word Cloud
st.subheader("Word Cloud of Titles")
words = " ".join(filtered['title'].dropna())
wc = WordCloud(width=800, height=400, background_color="white").generate(words)
fig, ax = plt.subplots()
ax.imshow(wc, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)
