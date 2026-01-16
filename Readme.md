# 🧪 Analyse der Korrelation zwischen Abwasser-Drogenrückständen und Polizeiberichten

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Status](https://img.shields.io/badge/Status-In_Progress-yellow.svg)

> **Dokumentation:** [Projekt-Report lesen](./ProjectReport.md)  
> **Planung:** [Roadmap ansehen](./Roadmap.md)
[Unser Trello Board](assets/trello.png)
> **Lessons Learned:** [Lessons Learned ansehen](Lessons_learned.md)

Dieses Repository enthält die Forschungsarbeit der **Gruppe 4** zur statistischen Beziehung zwischen chemisch nachgewiesenem Drogenkonsum und der öffentlichen Berichterstattung über drogenspezifische Delikte.

---

## 🎯 Projektziel

Wir stellen objektive Messwerte aus Kläranlagen den quantitativen Daten aus dem **Blaulichtreport** (Presseportal) gegenüber.

* **Forschungsfrage:**  
  Korreliert die Menge der Drogenrückstände im Abwasser mit der Häufigkeit polizeilicher Meldungen in deutschen Großstädten?
* **Untersuchte Städte:**  
  Chemnitz, Dortmund, Erfurt, München, Nürnberg, Saarbrücken

---

## 📝 Projektbeschreibung

Ziel dieses Projekts ist es zu untersuchen, ob eine messbare **Korrelation zwischen konsumierten Drogen** (basierend auf Abwasseranalysedaten der **EUDA**, ehemals EMCDDA) und der **Anzahl polizeilicher Meldungen** in den jeweiligen Städten besteht.

Hierbei werden objektive Messwerte aus Wasserwerken systematisch den quantitativen Daten des Presseportals gegenübergestellt.

---

## 🗂 Projektstruktur

```text
DIS08_Data_modeling/
├── src/
│   └── scraping/
│       ├── blaulicht_scaper.py   # Haupt-Scraper (Multiprocessing)
│       ├── get_proxies.py        # Proxy-Rotation
│   └── config.ini                # Zentrale Konfiguration
├── notebooks/
│   ├── analyse.ipynb             # Deskriptive Statistik & Visualisierung
│   ├── Hypothesentest.ipynb      # Spearman-Korrelation & Signifikanztests
│   └── retrieval.ipynb           # TF-IDF & IR-Analyse
├── data/
│   ├── raw/                      # Rohdaten
│   └── processed/                # Bereinigte CSV-Dateien
├── requirements.txt
└── README.md
```

---

## 🛠 Methodik & Features

Das Projekt deckt den gesamten **Data-Science-Zyklus** ab – von der Datenerhebung bis zur statistischen Auswertung:

### Scraping & Datenerhebung

* Ursprünglich war das Scraping mehrerer lokaler Nachrichtenquellen geplant.
* Zur besseren **Skalierbarkeit** und **Wartbarkeit** wurde der Fokus auf den zentralen **Blaulichtreport** gelegt.
* Ergebnis ist ein spezialisierter Scraper, der mehrere Städte effizient aggregiert, ohne quellspezifische Logik zu benötigen.

### Data Cleaning & Vorbereitung

* Bereinigung und Vereinheitlichung der Rohdaten.
* Zusammenführung in einen konsolidierten Datensatz mit den Variablen:

  * Stadt
  * Jahr
  * Drogentyp
  * Berichthäufigkeit

### Information Retrieval (IR)

* Einsatz von IR-Techniken zur Quantifizierung relevanter Polizeiberichte pro Stadt und Jahr.
* Ziel: Abbildung der öffentlichen Wahrnehmung bzw. polizeilichen Dokumentation von Drogendelikten.
[Häufigkeit der Schlagwörter](assets/drogen_wordcloud.jpeg)

### Statistische Auswertung

* Untersuchung der Korrelation zwischen:

  * **Milligramm pro Tag (daily mean)** aus Abwasseranalysen
  * **Trefferquote** aus dem Information Retrieval
* Einsatz von **Spearman-Rangkorrelation** und Signifikanztests.

---

## Voraussetzungen

* **Python:** Version 3.12 oder höher
* **Paketmanager:** `pip`

---

## 🛠 Installation & Setup

### 1️⃣ Repository klonen

```bash
git clone https://github.com/ichzann/DIS08_Data_modeling.git
cd DIS08_Data_modeling
```

### 2️⃣ Virtuelle Umgebung erstellen (empfohlen)

**Windows**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

---

## Konfiguration & Nutzung

### Städte anpassen

In der Datei `config.ini` können die zu analysierenden Städte festgelegt werden:

```ini
[ScrapingEinstellungen]
staedte = Chemnitz, Dortmund, München
tempo = 10
```

### Scraper starten

```bash
python src/scraping/blaulicht_scaper.py
```

### Analysen durchführen

```bash
jupyter notebook
```

Beispiele:

* `analyse.ipynb` – Visualisierungen & deskriptive Statistik
* `Hypothesentest.ipynb` – Korrelationen & Signifikanztests

---

## Ergebnisse (Auszug)

* Erste **Spearman-Hypothesentests** zeigen für den Gesamtdatensatz keinen signifikanten Zusammenhang (p-Wert > 0.05).
* Einzelne Städte wie **Chemnitz** und **Erfurt** weisen jedoch starke Korrelationen auf und werden weiter untersucht.

---


