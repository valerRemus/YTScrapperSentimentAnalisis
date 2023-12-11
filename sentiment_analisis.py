import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import math

import pandas as pd

df = pd.read_csv('comments.csv')

def sentiment_detection(df):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    analizador = SentimentIntensityAnalyzer()

    df['Categoria'] = ''
    df['Compound'] = 0.0

    for index, sentence in enumerate(df['Frases'].dropna()):
        if pd.isna(sentence):
            continue

        scores = analizador.polarity_scores(str(sentence))
        df.loc[index, 'Compound'] = scores['compound']

        if max(scores, key=scores.get) == 'neu':
            df.loc[index, 'Categoria'] = 'Neutral'
        elif max(scores, key=scores.get) == 'pos':
            df.loc[index, 'Categoria'] = 'Positive'
        elif math.isnan(scores['compound']):
            continue
        else:
            df.loc[index, 'Categoria'] = 'Negative'

    return df

# Calcular la media general de los sentimientos

import matplotlib.pyplot as plt

def grafico(df):
    # Create a bar chart with the exact number of sentences on the y-axis
    plt.figure(figsize=(10, 6))
    ax = df['Categoria'].value_counts().sort_index().plot(kind='bar', color=['blue', 'green', 'red'])

    # Display the exact number of sentences on the y-axis
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    plt.title('Sentiment Analysis')
    plt.xlabel('Category')
    plt.ylabel('Number of comments')
    plt.legend()
    plt.show()

# Example usage:
# grafico(your_dataframe)



sentiment_detection(df)
df.to_csv('sentiments.csv', index=False)
print(df)
grafico(df)