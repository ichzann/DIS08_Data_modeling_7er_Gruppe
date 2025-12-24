import pandas as pd
import os

file_path = os.path.dirname(__file__)
jan_path = os.path.join(file_path, "..")
scripte_path = os.path.join(jan_path, "..")
main_path = os.path.join(scripte_path, "..")
daten_sets_path = os.path.join(main_path, "Daten_sets/blaulicht_scraping")

suchwörter = ["Drogen", "Cannabis", "Kokain"]
such_pattern = '|'.join(suchwörter)

for filename in os.listdir(daten_sets_path):
    print(filename)
    if filename.startswith(".") or not filename.endswith(".csv"):
        continue

    df = pd.read_csv(os.path.join(daten_sets_path, filename), encoding="utf_8")

    artikel = df[df["title"].str.contains(such_pattern, case=False, na=False)]

    
    artikel = artikel.groupby(["jahr", "stadt", "gefundenes_wort"]).size().reset_index(name="anzahl")
    print(artikel)