import pandas as pd
import os

file_path = os.path.dirname(__file__)
jan_path = os.path.join(file_path, "..")
scripte_path = os.path.join(jan_path, "..")
main_path = os.path.join(scripte_path, "..")
daten_sets_path = os.path.join(main_path, "Daten_sets/blaulicht_scraping")

staedte_liste = []
for filename in os.listdir(daten_sets_path):
    print(filename)
    if filename.startswith("."):
        continue
    df = pd.read_csv(os.path.join(daten_sets_path, filename), encoding="utf_8")

    df["datum"] = pd.to_datetime(df["datum"], format="%d.%m.%Y – %H:%M", errors='coerce')
    stadt_info = {
            "filename": filename,
            "stadt": df["stadt"].iloc[0] if not df.empty else "Unbekannt",
            "von": df["datum"].min(),
            "bis": df["datum"].max(),
            "anzahl_posts": len(df)
        }
        
        # 3. Dictionary der Liste hinzufügen
    staedte_liste.append(stadt_info)


df_final = pd.DataFrame(staedte_liste)
df_final.to_json(os.path.join(daten_sets_path,"staedte_statistik.json"), orient="records",force_ascii=False, indent=4, date_format="iso")
print(staedte_liste)


