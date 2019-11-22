from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd

# url for future undergrad faq
# url = 'https://itsc.ontariotechu.ca/faqs/faqs-students.php'

# faculty itcs link
url = 'https://itsc.ontariotechu.ca/faqs/faqs-faculty-staff.php'

# open connection to webpage and read the html
client = uReq(url)
pagehtml = client.read()
client.close()

# read parse the html
html = soup(pagehtml, "html.parser")

# loop through all the html data and remove break tags
for i in html.findAll('br'):
    i.extract()

data = html.find_all('a', {'class':'accordion-title'})

string_data = []
for i in data:
    string_data.append(str(i.text))

df = pd.DataFrame(string_data)

df.insert(1, '1', 'itcs_faculty-Staff_faq')

print (df)

# df.to_csv('itcs_faculty-Staff_faq.csv', encoding='utf-8', index=False, header=False)
