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


