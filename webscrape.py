# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 14:38:55 2017

@author: amybrown
"""

#%%
from bs4 import BeautifulSoup
import requests

#%%
#Import page
url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

r = requests.get(url)



soup = BeautifulSoup(open(r.content))

#%%
for row in soup('table'):
    print(row)
    
soup('table')[6]

#%%
soup.title

soup.title.name

soup.title.string

soup.title.parent.name

soup.p["class"]

soup.a

soup.find_all

#%%
for link in soup.find_all('a'):
    print(link.get('href')) # this looks like it extracts all links
    
#%%
print(soup.get_text()) # extracts all page text
