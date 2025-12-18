import requests
import pandas as pd
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime
import os

def scrape_einfach(stadt: str, save_as_csv: bool = True, tempo: int = 10):
    """
    Abgespeckte Version des Scrapers ohne Proxies und Multiprocessing.
    """
    base_url = f"https://www.presseportal.de/blaulicht/r/{stadt}"
    data = []
    seite = 0
    article_counter = 0
    
    print(f"\n--- Starte Scraping für {stadt} ---")

    while True:
        url = f"{base_url}/{seite}"
        aktuelle_seite_num = 1 if seite < 29 else int(seite / 30) + 1
        
        print(f"Lade Seite {aktuelle_seite_num} für {stadt}...")
        
        try:
            # Einfacher Request ohne Proxy
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"Abbruch: Status Code {response.status_code}")
                break
        except Exception as e:
            print(f"Fehler beim Request: {e}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        artikel_liste = soup.find_all("article", class_="news")

        if not artikel_liste:
            print(f"Keine weiteren Artikel für {stadt} gefunden.")
            break

        for artikel in artikel_liste:
            try:
                datum = artikel.find("div", class_="date").text.strip()
                title_element = artikel.find("h3", class_="news-headline-clamp").find("a")
                title = title_element.text.strip().replace("\n", "")
                link = title_element["href"]
                id_tag = "/".join(link.rsplit("/", 2)[-2:])
                
                abstract_tag = artikel.find("p", class_=None)  

                if abstract_tag:
                    abstract = abstract_tag.text.strip()
                else:
                    # Falls kein Abstract da ist, Unterseite laden (ohne Proxy)
                    time.sleep(random.random() * 1 / tempo)
                    sub_res = requests.get(link, timeout=10)
                    sub_soup = BeautifulSoup(sub_res.text, "html.parser")
                    abschnitte = [p.text.strip() for p in sub_soup.find_all("p", class_=None)[1:]]
                    abstract = " ".join(abschnitte).replace("\n", " ")

                data.append({
                    "stadt": stadt,
                    "datum": datum,
                    "id": id_tag,
                    "title": title,
                    "abstract": abstract,
                    "link": link
                })
                article_counter += 1
                
            except Exception as e:
                print(f"Fehler bei Artikel-Extraktion: {e}")

        # Paginierung: Presseportal nutzt 30er Schritte
        seite += 30
        
        # Kurze Pause, um die Seite nicht zu fluten
        time.sleep(random.random() * 1 / tempo)

    # Speichern
    if save_as_csv and data:
        df = pd.DataFrame(data)
        downloadzeit = datetime.now().strftime("%Y-%m-%d")
        csv_name = f"{stadt}_blaulicht_scrape_{downloadzeit}.csv"
        
        # Ordner erstellen falls nicht existiert
        os.makedirs("Daten_sets/blaulicht_scraping", exist_ok=True)
        path = f"Daten_sets/blaulicht_scraping/{csv_name}"
        
        df.to_csv(path, index=False, encoding="utf-8")
        print(f"Fertig! {article_counter} Artikel für {stadt} in '{path}' gespeichert.")
    
    return data

def main():
    target_cities = ["München"]
    
    for stadt in target_cities:
        scrape_einfach(stadt)

if __name__ == "__main__":
    main()