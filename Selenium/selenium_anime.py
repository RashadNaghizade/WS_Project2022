#############################
# imports

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import sys
import csv
import os
import time
import urllib
import datetime
import re
import pandas as pd
import urllib.request
# from fake_useragent import UserAgent


#############
# taking links to genres and saving them together with a column of their names

link = 'https://myanimelist.net/anime.php'
chrome = webdriver.Chrome()
chrome.get(link)
time.sleep(1)

all_genre_links = []
all_genre_name =[]

agree_button = chrome.find_element(by=By.CSS_SELECTOR, value="button.css-1hy2vtq")
agree_button.click()
time.sleep(2)

links = chrome.find_elements(by=By.CSS_SELECTOR, value="div.genre-link div.genre-list.al a")

all_genre_links = [selector.get_attribute("href") for selector in links]
all_genre_name = [selector.text for selector in links]

df_1 = pd.DataFrame(list(zip(all_genre_links, all_genre_name)),
                    columns=['link', 'name'])

df_1 = df_1.iloc[:18,]

chrome.close()


############################################
# taking all anime links on the first page in each genre scraped above

chrome = webdriver.Chrome()

df_for_concating = pd.DataFrame()

for idx, genre_link in enumerate(df_1['link']):
    chrome.get(genre_link)

    #     agree_button = chrome.find_element(by=By.CSS_SELECTOR, value="button.css-1hy2vtq")
    #     agree_button.click()
    #     time.sleep(2)

    anime = chrome.find_elements(by=By.CSS_SELECTOR, value="h2.h2_anime_title a")

    name_of_genre = chrome.find_element(by=By.CSS_SELECTOR, value="span.di-ib.mt4").text
    amime_names_link = [selector.get_attribute("href") for selector in anime]
    anime_titles = [selector.text for selector in anime]
    genre_name_for_df = [df_1['name'][idx]] * len(anime)

    df_temporary = pd.DataFrame(list(zip(amime_names_link, anime_titles, genre_name_for_df)),
                                columns=['link', 'title', 'genre_name'])

    df_for_concating = pd.concat([df_for_concating, df_temporary], axis=0)

chrome.close()


#####################
# scraping the attributes of each anime

chrome = webdriver.Chrome()

score_ = []
rank_ = []
popularity_ = []
members_ = []
date_ = []
type_tv_ = []

for idx, anime_link in enumerate(df_for_concating['link']):
    chrome.get(anime_link)

    try:
        agree_button = chrome.find_element(by=By.CSS_SELECTOR, value="button.css-1hy2vtq")
        if agree_button:
            agree_button.click()
            time.sleep(2)

        score = chrome.find_element(by=By.CSS_SELECTOR, value='div.score-label.score-8').text
        rank = chrome.find_element(by=By.CSS_SELECTOR, value='span.numbers.ranked strong').text
        popularity = chrome.find_element(by=By.CSS_SELECTOR, value='span.numbers.popularity strong').text
        members = chrome.find_element(by=By.CSS_SELECTOR, value='span.numbers.members strong').text
        date = chrome.find_element(by=By.CSS_SELECTOR, value='span.information.season a').text
        type_tv = chrome.find_element(by=By.CSS_SELECTOR, value='span.information.type a').text

    except NoSuchElementException as e:
        print(f"Warning: {e})

    score_.append(score)
    rank_.append(rank)
    popularity_.append(popularity)
    members_.append(members)
    date_.append(date)
    type_tv_.append(type_tv)
    print(f'{idx} {anime_link} scraping completed')

df_for_concating['score'] = score_
df_for_concating['rank'] = rank_
df_for_concating['popularity'] = popularity_
df_for_concating['members'] = members_
df_for_concating['date'] = date_
df_for_concating['type_tv'] = type_tv_


df_for_concating.to_csv('df.csv')