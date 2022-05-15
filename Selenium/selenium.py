################################################################
# imports
from importlib.resources import path
from xml.etree.ElementTree import XML
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time

################################################################

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
# driver=webdriver.Chrome(executable_path="C:\Users\orxan\Desktop\web_scr7\chromedriver.exe")
wait = WebDriverWait(driver,1.5)

# url
url = 'https://myanimelist.net/anime.php'
driver.get(url)
time.sleep(2)

# close cookies
cookies_ = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/button[1]')
cookies_.click()
time.sleep(1)

#################
list_genres = []

path = '//a[re:test(@class, "genre-name-link")]/@href'

list_links = driver.find_elements_by_xpath(path)
for link_to_genre in list_links:
    elem = link_to_genre.get_attribute("href")
    list_genres.append(elem)

###################
# entering each link and scraping the 7 pieces of information
name        = []
score       = []
rank        = []
popularity  = []
members     = []
date        = []
channel     = []

# traverse list
for genre in list_genres:
    driver.get(By.XPATH, (genre + '[class="h2_anime_title"] a'))
    links = []
    for item in links:
      links.append(item.get_attribute('href'))
      for link in links:
          driver.get(link)
          name = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="h1-title"]')))
          score = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class"="score-label"]')))
          rank = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="di-ib ml12 pl20 pt8"]')))
          popularity = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="numbers popularity"]')))
          members = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="numbers members"]')))
          date = wait.until(EC.visibility_of_element_located((By.Xpath, '//*[@id="content"]/table/tbody/tr/td[1]/div/div[12]/text()')))
          channel = wait.until(EC.visibility_of_element_located((By.Xpath, '//*[@id="content"]/table/tbody/tr/td[1]/div/div[9]/a')))
          name.append(name.text)
          score.append(score.text)
          rank.append(rank.text)
          popularity.append(popularity.text)
          members.append(members.text)
          date.append(date.text)
          channel.append(channel.text)
          driver.back()
          time.sleep(2)

dataset = pd.DataFrame(
    {'name': name,
    'score': score,
    'rank': rank,
    'score': score,
    'popularity': popularity,
    'members': members,
    'date': date,
    'channel': channel
    })

dataset = dataset.iloc[:667,:]
dataset.to_csv('dataset_anime.csv')


driver.quit()