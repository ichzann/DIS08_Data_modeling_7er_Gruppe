# 🧪 Analyse der Korrelation zwischen Abwasser-Drogenrückständen und Polizeiberichten

Dieses Repository enthält die Forschungsarbeit der **Gruppe 4**, die sich mit der statistischen Beziehung zwischen chemisch nachgewiesenem Drogenkonsum und der öffentlichen Berichterstattung über drogenspezifische Delikte auseinandersetzt.

## 📝 Projektbeschreibung
Das Ziel dieses Projekts ist es, zu untersuchen, ob eine messbare **Korrelation zwischen den eingenommenen Drogen** (basierend auf Abwasseranalysedaten der EUDA, ehemals EMCDDA) und der **Anzahl der polizeilichen Meldungen** in den jeweiligen Städten besteht. Dabei werden objektive Messwerte aus Wasserwerken den quantitativen Daten aus dem "Blaulichtreport" gegenübergestellt.

## 🛠 Methodik & Features

Das Projekt umfasst den gesamten Data-Science-Zyklus von der Akquise bis zur Analyse:

*   **Scraping & Datenerhebung:** 
    *   Ursprünglich war ein Scraping verschiedener lokaler Nachrichtensender geplant. Um die Skalierbarkeit zu erhöhen und die Wartbarkeit des Codes zu optimieren, wurde der Fokus auf den **zentralen Blaulichtreport** verschoben. 
    *   Dies ermöglichte die Entwicklung eines spezialisierten Scrapers, der effizient Daten für mehrere Städte aggregiert, ohne für jede Quelle eine individuelle Architektur zu benötigen.
*   **Data Cleaning & Vorbereitung:**
    *   Die extrahierten Rohdaten wurden bereinigt und in einem konsolidierten Datensatz zusammengeführt.
    *   Ziel war die Erstellung einer einheitlichen Datenbasis, die alle für die Fragestellung relevanten Variablen (Stadt, Jahr, Drogentyp, Berichthäufigkeit) enthält.
*   **Information Retrieval (IR):**
    *   Implementierung von IR-Techniken, um die relative Dichte relevanter Artikel pro Stadt und Jahr präzise zu erfassen.
    *   Dieser Prozess dient der Quantifizierung der öffentlichen Wahrnehmung bzw. der polizeilichen Dokumentation von Drogendelikten.
*   **Statistische Auswertung:**
    *   Untersuchung der Korrelationen zwischen den Milligramm-Werten pro Tag (daily mean) aus dem Abwasser und der Trefferquote im Information Retrieval.

## 💻 Tech Stack

Das Projekt ist primär in **Python** umgesetzt, wobei ein Großteil der Analysen in interaktiven Umgebungen stattfindet:

*   **Sprachen:** Python, Jupyter Notebook.
*   **Bibliotheken:** (Annahme basierend auf Industriestandards) Pandas für Data Cleaning, BeautifulSoup/Scrapy für Web Scraping, Matplotlib/Seaborn für statistische Auswertungen.
*   **Repository-Struktur:**
    *   `/Daten_sets`: Bereinigte und rohe Datenquellen.
    *   `/scripte`: Python-Skripte für Scraping und Processing .
    *   `/statistik`: Analysen und Visualisierungen der Korrelationen.
    *   `/Retrieval (IR)`: Komponenten zur Artikelerfassung und -gewichtung .

## Projekt Dokumentation
[Roadmap](Roadmap.md)  
[Projekt Report](ProjectReport.md)
[Lessons Learned](Lessons_learned.md)
