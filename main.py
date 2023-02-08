import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup

import sys
import time
from datetime import datetime
from termcolor import colored

from injury_scraping import get_injuries


def main():
    injuries = get_injuries("antony", 602105)
    print(injuries)


if __name__ == "__main__":
    main()
