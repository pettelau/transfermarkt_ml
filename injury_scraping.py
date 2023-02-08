import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup

import sys
import time
from datetime import datetime
from termcolor import colored


def get_injuries(player_code, pid):
    # URL & PLAYER ID
    url = f"https://www.transfermarkt.com/{player_code}/verletzungen/spieler/{pid}"

    # Request
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    try:
        temp = pd.read_html(str(soup.find("table", class_="items")))[0]

        try:
            page = len(soup.find("div", class_="pager").find_all("li", class_="page"))
            if page > 1:
                for page_num in np.arange(2, page + 1, 1):
                    url2 = url + "/ajax/yw1/page/" + str(page_num)
                    soup2 = BeautifulSoup(
                        requests.get(url2, headers=headers).content, "html.parser"
                    )
                    temp_table2 = pd.read_html(
                        str(soup2.find("table", class_="items"))
                    )[0]
                    temp = temp.append(temp_table2)

        except Exception as e:
            print(e)
            pass

        temp["TMId"] = pid

        return temp

    except Exception as e:
        print(e)
        pass
