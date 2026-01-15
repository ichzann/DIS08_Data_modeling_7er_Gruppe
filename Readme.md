# Ø mg daily mean all drugs per country 
<img src="https://github.com/ichzann/DIS08_Data_modeling_7er_Gruppe/blob/main/Daten_sets/EUDA_Wastewater_analysis_and_drugs/filtered_by_drug/ranking%20videos/ranking_all_drugs.gif?raw=true" width="600" />


## 👮 Datenquelle: Polizeimeldungen (Presseportal Blaulicht)

Um die quantitativen Abwasserdaten (insb. den Kokain/Crack-Anstieg in Dortmund 2022) zu kontextualisieren, wurden Polizeimeldungen der Dienststelle Dortmund über [Presseportal.de](https://www.presseportal.de/blaulicht/r/Dortmund/0) gescrapt.

### 🎯 Warum diese Datenquelle?
Während Abwasserdaten reine Verbrauchsmengen anzeigen, liefern die Polizeiberichte den **sozialen und kriminologischen Kontext** auf Straßenebene. Die Verbindung beider Datensätze ermöglicht die Untersuchung folgender Hypothesen:

1.  **Sichtbarkeit vs. Konsum:** Korreliert die gemessene Stoffmenge im Wasser mit der Anzahl der BTM-Delikte (Betäubungsmittel)?
2.  **Beschaffungskriminalität:** Da insbesondere der Anstieg von Crack im Ruhrgebiet mit einer Verelendung der Szene einhergeht, lässt sich prüfen, ob parallel zu den Abwasserwerten auch Eigentumsdelikte (Diebstahl, Raub, PKW-Aufbrüche) in den Berichten zunehmen.
3.  **Hotspot-Identifikation:** Die Texte enthalten oft genaue Ortsangaben (z.B. "Innenstadt", "Nordstadt"), wodurch sich der Konsum räumlich verorten lässt, was Abwasserdaten allein oft nicht leisten können.

### 🔍 Extrahierte Datenpunkte
Das Scraping-Skript extrahiert für jeden Artikel:
* **Datum & Uhrzeit:** Für zeitliche Reihenanalysen (Time-Series).
* **Titel & Text:** Für NLP-Analysen (Keyword-Extraction nach Begriffen wie "BTM", "Drogen", "auffälliges Verhalten", "Widerstand").
* **Dienststelle:** Um sicherzustellen, dass die Berichte dem gleichen Einzugsgebiet wie dem Klärwerk zugeordnet werden können.


## kanban 🚧 Projektstatus

Den aktuellen Entwicklungsstand und geplante Features findest du auf meinem Trello-Board:

[![Trello Board](assets/trello.png)]
[![Trello](https://img.shields.io/badge/Trello-Projekt%20Board-blue?style=for-the-badge&logo=trello)](https://trello.com/b/tz49lLdt/mein-trello-board)