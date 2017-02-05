# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 20:41:04 2017

@author: amybrown
"""
from bs4 import BeautifulSoup
import requests

url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

r = requests.get(url)
soup = BeautifulSoup(open(r.content))


country = soup.find("tr", {"class": "tcont"}).td.contents # extracts the first element in the table!

country = soup.find_all("tr", {"class": "tcont"}).td.contents # doesn't work to grab all elements in the country column

print(soup.prettify)



all_tables = soup.find_all('table')

right_table = soup.find('tr', class_ = "tcont").td.contents

A=[]

for row in right_table.find_all('tr'):
    cells = row.find_all('td')
    states=row.find_all('th') #To store second column data
    if len(cells)==6: #Only extract table body not heading
        A.append(cells[0].find(text=True))
