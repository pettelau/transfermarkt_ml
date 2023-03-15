import pandas as pd

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


# player_code = "lionel-messi"
# pid = 28003
# player_code = "mesut-ozil"
# pid = 35664


def season_data(pid, player_code):
    # URL
    url = f"https://www.transfermarkt.com/{player_code}/leistungsdatendetails/spieler/{pid}/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1"

    # Request
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    try:
        temp = pd.read_html(str(soup.find("table", class_="items")))[0]
    except Exception as e:
        return pd.DataFrame()
    
    td_tags = soup.find("table", class_="items").find_all(
        "td", {"class": "hauptlink no-border-rechts zentriert"}
    )

    td_tags_league = soup.find("table", class_="items").find_all(
        "td", {"class": "hauptlink no-border-links"}
    )

    hrefs = [td.find("a").get("href") for td in td_tags]
    hrefs_league = [td.find("a").get("href") for td in td_tags_league]

    # print(len(hrefs))
    # print(hrefs)

    temp2 = temp.drop(temp.columns[[1, 3, 4, 9, 10, 11, 18]], axis=1)

    temp2.drop(temp2.tail(1).index, inplace=True)

    renamed = temp2.rename(
        columns={
            temp2.columns[1]: "Competition",
            temp2.columns[2]: "Games",
            temp2.columns[3]: "PPG",
            temp2.columns[4]: "Goals",
            temp2.columns[5]: "Assists",
            temp2.columns[6]: "Yellow_cards",
            temp2.columns[7]: "Yellow_red_cards",
            temp2.columns[8]: "Red_cards",
            temp2.columns[9]: "Penalty_goals",
            temp2.columns[10]: "Minutes_per_goal",
            temp2.columns[11]: "Minutes_played",
        }
    )

    # add club id to dataframe of player
    renamed["Club_id"] = np.zeros(len(renamed))

    if len(hrefs) == len(renamed):
        for index, href in enumerate(hrefs):
            club_id = href.split("/")[4]
            renamed["Club_id"][index] = club_id

    # add competition type to dataframe of player
    renamed["League_type"] = np.zeros(len(renamed))

    if len(hrefs_league) == len(renamed):
        for index, href_league in enumerate(hrefs_league):
            tournament_type = href_league.split("/")[3]
            renamed["League_type"][index] = tournament_type

    columns_to_replace = [
        "Games",
        "Goals",
        "Assists",
        "Yellow_cards",
        "Yellow_red_cards",
        "Red_cards",
        "Penalty_goals",
    ]

    for column in columns_to_replace:
        if pd.api.types.is_integer_dtype(renamed[column].dtype):
            continue
        else:
            renamed[column] = renamed[column].astype(str).str.replace("-", "0").astype(float).astype(int)

    ## PPG
    if not pd.api.types.is_float_dtype(renamed["PPG"]):
        renamed["PPG"] = renamed["PPG"].astype(str).str.replace("-", "0").astype(float)

    ## Minutes per goal
    renamed["Minutes_per_goal"] = renamed["Minutes_per_goal"].astype(str).str.replace("-", "0")

    renamed["Minutes_per_goal"] = (
        renamed["Minutes_per_goal"].str.replace(r"\D", "").astype(int)
    )

    ## Minutes played
    renamed["Minutes_played"] = renamed["Minutes_played"].str.replace("-", "0")

    renamed["Minutes_played"] = (
        renamed["Minutes_played"].str.replace(r"\D", "").astype(int)
    )

    # SEASON
    if pd.api.types.is_float_dtype(renamed["Season"]):
        renamed["Season"] = renamed["Season"].apply(lambda x: int(x))
    else:
        renamed["Season"] = renamed["Season"].apply(
            lambda x: int("20" + x.split("/")[0]) if "/" in x else int(x[-4:])
        )

    return renamed


df_players = pd.read_csv("./archive/players.csv")


df = df_players[["player_id", "player_code", "position"]]

df2 = df[5000:7500]

df2 = df2.loc[df["position"] != "Goalkeeper"]


appended_data = []
for index, row in df2.iterrows():
    print("I: ", index, "PID: ", row["player_id"])
    player_id, player_code = row["player_id"], row["player_code"]
    try:
        player_data = season_data(player_id, player_code)
    except Exception as e:
        appended_data = pd.concat(appended_data)
        player_id_column = appended_data.pop("player_id")
        appended_data.insert(0, "Player_id", player_id_column)
        appended_data.to_csv("season_data_3.csv", index=False)
        print(e)

    if not player_data.empty:
        player_data["player_id"] = player_id
        appended_data.append(player_data)

appended_data = pd.concat(appended_data)

player_id_column = appended_data.pop("player_id")

appended_data.insert(0, "Player_id", player_id_column)

appended_data.to_csv("season_data_3.csv", index=False)

# season_data(76948, "pablo-olivera")
