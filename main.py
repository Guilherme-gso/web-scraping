import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

# WEBSCRAPING 
URL = 'https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1'
chromedriver = 'C:/webdriver/chromedriver'

# Recuperando html a partir da URL
option = Options()
option.headless=True
driver = webdriver.Chrome(chromedriver)

driver.get(URL)
time.sleep(10)

driver.find_element_by_xpath('//div[@class="nba-stat-table"]//table//thead//tr//th[@data-field="PTS"]').click()

# Recuperando elemento 
element = driver.find_element_by_xpath('//div[@class="nba-stat-table"]//table')
html = element.get_attribute('outerHTML')

# Parse do HTML pra dataframe
soup = BeautifulSoup(html, 'html.parser')
table = soup.find(name='table')

df_full = pd.read_html(str(table))[0].head(10) # usando panda pra criar um dataframe com dados legiveis
df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', 'PTS']]
df.columns = ['pos', 'player', 'team', 'total']
print(df_full)

# Conversão para dicionário
ranking = {}
ranking['points'] = df.to_dict('records')

# Conversão para json
js = json.dumps(ranking)
nf = open('ranking.json', 'w')
nf.write(js)
nf.close()

driver.quit()