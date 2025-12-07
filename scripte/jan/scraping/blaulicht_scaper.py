import requests
import pandas as pd
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime
from multiprocessing import Pool, Lock
import configparser
import os
from get_proxies import main_proxies
from colorama import Fore, Style, init

# Init colorama für Windows Kompatibilität
init()

# Globale Variable für den Lock innerhalb der Worker-Prozesse
print_lock = None

def init_worker(l):
    global print_lock
    print_lock = l

def get_city_color(stadt):
    """Weist jeder Stadt eine feste Farbe zu"""
    colors = [Fore.GREEN, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.BLUE, Fore.RED]
    # Einfacher Hash, damit die gleiche Stadt immer die gleiche Farbe bekommt
    color_index = sum(ord(c) for c in stadt) % len(colors)
    return colors[color_index]

def safe_print(text, stadt="System"):
    """Thread-sicheres Drucken mit Farben"""
    color = get_city_color(stadt)
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # Der Lock sorgt dafür, dass dieser Block nicht unterbrochen wird
    with print_lock:
        # Wir färben nur den Städtenamen und den Timestamp
        prefix = f"{Style.BRIGHT}{color}[{timestamp} | {stadt:<10}]{Style.RESET_ALL}"
        # Wenn der Text mehrere Zeilen hat (wie deine Tabelle), rücken wir sie ein
        formatted_text = text.replace("\n", f"\n{' ' * 24}")
        print(f"{prefix} {formatted_text}")

def load_proxies_from_file():
    PROXY_FILE_PATH = 'scripte/jan/scraping/working_proxies.txt'
    if not os.path.exists(PROXY_FILE_PATH):
        print(f"Warnung: Proxy-Datei {PROXY_FILE_PATH} nicht gefunden.")
        return []
    
    with open(PROXY_FILE_PATH, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    return proxies


def make_request_with_proxy(url, proxy_list, max_retries=10, context="System"):
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
        safe_print(f"[{context}] Versuch {attempt+1}/{max_retries} mit Proxy: {proxy}")
        
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
            
    safe_print(f"{Fore.RED}FEHLER: Alle Proxies fehlgeschlagen.{Style.RESET_ALL}", context)
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
    proxy_list = load_proxies_from_file()

    safe_print(f"\n\n\n===== Starte Scraping für {stadt} =====")

    while True:
        url: str = f"{base_url}/{seite}"
        eigentliche_seite = str(1 if seite < 29 else int(seite / 30) + 1)  # Da die webseite mit einem vielfachen von 30 pagnation 

        response = make_request_with_proxy(url, proxy_list, context=stadt)
        request_counter += 1

        if response.status_code != 200:
            print("Bad Status code. Code: ", response.status_code)
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        artikel_liste = soup.find_all("article", class_="news")

        msg = f"{len(artikel_liste)} Artikel auf Seite {eigentliche_seite} gefunden.\n"
        msg += f"{'Datum':<18} {'ID':<15} {'Titel':<30}\n"
        msg += f"{'_'*18} {'_'*15} {'_'*30}"    

        for artikel in artikel_liste:
            datum = artikel.find("div", class_="date").text.strip()
            title = artikel.find("h3", class_="news-headline-clamp").find("a").text.strip().replace("\n", "")
            link = artikel.find("h3", class_="news-headline-clamp").find("a")["href"]
            id_tag = "/".join(link.rsplit("/", 2)[-2:])
            abstract_tag = artikel.find("p", class_=None)  

            msg += f"\n{datum:<18} {id_tag:<15} {title[:30]}"

            if abstract_tag:
                abstract = abstract_tag.text.strip() 
            # wenn abstract nicht da ist, soll der Text vom verlinketen artikel genommen werden 
            else:
                try:
                    time.sleep(random.random()*2/tempo)
                    response_unterseite = make_request_with_proxy(link, proxy_list, context=stadt)
                    abstract_soup_unterseite = BeautifulSoup(response_unterseite.text, "html.parser")
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

        safe_print(msg, stadt) 
        x = random.random()*2 / tempo  
        time.sleep(x)
        seite += 30


    safe_print(f"Fertig! {article_counter} Artikel in {request_counter} Requests gefunden.", stadt)

    downloadzeit =  datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")
    df = pd.DataFrame(data)
    
    if save_as_csv and not df.empty:
        csv_name = f"{stadt}_blaulicht_scrape_{downloadzeit}"
        df.to_csv(f"Daten_sets/blaulicht_scraping/{csv_name}.csv", index=False, encoding="utf-8")
        print(f"DataFrame als CSV gespeichert. Dateiname: {csv_name}")
        safe_print(f"Fertig! {article_counter} Artikel gespeichert.", stadt)
    
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
    print("="*80)
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
    print("="*80)
    print("Suche frische Proxies...")
    main_proxies()
    l = Lock()
    anzahl_prozesse = 2
    print(f"Starte Multiprocessing mit {anzahl_prozesse} Prozessen für {len(target_cities)} Städte...")

    with Pool(processes=anzahl_prozesse, initializer=init_worker, initargs=(l,)) as p:
        p.map(scrape, target_cities)



if __name__ == "__main__":
    main()


