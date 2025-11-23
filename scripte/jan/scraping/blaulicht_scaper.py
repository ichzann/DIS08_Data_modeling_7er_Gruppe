from operator import rshift
from urllib import request
import requests
import pandas as pd
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime
import os
from pprint import pprint

def scrape(stadt: str, save_as_csv: bool = True, tempo: int = 10):
    """
    städte:         Dresden, Erfurt, Hamburg, München, Nürnberg, Chemnitz, Dortmund\n
    save_as_csv:    True, False (wenn gespeichert werden soll als CSV)\n
    tempo:          10 für schnell, 1 für langsam
    """
    base_url: str = f"https://www.presseportal.de/blaulicht/r/{stadt}"
    data: list[dict]  = []
    seite: int = 0
    article_counter: int = 0
    request_counter: int = 0

    print("\n\n\n===== Starte Scraping =====")

    while True:
        url: str = f"{base_url}/{seite}"
        print("Scrape URL:", url)
        eigentliche_seite = str(1 if seite < 29 else int(seite / 30) + 1)  # Da die webseite mit einem vielfachen von 30 pagnation 
        print("- Seite:" + eigentliche_seite)
        response = requests.get(url)
        request_counter += 1

        if response.status_code != 200:
            print("Bad Status code. Code: ", response.status_code)
            break

        soup = BeautifulSoup(response.text, "html.parser")

        artikel_liste = soup.find_all("article", class_="news")
        print(f"- {len(artikel_liste)} Artikel auf Seite {eigentliche_seite} gefunden.")
        print("- Scrape Artikel:\n    Datum: ", "ID:", "Titel:", "\t\tHinweis:", sep="\t"*2)
        print("    "+"_"*15+"\t"+"_"*15+"\t"+ "_"*30+"\t"+ "_"*28)

        for artikel in artikel_liste:
            datum = artikel.find("div", class_="date").text.strip()
            title = artikel.find("h3", class_="news-headline-clamp").find("a").text.strip().replace("\n", "")
            link = artikel.find("h3", class_="news-headline-clamp").find("a")["href"]
            id_tag = "/".join(link.rsplit("/", 2)[-2:])
            abstract_tag = artikel.find("p", class_=None)  
            if abstract_tag:
                print(f"    {datum}  {id_tag:<15}", f"{title[:30]}", sep="\t")
                abstract = abstract_tag.text.strip() 
            # wenn abstract nicht da ist, soll der Text vom verlinketen artikel genommen werden 
            else:
                try:
                    print(f"    {datum}  {id_tag:<15}", f"{title[:30]}", "Kein Abstact gehe zum Artikel", sep="\t")
                    time.sleep(random.random()*2/tempo)
                    abstract_soup_unterseite = BeautifulSoup(requests.get(link).text, "html.parser")
                    abstract_liste_unterseite = abstract_soup_unterseite.find_all("p", class_=None)
                    request_counter += 1

                    abschnitte = []
                    for abschnitt in abstract_liste_unterseite[1:]:
                        text = abschnitt.text.strip()
                        abschnitte.append(text)
                    abstract = " ".join(abschnitte).replace("\n", "")
                except Exception as e:
                    print("Exception", e)
                    abstract = "N/A"
                
            data.append({
                "stadt": stadt,
                "datum": datum,
                "id": id_tag,
                "title": title,
                "abstract": abstract,
                "link": link
            })
            article_counter += 1
            

        if not artikel_liste:
            print("Letzte Seite erreicht. Beende das Scrapen")
            break

        x = random.random()*8 / tempo
        print(f"- Seite Abgeschlossen. Warten für {round(x, 1)} Sekunden\n"+"_"*60)
        time.sleep(x)
        seite += 30


    print(f"- Es wurden bei {stadt}: {article_counter} Arktikel auf {eigentliche_seite} Seiten gefunden.")
    print(f"- Erledigt in {request_counter} Requests")

    downloadzeit =  datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")
    df = pd.DataFrame(data)
    
    if save_as_csv:
        csv_name = f"{stadt}_blaulicht_scrape_{downloadzeit}"
        df.to_csv(f"Daten_sets/blaulicht_scraping/{csv_name}.csv", index=False, encoding="utf-8")
        print(f"DataFrame als CSV gespeichert. Dateiname: {csv_name}")
    
    return df

scrape(stadt="Chemnitz", save_as_csv=True, tempo=8)

#print(df.loc[df["title"].str.contains("Drogen")])
