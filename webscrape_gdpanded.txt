from bs4 import BeautifulSoup
import requests
import pandas as pd
import warnings # current version of seaborn generates a bunch of warnings that we'll ignore
warnings.filterwarnings("ignore")
import seaborn as sns # try to install seaborn from home


url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(r.content)

table = soup.find_all('table')[6]

header_html = table.find(class_='lheader').find_all('td')
column_names = [c.text for c in header_html if len(c.text) > 0]

rows = table.find_all('tr', {'class': 'tcont'})    

cells = [[c.text for c in row.find_all('td')] for row in rows]

countries_df = pd.DataFrame(cells)

cleaned_df = countries_df.drop([2, 3, 5, 6, 8, 9, 11], axis=1)
  
#cleaned_df = cleaned_df.drop(cleaned_df[0][94:99])

cleaned_df.columns = column_names

cleaned_df = cleaned_df[cleaned_df.Total.notnull()]

for col in cleaned_df:
    print(col, cleaned_df[col].dtypes)
    
cleaned_df['Total'] = cleaned_df['Total'].astype('int64')
cleaned_df['Men'] = cleaned_df['Men'].astype('int64')
cleaned_df['Women'] = cleaned_df['Women'].astype('int64')

#### Analysis ####
# Distribution of Values

sns.boxplot(cleaned_df[["Total", "Women", "Men"]])

cleaned_df['Total'].mean()
cleaned_df['Women'].mean()
cleaned_df['Men'].mean()

sns.lmplot('Women', 'Men', data=cleaned_df, fit_reg=True)

### GDP Data
gdp_df = pd.read_csv('C:\\Users\\abrown09\\Desktop\\Data Science\\Python\\Thinkful\\Unit 3\\Lesson_3\\GDP Data\\gdp_pandas.csv', encoding='latin')   
gdp_df = gdp_df[gdp_df['1999'].notnull()]

### join GDP with cleaned_UN data
cleaned_df = cleaned_df.rename(columns={'Country or area': 'Country Name'})

# this works-but it doesn't account for names that are formatted differently between the two dfs, which results in them  being dropped
# also, i need to figure out a way to merge on or match on column, so that the country is only matched with the gdp of the same year the education data represents
test_df = pd.merge(cleaned_df, gdp_df, left_on='Country Name', right_on='Country Name') # this is the right process but I need

year_dict = cleaned_df.set_index('Country Name')['Year'].to_dict()


df = pd.Dataframe()

for k, v in year_dict.items():
    if k == gdp_df['Country Name']:
        print(1)