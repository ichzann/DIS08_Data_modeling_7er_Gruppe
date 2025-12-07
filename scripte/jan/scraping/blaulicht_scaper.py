import requests
import pandas as pd
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime
from multiprocessing import Pool
import configparser
import os
from get_proxies import write_working_proxies

def load_proxies_from_file():
    PROXY_FILE_PATH = 'scripte/jan/scraping/working_proxies.txt'
    if not os.path.exists(PROXY_FILE_PATH):
        print(f"Warnung: Proxy-Datei {PROXY_FILE_PATH} nicht gefunden.")
        return []
    
    with open(PROXY_FILE_PATH, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    return proxies


def make_request_with_proxy(url, proxy_list, max_retries=10):
    if not proxy_list:
        print("Keine Proxies geladen, soll direkte Verbindung verwendet werden?")
        if input("Y/N").upper() == "Y":
            try:
                return requests.get(url, timeout=10)
            except Exception as e:
                print(f"Direkte Verbindung fehlgeschlagen: {e}")
                return None
        else:
            print("Scraping versuch abgebrochen")

    for attempt in range(max_retries):
        proxy = random.choice(proxy_list)
        proxies_dict = {'http': proxy, 'https': proxy}
        
        try:
            response = requests.get(url, proxies=proxies_dict, timeout=8)
            
            if response.status_code == 200:
                return response
            elif response.status_code == 404:
                return response
            else:
                continue    # Nächsten Proxy probieren
                
        except Exception:
            # Verbindungstimeout oder Proxy Fehler. Nächster Versuch
            continue
            
    print(f"Fehler: Konnte URL auch nach {max_retries} Versuchen mit verschiedenen Proxies nicht laden.")
    return None

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

    print(f"\n\n\n===== Starte Scraping für {stadt} =====")

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


def load_cities_from_config():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, 'config.ini')
    
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    
    try:
        cities_string = config['ScrapingEinstellungen']['staedte']
    except KeyError:
        print("Fehler: Konnte 'staedte' in config.ini nicht finden.")
        return []

    cities_list = [city.strip() for city in cities_string.split(',')]
    
    return cities_list


def main():
    target_cities = load_cities_from_config()
    print("="*60)
    print("""
    ██████╗ ██╗      █████╗ ██╗   ██╗██╗██╗ ██████╗██╗  ██╗████████╗
    ██╔══██╗██║     ██╔══██╗██║   ██║██║██║██╔════╝██║  ██║╚══██╔══╝
    ██████╔╝██║     ███████║██║   ██║██║██║██║     ███████║   ██║   
    ██╔══██╗██║     ██╔══██║██║   ██║██║██║██║     ██╔══██║   ██║   
    ██████╔╝███████╗██║  ██║╚██████╔╝██║██║╚██████╗██║  ██║   ██║   
    ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   
                                                                    
    ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗         
    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗        
    ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝        
    ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗        
    ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║        
    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
    """)
    print("="*60)
    print("Suche frische Proxies...")
    write_working_proxies()
    with Pool(processes=1) as p:
        p.map(scrape, target_cities)



if __name__ == "__main__":
    main()


