import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import quote
from pywhapbot import WhapBot


def wiki_parser():
    url = requests.get("https://es.wikipedia.org/wiki/Anexo:Diputados_de_la_XIV_legislatura_de_Espa%C3%B1a")
    soup = BeautifulSoup(url.text, "lxml")
    table = soup.find("table", {"class": "wikitable sortable"})
    df = pd.DataFrame(pd.read_html(str(table))[0])

    politics = df.get("Nombre y apellidos").to_list()
    for idx, pol in enumerate(politics):
        surname, name = pol.split(",")
        politics[idx] = f"{name} {surname}".strip()

    parties = df.get("Lista.1").to_list()

    # return list(zip(politics, parties))
    return list(map(list, zip(politics, parties)))


def search_twitter(politic):
    url = f"https://twitter.com/search?q={quote(politic)}&src=typed_query&f=user"
    with WhapBot("chrome") as bot:
        bot.get(url)
        a = input("Select the profile geoffrense: ")
        if a.lower() == "none":
            twitter = None
        else:
            twitter = bot.driver.current_url.split("/")[-1]
    return twitter
