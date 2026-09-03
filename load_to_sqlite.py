import pandas as pd
import sqlite3
import os

df = pd.read_csv('data/cleaned_weather.csv')

conn = sqlite3.connect('weather_final.db')

df.to_sql('weather_final', conn, if_exists='replace', index=False)