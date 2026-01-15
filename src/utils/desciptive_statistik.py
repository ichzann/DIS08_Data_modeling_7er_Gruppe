import pandas as pd

df = pd.read_csv('Data/processed/wasser_cleaning/alle_staedte.csv', sep=';')

print(df.describe())