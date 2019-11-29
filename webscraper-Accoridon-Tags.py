from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd

# url for future undergrad faq
# url = 'https://itsc.ontariotechu.ca/faqs/faqs-students.php'

userInput1 = str(input("Please Provide url from FAQ acoridion: "))
userInput2 = str(input("Please Provide a file name ending with .csv: "))
userInput3 = str(input("Please give name of faq name: "))

# faculty itcs link
url = userInput1

# open connection to webpage and read the html
client = uReq(url)
pagehtml = client.read()
client.close()

# read parse the html
html = soup(pagehtml, "html.parser")

# loop through all the html data and remove break tags
for i in html.findAll('br'):
    i.extract()

data = html.find_all('a', {'class': 'accordion-title'})

# convert each input to a string and appending to
# separate array
string_data = []
for i in data:
    string_data.append(str(i.text))

df = pd.DataFrame(string_data)

df.insert(1, '1', userInput3)

print (df)

# Exports data to a csv file which can be uploaded to Watson Assistant.
df.to_csv(userInput2, encoding='utf-8', index=False, header=False)
