import re
from matplotlib.pyplot import fill
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from multiprocessing import Pool

def get_proxies():
    url: str = "https://free-proxy-list.net/de/ssl-proxy.html"
    daten_dic: list[dict] = []
    headers_list = []
    response = requests.get(url=url)

    if response.status_code == 200:
        response_text = response.text
        soup = BeautifulSoup(response_text, "html.parser")
        table = soup.find("table", class_="table table-striped table-bordered")

        # Überschriften ziehen
        headers = table.find_all("th")
        for header in headers:
            headers_list.append(header.text)

        # Tabbellen Inhalt
        table_content = table.find_all("tbody")
        row = table.find_all("tr")

        for column in row:
            values = column.find_all("td")
            
            filler_dic = {}
            for index, value in enumerate(values):
                filler_dic[headers_list[index]] = value.text
            daten_dic.append(filler_dic)     
    return daten_dic


def check_proxy(proxy_string):
    try:
        response = requests.get('https://httpbin.org/ip', proxies={'http': proxy_string, 'https': proxy_string}, timeout=3)
        print(f"[+] Funktioniert:\t{proxy_string}")
        return proxy_string
    except:
        print(f"    unavailable:\t{proxy_string}")
        return False


def main():
    print("\n- Sammle Proxies von: https://httpbin.org/ip\n")
    daten_dic = get_proxies()
    
    proxy_liste = []
    for eintrag in daten_dic:
        if "IP Address" in eintrag and "Port" in eintrag:
            ip = eintrag["IP Address"]
            port = eintrag["Port"]
            proxy_liste.append(f"{ip}:{port}")

    print(f"- Insgesamt {len(proxy_liste)} Proxies gefunden. Starte health check for Proxies\n\n- Starte dafür Multiprocessing mit: 10 Threads")

    working_proxies = []

    with Pool(processes=10) as p:
        ergebnisse = p.map(check_proxy, proxy_liste)

    # None/ False Werte rauswerfn
    working_proxies = [proxy for proxy in ergebnisse if proxy is not None or False]

    print(f"\nFertig - {len(working_proxies)} funktionierende Proxies gefunden.")


    pfad = 'scripte/jan/scraping/working_proxies.txt' 
    with open(pfad, 'w') as f:
        for p in working_proxies:
            f.write(f"{p}\n")
    print(f"Gespeichert unter {pfad}")


if __name__ == '__main__':
    main()

