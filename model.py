import string
import joblib

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


df = pd.read_csv("train_data.csv", sep=",")
train_df, test_df = train_test_split(df, test_size=5)

nltk.download("stopwords")
nltk.download('punkt_tab')
snowball = SnowballStemmer(language="english")
stop_words = stopwords.words("english")

def tokinize_sentese(sentense: str):
    tokens = word_tokenize(sentense, language="english")
    tokens = [i for i in tokens if i not in string.punctuation]
    tokens = [i for i in tokens if i not in stop_words]
    tokens = [snowball.stem(i) for i in tokens]
    return tokens

model_pipeline = Pipeline([
    ("vectorizer", TfidfVectorizer(tokenizer=tokinize_sentese)),
    ("model", LogisticRegression(random_state=0))
])
model_pipeline.fit(train_df["task_description"], train_df["priority"])

joblib.dump(model_pipeline, "./model.joblib")
