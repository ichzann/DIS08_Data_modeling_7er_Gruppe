import matplotlib
import pandas as pd
import os

# relativer Pfad vom Script zu den Datenordnern
script_dir = os.path.dirname(os.path.abspath(__file__))
data_sets_folder_path = os.path.join(script_dir, "../../../Daten_sets")
euda_sets_path = os.path.join(data_sets_folder_path, "EUDA_Wastewater_analysis_and_drugs")

def deutsche_daten(save_as_csv: bool = False):
    file_name = "ww2025-all-data.csv" 
    df = pd.read_csv(os.path.join(euda_sets_path, "ww2025-all-data.csv"))

    städte = ['Chemnitz', 'Dortmund', 'Dülmen', 'Erfurt', 'Munich G', 'Nuremberg', 'Saarbrücken (2)', 'Hamburg N', 'Stuttgart']

    df_deutschland = pd.DataFrame()

    filt = df["City"].isin(städte)
    df_deutschland = df[filt]
    if save_as_csv:
        df_deutschland.to_csv(os.path.join(euda_sets_path, "ww2025_deutschland.csv"))
    return df_deutschland

df = pd.read_csv(os.path.join(euda_sets_path, "ww2025_deutschland.csv"))

datenverfügbarkeit_tabelle = pd.crosstab(
    index=df['City'], 
    columns=df['Year'],
    dropna=True
)
print(datenverfügbarkeit_tabelle)