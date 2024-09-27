# I am looking at the Craigslist books page for this assignment. Unfortunately, there was not much data to scrape beyond the price.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Page requests
import requests

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'}
url = 'https://charlottesville.craigslist.org/search/bka#search=1~gallery~0~0'
raw = requests.get(url, headers=header) # Get page

from bs4 import BeautifulSoup as soup # HTML parser
bsObj = soup(raw.content,'html.parser') # Parse the html
listings = bsObj.find_all(class_="cl-static-search-result") # Find all listings

import re

data = []

for k in range( len(listings) ):
    title = listings[k].find('div',class_='title').get_text().lower()
    price = listings[k].find('div',class_='price').get_text()
    link = listings[k].find(href=True)['href']
    words = title.split()

    # Get years from title string:
    regex_search = re.search(r'20[0-9][0-9]|19[0-9][0-9]', title ) # Find year references
    if regex_search is None: # If no hits, record year as missing value
        year = np.nan
    else: # If hits, record year as first match
        year = regex_search.group(0)
    #
    data.append({'title':title,'price':price,'year':year,'link':link})

# Wrangle the data
df = pd.DataFrame.from_dict(data)
df['price'] = df['price'].str.replace('$','')
df['price'] = df['price'].str.replace(',','')
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['year'] = pd.to_numeric(df['year'], errors='coerce')
print(df.shape)
df.to_csv('craigslist_cville_books.csv')
df.head()

# EDA for price:
print(df['price'].describe())
df['price'].hist(grid=False)
plt.show()

# how many books are $10 or less
under_10 = df[df['price'] <= 10]
under_10.head()
len(under_10)

# how many books are greater than $100?
over_100 = df[df['price'] >= 100]
over_100.head()
len(over_100)