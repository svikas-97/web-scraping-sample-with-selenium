from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time

website = 'https://www.scrapethissite.com/pages/ajax-javascript/'
path = 'C:\Program Files\chromedriver'
driver = webdriver.Chrome(path)
driver.get(website)

time.sleep(10)

title = []
nominations = []
awards = []
year = []


for i in range(2010,2016):
    button = driver.find_element_by_xpath('//a[@id={}]'.format(i))
    button.click()

    time.sleep(5)

    film_name = driver.find_elements_by_class_name('film-title')
    for film_title in film_name:
        title.append(film_title.text)

    film_nominations = driver.find_elements_by_class_name('film-nominations')
    for film_nomination in film_nominations:
        nominations.append(film_nomination.text)

    film_awards = driver.find_elements_by_class_name('film-awards')
    for film_award in film_awards:
        awards.append(film_award.text)
driver.quit()


r = requests.get('https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films')
soup = bs(r.content)
# print(soup.prettify())

for i in range(2010,2016):
    tag_a = soup.find_all('a', title='{} in film'.format(i))
    text_year = [tag.get_text() for tag in tag_a]
    year.append(text_year)

year = year[0]+year[1]+year[2]+year[3]+year[4]+year[5]

# print(year)

df = pd.DataFrame({
    'Title': title,
    'Year': year,
    'Nominations': nominations,
    'Awards': awards
})

# print(df)

df.to_csv('2010-2015 oscar winning films.csv', index=False)

