[EUDA_Wastewater_analysis_and_drugs](https://www.euda.europa.eu/publications/html/pods/waste-water-analysis_en)

# 📊 Beschreibung der EUDA-Abwasseranalyse-Datensätze (2024/2025)

Diese vier Dateien enthalten die Ergebnisse der europäischen Abwasseranalyse auf Drogen und deren Metaboliten, die vom **Europäischen Zentrum für die Beobachtung von Drogen und Drogensucht (EUDA)** veröffentlicht wurden (Datenstand 2024, Bericht 2025).

---

## 1. `ww2025-site-info-table.csv`

**Titel:** Standortinformationen
**Zweck:** Enthält Metadaten zu allen Probenahmestellen (Kläranlagen).

| Spalte | Beschreibung | Beispielwerte |
| :--- | :--- | :--- |
| **SiteID** | Eindeutige Kennung der Kläranlage. | `AT001`, `NL010` |
| **Country, City** | Land und Stadt des Standortes. | `AT`, `Graz` |
| **Location** | Name der Kläranlage/des Standorts. | `ARA Graz` |
| **Latitude, Longitude** | Geografische Koordinaten der Anlage. | `47.0707`, `15.4395` |
| **Population** | Geschätzte Bevölkerungszahl, die an die Kläranlage angeschlossen ist. | `425000` |
| **Institution** | Name der durchführenden Forschungseinrichtung. | `Medical University Innsbruck` |

---

## 2. `ww2025-aggregated-trends.csv`

**Titel:** Aggregierte Langzeit-Trends
**Zweck:** Zeigt die über alle teilnehmenden Standorte gemittelten jährlichen Konzentrationswerte der Hauptmetaboliten.

| Spalte | Beschreibung | Einheit |
| :--- | :--- | :--- |
| **metabolite** | Name des analysierten Drogenmetaboliten oder der Substanz. | N/A |
| **2011 bis 2024** | Die über alle Standorte gemittelte tägliche Menge (Mass-load) der Substanz in den jeweiligen Jahren. | mg/1000 Personen/Tag |
| **Fokus:** | Langfristige zeitliche Entwicklung des Konsums. | |

---

## 3. `ww2025-all-data.csv`

**Titel:** Detaillierte Tagesdaten nach Standort
**Zweck:** Liefert die täglichen Konzentrationswerte sowie aggregierte Mittelwerte für jeden Standort und jedes Jahr.

| Spalte | Beschreibung | Einheit |
| :--- | :--- | :--- |
| **Year, Metabolite, Site ID, Country, City** | Identifikationsmerkmale des Messwertes. | N/A |
| **Wednesday bis Tuesday** | Die täglich gemessene Mass-load der Substanz für den jeweiligen Wochentag. | mg/1000 Personen/Tag |
| **Weekday mean** | Durchschnitt der Messwerte von Montag bis Donnerstag (Mo-Do). | mg/1000 Personen/Tag |
| **Weekend mean** | Durchschnitt der Messwerte von Freitag bis Sonntag (Fr-So). | mg/1000 Personen/Tag |
| **Daily mean** | Gesamtdurchschnitt aller gemessenen Tage. | mg/1000 Personen/Tag |
| **Fokus:** | Detaillierte Analyse wochentäglicher Konsummuster und standortspezifischer Werte. | |

---

## 4. `ww2025-changes-all-substances.csv`

**Titel:** Jährliche Konsumveränderungen (2023 vs. 2024)
**Zweck:** Vergleicht die durchschnittlichen Konsumwerte des aktuellen Jahres (2024) mit dem Vorjahr (2023) und kategorisiert die prozentuale Veränderung.

| Spalte | Beschreibung | Einheit |
| :--- | :--- | :--- |
| **country, city, metabolite** | Identifikationsmerkmale. | N/A |
| **value_current** | Durchschnittlicher Wert des aktuellen Messjahres (**2024**). | mg/1000 P./Tag |
| **value_previous** | Durchschnittlicher Wert des Vorjahres (**2023**). | mg/1000 P./Tag |
| **change_percent** | Die prozentuale Veränderung ( $\frac{\text{Aktuell} - \text{Vorjahr}}{\text{Vorjahr}} \times 100$). | % |
| **change_percent2** | Kategorisierung der Veränderung (z.B. `increase`, `decrease`, `stable`). | N/A |
| **SiteID** etc. | Zusätzliche Standortinformationen (aus `ww2025-site-info-table.csv`). | N/A |
| **Fokus:** | Analyse der Dynamik und der signifikantesten Zunahmen/Abnahmen im letzten Berichtszeitraum. | |