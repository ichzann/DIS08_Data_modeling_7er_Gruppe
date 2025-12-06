import pandas as pd
import os

file_path = os.path.dirname(__file__)
jan_path = os.path.join(file_path, "..")
scripte_path = os.path.join(jan_path, "..")
main_path = os.path.join(scripte_path, "..")
daten_sets_path = os.path.join(main_path, "Daten_sets/EUDA_Wastewater_analysis_and_drugs/ww2025_deutschland.csv")

print("")
df = pd.read_csv(daten_sets_path)


max_drugs_index = df.idxmax()
max_drugs = df.loc[max_drugs_index]
print(max_drugs)