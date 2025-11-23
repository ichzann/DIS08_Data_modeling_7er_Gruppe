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
datenverfügbarkeit_tabelle = pd.crosstab(
    index=df['Year'], 
    columns=df['Metabolite'],
    dropna=True
)
print(datenverfügbarkeit_tabelle)
print(df["Metabolite"].value_counts())
print(df.head(3))
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def check_data_quality(df):
    print("--- 1. BASIS-INFO & DATENTYPEN ---")
    print(df.info())
    print("\n")

    # --- 2. FEHLENDE WERTE (NANS) ---
    print("--- 2. ANALYSE FEHLENDER WERTE ---")
    missing = df.isnull().sum()
    missing = missing[missing > 0] # Nur Spalten mit Fehlern zeigen
    if not missing.empty:
        print(missing)
        # Visualisierung der fehlenden Werte (Heatmap)
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap="viridis")
        plt.title("Karte der fehlenden Werte (Gelb = Fehlend)")
        plt.show()
    else:
        print("Perfekt! Keine fehlenden Werte (NaNs) gefunden.")
    print("\n")

    # --- 3. DUPLIKATE ---
    # Einzigartigkeit prüfen: Es sollte pro Stadt, Jahr und Metabolit nur EINE Zeile geben
    print("--- 3. DUPLIKAT-CHECK ---")
    duplicates = df[df.duplicated(subset=['City', 'Year', 'Metabolite'], keep=False)]
    if not duplicates.empty:
        print(f"ACHTUNG: {len(duplicates)} Duplikate gefunden!")
        print(duplicates[['City', 'Year', 'Metabolite']].head())
    else:
        print("Konsistenz OK: Keine Duplikate für Stadt/Jahr/Metabolit-Kombinationen.")
    print("\n")

    # --- 4. LOGISCHE PLAUSIBILITÄT ---
    print("--- 4. LOGIK-CHECK (Negativ-Werte) ---")
    # Konzentrationen können physikalisch nicht negativ sein
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    negative_values = (df[numeric_cols] < 0).sum().sum()
    
    if negative_values > 0:
        print(f"ALARM: {negative_values} negative Werte gefunden! Das ist physikalisch unmöglich.")
    else:
        print("Plausibilität OK: Keine negativen Konzentrationen.")
    print("\n")

    # --- 5. AUSREISSER (STATISTISCH) ---
    print("--- 5. AUSREISSER-ANALYSE (Top 5 Extremwerte pro Metabolit) ---")
    # Wir schauen uns die "Daily mean" Spalte an
    
    # Boxplot für visuelle Prüfung
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x="Daily mean", y="Metabolite", palette="Set2")
    plt.title("Verteilung & Ausreißer (Boxplot)")
    plt.xlabel("Daily mean Konzentration")
    plt.xscale('log') # Logarithmische Skala, da Drogenwerte oft exponentiell verteilt sind
    plt.show()

    # Z-Score Methode (einfach): Werte die extrem weit vom Durchschnitt abweichen
    # Wir zeigen hier einfach die absoluten Top-Werte an
    for metabolit in df['Metabolite'].unique():
        df_sub = df[df['Metabolite'] == metabolit]
        top_5 = df_sub.nlargest(5, 'Daily mean')[['Year', 'City', 'Daily mean']]
        print(f"-> Top 5 höchste Werte für {metabolit}:")
        print(top_5)
        print("-" * 30)

# --- AUSFÜHRUNG ---
# (Angenommen df ist dein gefiltertes 'df_deutschland')
check_data_quality(df)
import matplotlib.pyplot as plt
import seaborn as sns

def plot_meth_hotspots(dataframe):
    # 1. Wir isolieren nur die Methamphetamin-Daten
    df_meth = dataframe[dataframe['Metabolite'] == 'methamphetamine']
    
    # 2. Sortier-Logik erstellen
    # Wir berechnen den Median für jede Stadt und sortieren absteigend.
    # Das sorgt dafür, dass die "schlimmsten" Städte ganz links stehen.
    my_order = df_meth.groupby("City")["Daily mean"].median().sort_values(ascending=False).index
    
    # 3. Plotten
    plt.figure(figsize=(14, 7))
    
    sns.boxplot(
        data=df_meth, 
        x="City", 
        y="Daily mean", 
        order=my_order,    # Hier wenden wir die Sortierung an
        palette="magma"    # "magma" wirkt bedrohlicher/intensiver für Hotspots
    )
    
    # Visuelles Tuning
    plt.title('Wer treibt den Durchschnitt hoch? Methamphetamin-Belastung nach Städten', fontsize=18, weight='bold')
    plt.ylabel('Mittlere Tagesdosis (mg/1000p/Tag)', fontsize=14)
    plt.xlabel('Stadt', fontsize=14)
    plt.xticks(rotation=45)  # Schräge Beschriftung, damit man lange Städtenamen lesen kann
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Optional: Eine Linie für den deutschlandweiten Median einzeichnen
    german_median = df_meth['Daily mean'].median()
    plt.axhline(german_median, color='blue', linestyle='--', label=f'Deutschlandweiter Median ({german_median:.1f})')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

# --- Ausführen ---
# (Wir nutzen wieder deinen bereinigten DataFrame)
plot_meth_hotspots(df)