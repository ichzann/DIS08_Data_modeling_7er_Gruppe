import re
from matplotlib.pyplot import fill
import requests
from bs4 import BeautifulSoup
from pprint import pprint


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


def is_proxy_working(proxy):
    try:
        response = requests.get('https://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=5)
        return response.status_code == 200
    except:
        return False


def write_working_proxies():
    working_proxies = []
    daten_dic = get_proxies()
    for eintrag in daten_dic:
        if not eintrag or "IP Address" not in eintrag:
            continue

        ip = eintrag["IP Address"]
        port = eintrag["Port"]

        proxy_string = f"{ip}:{port}" 

        print(f"Teste: {proxy_string} -", end="", sep="\t")
        if is_proxy_working(proxy_string):
            print(" OK!")
            working_proxies.append(proxy_string)
        else:
            print(" Fehlgeschlagen.")

    with open('working_proxies.txt', 'w') as f:
        for p in working_proxies:
            f.write(f"{p}\n")

write_working_proxies()