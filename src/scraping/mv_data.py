import re
import pandas as pd
import pyjsparser

pd.options.mode.chained_assignment = None
import numpy as np

import warnings

warnings.filterwarnings("ignore")

import time

import requests
from bs4 import BeautifulSoup

import sys
import time
from datetime import datetime
from termcolor import colored

from IPython.display import display

display = pd.options.display

display.max_columns = 1000
display.max_rows = 100

# test

# player_code = "lionel-messi"
# pid = 28003
# player_code = "mesut-ozil"
# pid = 35664


def mv_data(pid, player_code):
    # URL
    url = f"https://www.transfermarkt.com/{player_code}/marktwertverlauf/spieler/{pid}"

    # Request
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    # Name
    name = soup.find("h1").get_text()

    # Parsed
    script = soup.find("script", text=re.compile("Highcharts.Chart")).text
    # print(script)
    parsed = pyjsparser.parse(script)
    sc = parsed["body"][8]["expression"]["arguments"][1]["body"]["body"][1][
        "declarations"
    ][0]["init"]["arguments"][0]["properties"][5]["value"]["elements"][0]["properties"][
        2
    ][
        "value"
    ][
        "elements"
    ]

    mv = list(map(lambda x: int(x["properties"][0]["value"]["value"]), sc))
    club = list(map(lambda x: x["properties"][1]["value"]["value"], sc))
    date = list(map(lambda x: x["properties"][4]["value"]["value"], sc))

    mv_df = pd.DataFrame(
        {
            "MarketValue": mv,
            "Club": club,
            "Season": date,
        }
    )


    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    mv_df["Season"] = mv_df["Season"].apply(
        lambda x: int(x[-4:]) if months.index(x[0:3]) > 6 else int(x[-4:]) - 1
    )

    mv_df_2 = mv_df.drop_duplicates(subset=["Season"], keep="last")

    return mv_df_2


# mv_data(134354, 'ian-raeymaekers')


df_players = pd.read_csv("./archive/players.csv")


df = df_players[["player_id", "player_code"]]

df2 = df[0:7000]

start_time = time.time()
appended_data = []
for index, row in df2.iterrows():
    player_id, player_code = row["player_id"], row["player_code"]
    print("I: ", index, "PID: ", player_id)
    try:
        player_data = mv_data(player_id, player_code)
    except Exception as e:
        print(e)
        continue
    player_data["player_id"] = player_id
    appended_data.append(player_data)

end_time = time.time()
appended_data = pd.concat(appended_data)

player_id_column = appended_data.pop("player_id")

appended_data.insert(0, "Player_id", player_id_column)

appended_data.to_csv("mv_1.csv", index=False)

print("Elapsed time: ", end_time - start_time)
