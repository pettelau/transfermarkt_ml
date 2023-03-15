import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")
print(soup)
players = []
for player in soup.find_all("tr", class_="odd"):
    name = player.find("a").text
    position = player.find("td", class_="zentriert").text
    value = (
        player.find("td", class_="rechts").text.replace("\u20ac", "").replace("m", "")
    )

    players.append([name, position, value])

df = pd.DataFrame(players, columns=["Name", "Position", "Value"])
print(df)
