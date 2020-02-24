from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd

# url for web page to be parsed
url = "specific url to be parsed"

# open connection to webpage and read the html
client = uReq(url)
pagehtml = client.read()
client.close()

# read parse the html
html = soup(pagehtml, "html.parser")

# loop through all the html data and remove break tags
for i in html.findAll('br'):
    i.extract()

data = html.findAll("strong")

string_arr = []
# take in html data and convert it to strings
for i in data[17:]:
    string = str(i.text)
    string_arr.append(string)

# remove non breaking spaces and empty strings
for i in string_arr:
    if i == '\xa0':
        string_arr.remove(i)
    if i == ' ':
        string_arr.remove(i)

# create and export dataframes to csv
df= pd.DataFrame(string_arr)
df.insert(1, '1', 'test_intents')
df.to_csv('new_intents.csv', encoding='utf-8', index=False, header=False)
