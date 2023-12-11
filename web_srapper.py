import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from googletrans import Translator

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt



class yt_sentiment_analisis():
    def __init__(self):
        self.translator = Translator()

    def scrapper(self, url):
        chrome_path = r'C:\Users\r3mus\Downloads\chromedriver-win64\chromedriver-win64.exe'
        service = Service(executable_path=chrome_path)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome()

        # Abre la URL de YouTube
        driver.get(url)

        # Espera a que la página cargue completamente
        wait = WebDriverWait(driver, 15)

        for _ in range(20):
             #Desplázate hacia abajo para cargar más comentarios
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body'))).send_keys(Keys.END)
            time.sleep(5)  # Espera 5 segundos para cargar los comentarios

        # Espera a que se carguen todos los comentarios
        comments = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#content #content-text')))
        data = [comment.text for comment in comments]

        # Crea un DataFrame con los comentarios
        df = pd.DataFrame(data, columns=['Frases'])
        df.dropna()
        df.to_csv('comments.csv', index=False)
        driver.quit()


    def traductor(self, csv):
        df = pd.read_csv(csv)
        for index, row in df.iterrows():
            translated_text = self.translator.translate(row['Frases'], dest='en').text
            df.at[index, 'Frases'] = translated_text

        df.to_csv('translated.csv', index=False)

    def sentiment_detection(self, csv):

        df = pd.read_csv("translated.csv")
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        analizador = SentimentIntensityAnalyzer()

        df['Categoria'] = ''
        df['Compound'] = 0.0

        for index, sentence in enumerate(df['Frases'].dropna()):
            if pd.isna(sentence):
                continue

            scores = analizador.polarity_scores(str(sentence))
            df.loc[index, 'Compound'] = scores['compound']

            if scores['compound'] >= -0.800 and scores['compound'] <= 0.300:
                df.loc[index, 'Categoria'] = 'Neutral'
            elif scores['compound'] >= 0.300:
                df.loc[index, 'Categoria'] = 'Positive'
            else:
                df.loc[index, 'Categoria'] = 'Negative'

        df.to_csv("sentiments.csv", index=False)


    def grafico(self, df):
        df = pd.read_csv("sentiments.csv")
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
        return plt.show()



#scrapper('https://www.youtube.com/watch?v=yAO1rxNVJ4g')