import os
import pandas as pd

# relativer Pfad vom Script zu den Datenordnern
script_dir = os.path.dirname(os.path.abspath(__file__))
data_sets_folder_path = os.path.join(script_dir, "../../../Daten_sets")
euda_sets_path = os.path.join(data_sets_folder_path, "EUDA_Wastewater_analysis_and_drugs")


file_name = "ww2025-all-data.csv" 
df = pd.read_csv(os.path.join(euda_sets_path, "ww2025-all-data.csv"))


df_c = df[df["Metabolite"] == "cocaine"]
df_c = df_c[["Year", "City", "Daily mean"]]


df_transformed = df_c.pivot_table(index='Year', columns='City', values='Daily mean', aggfunc='mean')

df_transformed = df_transformed.reset_index()

df_transformed.columns.name = None

print(df_transformed.head())
print(df_transformed.head(3))

df_transformed.to_csv(os.path.join(euda_sets_path, "ww2025_cocaine_pivoted.csv"), index=False)