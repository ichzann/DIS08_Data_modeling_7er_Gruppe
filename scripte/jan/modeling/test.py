import os
import pandas as pd

# relativer Pfad vom Script zu den Datenordnern
script_dir = os.path.dirname(os.path.abspath(__file__))
data_sets_folder_path = os.path.join(script_dir, "../../../Daten_sets")
euda_sets_path = os.path.join(data_sets_folder_path, "EUDA_Wastewater_analysis_and_drugs")
filtered_by_drug_data_sets = os.path.join(euda_sets_path, "filtered_by_drug")


file_name = "ww2025-all-data.csv" 
df = pd.read_csv(os.path.join(euda_sets_path, "ww2025-all-data.csv"))


def nach_droge_segmentieren(df, drogenname: str):
    df_droge = df[df["Metabolite"] == drogenname]

    df_c = df_droge[["Year", "City", "Daily mean"]]


    df_transformed = df_c.pivot_table(index='Year', columns='City', values='Daily mean', aggfunc='mean')

    df_transformed = df_transformed.reset_index()

    df_transformed.columns.name = None

    df_transformed.to_csv(os.path.join(filtered_by_drug_data_sets, f"ww2025_{drogenname}_pivoted.csv"), index=False)
    print("Gespeichert:", f"ww2025_{drogenname}_pivoted.csv")

drugs = df["Metabolite"].unique().tolist()

"""
for droge in drugs:
    nach_droge_segmentieren(df, droge)
"""

def speichere_durchschnitt_aller_drogen(df):
    df_avg = df.pivot_table(index='Year', columns='City', values='Daily mean', aggfunc='mean')

    df_avg = df_avg.reset_index()
    df_avg.columns.name = None
    print(df_avg.head(3))

    dateiname = "ww2025_average_all_drugs_pivoted.csv"
    df_avg.to_csv(os.path.join(filtered_by_drug_data_sets, dateiname), index=False)
    print("Gespeichert:", dateiname)

speichere_durchschnitt_aller_drogen(df)