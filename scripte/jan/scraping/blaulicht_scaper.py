from email.mime import base
import requests
import pandas as pd
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime
import os

def scrape(stadt: str, save_as_csv: bool = True):
    """
    städte = Dresden, Erfurt, Hamburg, München, Nürnberg, Chemnitz, Dortmund
    """
    stast = stadt
    base_url: str = f"https://www.presseportal.de/blaulicht/r/{stadt}"
    data: list[dict]  = []
    seite: int = 0
    counter: int = 0

    print("===== Starte Scraping =====")
    while True:
        url: str = f"{base_url}/{seite}"
        print("Scrape URL:", url)
        print("- Seite:" + str(1 if seite < 30 else seite - 28))
        response = requests.get(url)

        if response.status_code != 200:
            print("Bad Status code. Code: ", response.status_code)
            break

        soup = BeautifulSoup(response.text, "html.parser")

        artikel_liste = soup.find_all("article", class_="news")

        for artikel in artikel_liste:
            datum = artikel.find("div", class_="date").text.strip()
            title = soup.find("h3", class_="news-headline-clamp").find("a").text.strip()
            abstract = soup.find("p", class_="")
            link = soup.find("h3", class_="news-headline-clamp").find("a")["href"]
            

            data.append({
                "stadt": stadt,
                "datum": datum,
                "title": title,
                "abstract": abstract,
                "link": link
            })
            counter += 1

        if seite > 30:
            break 

        if not artikel_liste:
            print("Letzte Seite erreicht. Beende das Scrapen")
            break

        x = random.random()*8
        print(f"Warten für {round(x, 1)} Sekunden\n"+"_"*50)
        time.sleep(x)
        seite += 30

    print(f"- Es wurden für {stadt}: {len(artikel_liste)} gefunden")

    downloadzeit =  datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")
    df = pd.DataFrame(data)
    
    if save_as_csv:
        csv_name = f"{stadt}_blaulicht_scrape_{downloadzeit}"
        df.to_csv(f"Daten_sets/{csv_name}.csv", index=False, encoding="utf-8")
    
    return df

scrape(stadt="Dortmund")

#print(df.loc[df["title"].str.contains("Drogen")])
