import pandas as pd

df = pd.read_csv('Data/raw/EUDA_Wasserwerk2016-24/Wasserwerk2016-2024.csv')

print(df["Daily mean"].describe())