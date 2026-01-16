# Projektbericht: Korrelation von Abwasserdaten und Drogenkriminalität (2020-2024)

## 1. Einleitung & Motivation

### 1.1 Themenfindung
Zu Beginn des Projekts standen wir vor der Wahl, Wetterdaten mit Bewegungsdaten zu verknüpfen oder öffentliche Klärwerksdaten zu analysieren, um Rückschlüsse auf den Drogenkonsum in Städten zu ziehen. Basierend auf Berichten der europäischen Drogenbeobachtungsstelle (EUDA) entschieden wir uns für den gesellschaftlich relevanteren Ansatz der Abwasseranalyse.

> **Quelle:** [Waste water analysis - EUDA](https://www.euda.europa.eu/publications/html/pods/waste-water-analysis_en)

### 1.2 Ursprüngliches Forschungsziel
Unsere initiale Forschungsfrage lautete: *Wie ist der Zusammenhang zwischen Kokainkonsum und lokaler Berichterstattung über Kokain im Zeitraum von 2020 bis 2024?*

---

## 2. Projektmanagement (Methodik)

Wir haben uns für einen **adaptierten agilen Ansatz** entschieden, der speziell auf die begrenzten Zeitressourcen eines Studentenprojekts zugeschnitten wurde.

### 2.1 Der "Vorlesungs-Sprint"
Anstatt klassischer 2-Wochen-Sprints orientierte sich unser Rhythmus an den Vorlesungen:
* **Sprint-Dauer:** 1 Woche (Donnerstag bis Donnerstag).
* **Sprint Review & Planning:** Wöchentlich im Anschluss an die Vorlesung (Face-to-Face). Hier wurden die Ergebnisse der Woche präsentiert und die Aufgaben für die nächste Woche verteilt.

### 2.2 Tandem-Struktur & Dailies
Um die Absprache zu verbessern und Wissen direkt zu teilen, haben wir statt großer Daily-Scrums auf **Entwicklungstandems** gesetzt.
* **Konzept:** Aufgaben werden primär in 2er-Gruppen bearbeitet (Pair Programming).
* **Vorteil:** Direkte gegenseitige Verantwortlichkeit (Accountability) und schnelle Problemlösung ("Mini-Dailies" auf Zuruf) ohne lange Meetings.

### 2.3 Tools & Kommunikation
* **Kanban Board (Trello):** Zur Visualisierung des Workflows, Backlog-Pflege und Meilenstein-Tracking.
    * [Link zum Projekt-Board](https://trello.com/b/tz49lLdt/mein-trello-board)
* **WhatsApp:** Für schnelle, asynchrone Abstimmungen (Short-Polls) und Link-Sammlung.

---

## 3. Team & Rollenverteilung

Jedes Teammitglied agierte primär als **Developer**. Zusätzlich wurden spezifische Management-Rollen verteilt, um den Overhead gering zu halten:

| Name | Rolle | Verantwortungsbereich |
| :--- | :--- | :--- |
| **Leon** | **Product Owner / Scrum Master** | Gesamtkoordination, Backlog-Priorisierung, Roadmap-Überwachung. |
| **Lene** | **Project Enablement** | Stakeholder Management (Dozenten), Anforderungsanalyse, Beseitigung von Blockern ("Impediment Removal"). |
| **Jan** | **Tech Enablement** | DevOps, Bereitstellung Virtual Environment, Git-Repository Management & Merge-Strategien. |
| **Kenan** | **Time Keeper** | Überwachung der Timeboxen in Meetings, Ressourcen-Management (Pausenplanung). |
| **Ihsan, Felix, Josy** | **Advisory & QA** | Fachliche Beratung, Validierung von Lösungsansätzen, Qualitätssicherung. |

---

## 4. Verlauf

Das Projekt war geprägt von einem agilen Vorgehen. Aufgrund technischer und datenschutzrechtlicher Hürden mussten wir sowohl unsere Datengrundlage als auch unsere Arbeitsweise während des Semesters grundlegend anpassen.

### 4.1 Phase 1: Der ursprüngliche Plan (Lokalnachrichten)
Zu Beginn wurde eine Roadmap durch **Leon** erstellt. Der Plan sah vor, Lokalnachrichten verschiedener Städte manuell zu scrapen. Die Aufgabenverteilung war geographisch organisiert:

* **Chemnitz, Dortmund:** Jan
* **Dresden, Erfurt:** Felix
* **Hamburg, Hannover:** Lene
* **Magdeburg, München:** Ihsan
* **Nürnberg, Saarbrücken:** Josy
* **Stuttgart:** Kenan

### 4.2 Phase 2: Die Hürde (Blocker)
Während der ersten Scraping-Versuche traten massive Probleme auf, die das ursprüngliche Konzept unmöglich machten:
1.  **Archiv-Lücken:** Viele lokale Nachrichtenseiten boten keine historischen Daten bis 2020.
2.  **Struktur:** Berichte waren oft nur schwer über Suchleisten auffindbar.
3.  **Compliance (Robots.txt):** Die meisten Nachrichtenseiten untersagten das automatisierte Auslesen (Scraping) in ihrer `robots.txt` ausdrücklich.

### 4.3 Phase 3: Der Pivot & Neustart (Blaulicht-Reports)
Um das Projektziel zu retten, wechselten wir die Datenquelle auf Polizeiberichte ("Blaulicht") des Presseportals ([Link](https://www.presseportal.de/blaulicht/)). Dies erforderte eine komplette Umstrukturierung des Teams und der Aufgaben:

**Neue Rollenverteilung & Technischer Lead:**
Da die manuelle Aufteilung hinfällig war, zentralisierten wir den Scraping-Prozess.
* **Scraping Lead:** Jan entwickelte einen zentralen Scraper für alle Städte, inklusive einer **Proxy-Rotation**, um Blocking zu verhindern.
* **Data Cleaning:** Lene (Wasserwerksdaten) und Ihsan (Blaulicht-Reports) bereinigten die Datensätze, unterstützt von Leon.

### 4.4 Angepasste Forschungsfrage
Durch den Wechsel der Datenquelle haben wir die Frage präzisiert:
*Besteht eine Korrelation zwischen der relativen Häufigkeit von Berichten zu Drogendelikten in einer Stadt und dem tatsächlichen Drogenkonsum laut Abwasserdaten?*

---

## 5. Technische Umsetzung & Methodik

### 5.1 Feature Engineering (TF/IDF)
Da die bloße Anzahl der Berichte aufgrund variierender Artikelmengen über die Jahre (2020-2024) verzerrt wäre, musste eine Normalisierung stattfinden.
* **Umsetzung:** Kenan (Support: Josy)
* **Methode:** Berechnung von TF/IDF-Werten, um relevante Berichte ins Verhältnis zur Gesamtmenge der Nachrichten zu setzen.

### 5.2 Daten-Selektion
Nach der ersten Evaluation mussten wir die Anzahl der untersuchten Städte reduzieren, da für einige Standorte zu große Lücken in den Abwasser- oder Polizeidaten bestanden.
* **Finales Set:** Chemnitz, Dortmund, Erfurt, München, Nürnberg, Saarbrücken.
* **Ausgeschlossen:** Dresden, Hamburg, Hannover, Stuttgart, Magdeburg.

### 5.3 Hypothesentest
Zum Abschluss wurde statistisch geprüft, ob die vermutete Korrelation signifikant ist.
* **Durchführung:** Felix (Support: Leon, Lene)
* **Scope:** Tests für einzelne Städte sowie für den Gesamtdatensatz.

---

## 6. Retrospektive (Lessons Learned)

Zum Abschluss des Projekts bewerten wir den Verlauf und unsere Zusammenarbeit mit der **5-Finger-Methode**:

* 👍 **Daumen (Das lief super): Team-Commitment & Klima**
  Trotz der Herausforderungen ist niemand "abgetaucht". Die Teilnahme an den Vor-Ort-Terminen war konstant hoch und der zwischenmenschliche Umgang sehr positiv. Der Zusammenhalt im Team war das Fundament, das das Projekt am Laufen hielt.

* 👉 **Zeigefinger (Das ist uns aufgefallen): Management-Overhead**
  Wir haben unterschätzt, dass Koordination massiv Zeit kostet. Bei einer Gruppengröße von 7 Personen den Überblick zu behalten und *alle* Perspektiven aktiv einzubeziehen, war deutlich aufwendiger als gedacht und hat viele Ressourcen gebunden.

* 🖕 **Mittelfinger (Das war schwierig): Skalierung & Abhängigkeiten**
  * **Sequenzielle Abhängigkeiten:** Da viele Aufgaben aufeinander aufbauten (z.B. Cleaning erst nach Scraping), konnten wir selten wirklich parallel arbeiten. Für 7 Leute gab es oft nicht gleichzeitig genug zu tun.
  * **Disziplin:** Die geplante "Tandem-Struktur" (2er-Teams) löste sich oft auf und wurde zu ineffizientem "Gruppen-Brainstorming".
  * **Kommunikation:** Absprachen waren teils missverständlich, was zu unnötigen Schleifen führte.

* 💍 **Ringfinger (Das nehmen wir mit): Resilienz & Realismus**
  Nichts läuft exakt wie geplant – und das ist okay. Wir haben gelernt, dass Hürden (wie das Scraping-Verbot) nicht das Projektende bedeuten, sondern nur eine Kurskorrektur erfordern. Eine solide Struktur ist dabei wichtiger als der perfekte Plan A.

* 🤏 **Kleiner Finger (Kam zu kurz): Prozess-Treue & Snacks**
  * **Methodik:** Das "Pair Programming" wurde im Eifer des Gefechts oft vergessen. Auch die Involvierung aller Mitglieder in *jeden* Teilprozess war bei der Gruppengröße nicht immer realisierbar.
  * **Verpflegung:** Die Snacks hätten üppiger ausfallen können.

---

## 7. Projektabschluss

Für die Abschlusspräsentation ist das Team wie folgt aufgestellt:

| Mitglied | Verantwortungsbereich |
| :--- | :--- |
| **Josy** | Hypothese (Intro), Support PM |
| **Lene** | Wasserwerksdaten, Presseportal-Vorstellung |
| **Jan** | Technical Lead Scraping, Proxy Rotation |
| **Ihsan** | Data Cleaning |
| **Kenan** | Feature Engineering (TF/IDF) |
| **Felix** | Hypothesentest & Statistik |
| **Leon** | Projektmanagement, Roadmap |