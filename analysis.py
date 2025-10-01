import pandas as pd

# LOADING & EXPLORING THE DATASET
# Load the dataset
df = pd.read_csv("metadata.csv")

# Explore structure
print(df.shape)
print(df.info())
print(df.head())

# CLEANING THE DATA
# Missing values
print(df.isnull().sum())

# Drop papers without title or publish_time
df = df.dropna(subset=['title', 'publish_time'])

# Fill NaN journal names with "Unknown"
df['journal'] = df['journal'].fillna("Unknown")

# convert dates and extract year
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year

# add abstract word count
df['abstract_word_count'] = df['abstract'].fillna("").apply(lambda x: len(x.split()))

# BASIC ANALYSIS
# Publications by Year
year_counts = df['year'].value_counts().sort_index()

# top journals
top_journals = df['journal'].value_counts().head(10)

# word frequency in titles
from collections import Counter
import re

words = " ".join(df['title'].dropna()).lower()
words = re.findall(r'\b[a-z]{3,}\b', words)  # min 3 letters
common_words = Counter(words).most_common(20)

# VISUALIZATIONS

import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Publications over time
df['year'].value_counts().sort_index().plot(kind="bar")
plt.title("Publications by Year")
plt.show()

# Top journals
sns.barplot(x=top_journals.values, y=top_journals.index)
plt.title("Top Journals")
plt.show()

# Word Cloud
wc = WordCloud(width=800, height=400, background_color="white").generate(" ".join(words))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()
