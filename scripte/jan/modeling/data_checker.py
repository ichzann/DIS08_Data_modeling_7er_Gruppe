# data_checker.py
'''
Script zum Analysieren der Datenqualität von Dateien.
Funktion:

'''
from ctypes.macholib.dyld import dyld_find
from fileinput import filename
import os
import pandas as pd

# Variablen und Konstanten
LINE = "_"*100
LINE2 = "="*100

# relativer Pfad vom Script zu den Datenordnern
script_dir = os.path.dirname(os.path.abspath(__file__))
data_sets_folder_path = os.path.join(script_dir, "../../../Daten_sets")
euda_sets_path = os.path.join(data_sets_folder_path, "EUDA_Wastewater_analysis_and_drugs")

# Datei als DataFrame einlesen
file_name = "ww2025_deutschland.csv" 
df = pd.read_csv(os.path.join(euda_sets_path, file_name))

    
def data_checker():
    print(f"{LINE2}\n# Starte Datenchecker ...\n{LINE2}\n")

    # decrib
    print("1. Kurzbeschreibung der Daten:\n" + LINE ,"\n", df.describe())
    # Fehlende Werte
    df_null_value_sum = df.isnull().sum().to_dict()
    print(f"\n2. Anzahl fehlender Werte pro Spalte: {sum(df_null_value_sum.values())}\n"+ LINE)

    print(df.isnull().sum())
    rows_with_nulls = df[df.isnull().any(axis=1)]
    print(rows_with_nulls["City"].unique())
    print(df["Year"].unique())
    # Erste Zeilen (visuelle Kontrolle)
    print("\nErste Zeilen:")
    print(df.head())

data_checker()