# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 09:54:23 2017

@author: amybrown
"""

from bs4 import BeautifulSoup
import requests
import urllib2


url = 'https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India'
r = requests.get(url)
soup = BeautifulSoup(open(r.content))


print(soup.prettify())

soup.title
soup.title.string
soup.a
soup.find_all("a")

all_links=soup.find_all("a")
for link in all_links:
    print(link.get("href"))
    
soup.td
soup.find_all("td")
all_x = soup.find_all("td")
for x in all_x:
    print(x.get("td"))

all_tables=soup.find_all('table')

right_table=soup.find_all('table', class_='tcont')