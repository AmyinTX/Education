#%%
from bs4 import BeautifulSoup
import requests
import pandas as pd
import warnings # current version of seaborn generates a bunch of warnings that we'll ignore
warnings.filterwarnings("ignore")
import seaborn as sns # try to install seaborn from home
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process
import numpy as np
#%%
url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(r.content)

#%%
table = soup.find_all('table')[6]
header_html = table.find(class_='lheader').find_all('td')
column_names = [c.text for c in header_html if len(c.text) > 0]
rows = table.find_all('tr', {'class': 'tcont'})    
cells = [[c.text for c in row.find_all('td')] for row in rows]

#%%
countries_df = pd.DataFrame(cells)
cleaned_df = countries_df.drop([2, 3, 5, 6, 8, 9, 11], axis=1)
cleaned_df.columns = column_names
cleaned_df = cleaned_df[cleaned_df.Total.notnull()]

#%%
for col in cleaned_df:
    print(col, cleaned_df[col].dtypes)
    
cleaned_df['Total'] = cleaned_df['Total'].astype('int64')
cleaned_df['Men'] = cleaned_df['Men'].astype('int64')
cleaned_df['Women'] = cleaned_df['Women'].astype('int64')

#%%
#### Analysis ####
# Distribution of Values

sns.boxplot(cleaned_df[["Total", "Women", "Men"]])

cleaned_df['Total'].mean()
cleaned_df['Women'].mean()
cleaned_df['Men'].mean()

sns.lmplot('Women', 'Men', data=cleaned_df, fit_reg=True)

#%%
### GDP Data
gdp_df = pd.read_csv('/Users/amybrown/Thinkful/Unit_3/Lesson_3/clean_gdp.csv', encoding='latin')   
gdp_df = gdp_df[gdp_df['1999'].notnull()]

#%%
### join GDP with cleaned_UN data
cleaned_df = cleaned_df.rename(columns={'Country or area': 'Country Name'})

keys = [c for c in gdp_df if c.startswith('19') or c.startswith('20')]
stacked = pd.melt(gdp_df, id_vars='Country Name',  value_vars=keys, value_name='key')
stacked = stacked.rename(columns={'variable': 'Year'})
stacked = stacked.rename(columns={'key': 'GDP'})

final_df = pd.merge(cleaned_df, stacked, on=['Country Name', 'Year'])

for col in final_df:
    print(col, final_df[col].dtypes) 
    
# GDP needs to be changed from object to int and I need to strip the commas out
final_df['GDP'] = final_df['GDP'].str.replace(',', '')
final_df['GDP'] = final_df['GDP'].astype('int64') # it worked!

#%%

#%% any relationship between school life expectancy and GDP?

plt.scatter(final_df['GDP'], final_df['Total'])


x = final_df['GDP']
y = final_df['Total']

# make a scatterplot with seaborn
plt.scatter(x, y)
pearsonr(x, y)
#%% try a log transformation of the GDP variable
log_gdp = (np.log(final_df['GDP']))

plt.scatter(log_gdp, y)
pearsonr(log_gdp, y)